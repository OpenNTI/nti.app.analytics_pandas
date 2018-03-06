#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import numpy as np

from pyramid.view import view_config

from nti.analytics_pandas.analysis import NoteLikesTimeseries
from nti.analytics_pandas.analysis import NotesViewTimeseries
from nti.analytics_pandas.analysis import NotesCreationTimeseries
from nti.analytics_pandas.analysis import NoteFavoritesTimeseries

from nti.analytics_pandas.analysis.common import get_data
from nti.analytics_pandas.analysis.common import reset_dataframe_

from nti.app.analytics_pandas.views import MessageFactory as _

from nti.app.analytics_pandas.views.commons import iternamedtuples
from nti.app.analytics_pandas.views.commons import build_event_chart_data
from nti.app.analytics_pandas.views.commons import build_event_table_data
from nti.app.analytics_pandas.views.commons import save_chart_to_temporary_file
from nti.app.analytics_pandas.views.commons import build_event_grouped_chart_data
from nti.app.analytics_pandas.views.commons import build_event_grouped_table_data
from nti.app.analytics_pandas.views.commons import get_course_id_and_name_given_ntiid
from nti.app.analytics_pandas.views.commons import build_events_data_by_device_type
from nti.app.analytics_pandas.views.commons import build_events_data_by_sharing_type
from nti.app.analytics_pandas.views.commons import build_events_data_by_resource_type
from nti.app.analytics_pandas.views.commons import build_events_data_by_enrollment_type

from nti.app.analytics_pandas.views.mixins import AbstractReportView

logger = __import__('logging').getLogger(__name__)


@view_config(name="NotesReport")
class NotesTimeseriesReportView(AbstractReportView):

    @property
    def report_title(self):
        return _(u'Notes Report')

    def _build_data(self, data=_('sample notes report')):
        keys = self.options.keys()
        if 'has_note_view_events' not in keys:
            self.options['has_note_view_events'] = False
            self.options['has_note_views_per_enrollment_types'] = False
            self.options['has_note_views_per_device_types'] = False
            self.options['has_note_views_per_resource_types'] = False
            self.options['has_note_views_per_sharing_types'] = False
        if 'has_note_create_events' not in keys:
            self.options['has_note_create_events'] = False
            self.options['has_notes_created_per_resource_types'] = False
            self.options['has_notes_created_per_device_types'] = False
            self.options['has_notes_created_per_enrollment_types'] = False
            self.options['has_notes_created_per_sharing_types'] = False
        if 'has_note_like_events' not in keys:
            self.options['has_note_like_events'] = False
        if 'has_note_favorite_events' not in keys:
            self.options['has_note_favorite_events'] = False
        self.options['data'] = data
        return self.options

    def __call__(self):
        values = self.readInput()
        if "MimeType" not in values.keys():
            values["MimeType"] = 'application/vnd.nextthought.reports.noteeventstimeseriescontext'
        self.options['ntiid'] = values['ntiid']
        course_ids, course_names = get_course_id_and_name_given_ntiid(self.db.session,
                                                                      self.options['ntiid'])
        data = {}
        if course_ids and course_names:
            self.options['course_ids'] = course_ids
            self.options['course_names'] = ", ".join(map(str, course_names or ()))
            self.options['start_date'] = values['start_date']
            self.options['end_date'] = values['end_date']
            if 'period' in values.keys():
                self.options['period'] = values['period']
            else:
                self.options['period'] = u'daily'
            nvt = NotesViewTimeseries(self.db.session,
                                      self.options['start_date'],
                                      self.options['end_date'],
                                      self.options['course_ids'] or (),
                                      period=self.options['period'])
            if not nvt.dataframe.empty:
                self.options['has_note_view_events'] = True
                data['notes_viewed'] = self.build_notes_viewed_data(nvt)
            nct = NotesCreationTimeseries(self.db.session,
                                      self.options['start_date'],
                                      self.options['end_date'],
                                      self.options['course_ids'] or (),
                                      period=self.options['period'])
            if not nct.dataframe.empty:
                self.options['has_note_create_events'] = True
                data['notes_created'] = self.build_notes_created_data(nct)
            nlt = NoteLikesTimeseries(self.db.session,
                                      self.options['start_date'],
                                      self.options['end_date'],
                                      self.options['course_ids'] or (),
                                      period=self.options['period'])
            if not nlt.dataframe.empty:
                self.options['has_note_like_events'] = True
                data['notes_liked'] = self.build_notes_liked_data(nlt)
            nft = NoteFavoritesTimeseries(self.db.session,
                                      self.options['start_date'],
                                      self.options['end_date'],
                                      self.options['course_ids'] or (),
                                      period=self.options['period'])
            if not nft.dataframe.empty:
                self.options['has_note_favorite_events'] = True
                data['notes_favorite'] = self.build_notes_liked_data(nft)
        values = self.readInput()
        self._build_data(data)
        return self.options

    def build_notes_viewed_data(self, nvt):
        note_views = {}
        df = nvt.analyze_total_events()
        df = reset_dataframe_(df)
        note_views['num_rows'] = df.shape[0]
        note_views['column_name'] = _(u'Notes Viewed')
        if note_views['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_note_views',
                                           'Notes Viewed')
            note_views['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            note_views['events_chart'] = ()
        
        if note_views['num_rows'] == 1:
            note_views['tuples'] = build_event_table_data(df)
        else:
            note_views['tuples'] = ()

        self.get_the_n_most_viewed_notes_and_its_author(nvt, note_views, max_rank_number=10)
        self.build_notes_viewed_by_resource_type_data(nvt, note_views)
        self.build_notes_viewed_by_device_type_data(nvt, note_views)
        self.build_notes_viewed_by_enrollment_type_data(nvt, note_views)
        self.build_notes_viewed_by_sharing_type_data(nvt, note_views)
        return note_views

    def build_notes_viewed_by_device_type_data(self, nvt, note_views):
        df = nvt.analyze_total_events_based_on_device_type()
        if df.empty:
            self.options['has_note_views_per_device_types'] = False
            return
        df = reset_dataframe_(df)
        self.options['has_note_views_per_device_types'] = True
        columns = ['timestamp_period', 'device_type',
                   'number_of_note_views']
        df = df[columns]
        build_events_data_by_device_type(df, note_views)

    def build_notes_viewed_by_enrollment_type_data(self, nvt, note_views):
        df = nvt.analyze_total_events_based_on_enrollment_type()
        if df.empty:
            self.options['has_note_views_per_enrollment_types'] = False
            return
        self.options['has_note_views_per_enrollment_types'] = True
        df = reset_dataframe_(df)
        columns = ['timestamp_period', 'enrollment_type',
                   'number_of_note_views']
        df = df[columns]
        build_events_data_by_enrollment_type(df, note_views)

    def build_notes_viewed_by_resource_type_data(self, nvt, note_views):
        df = nvt.analyze_total_events_based_on_resource_type()
        if df.empty:
            self.options['has_note_views_per_resource_types'] = False
            return
        self.options['has_note_views_per_resource_types'] = True
        df = reset_dataframe_(df)
        columns = ['timestamp_period', 'resource_type',
                   'number_of_note_views']
        df = df[columns]
        build_events_data_by_resource_type(df, note_views)

    def build_notes_viewed_by_sharing_type_data(self, nvt, note_views):
        df = nvt.analyze_total_events_based_on_sharing_type()
        if df.empty:
            self.options['has_note_views_per_sharing_types'] = False
            return
        self.options['has_note_views_per_sharing_types'] = True
        df = reset_dataframe_(df)
        columns = ['timestamp_period', 'sharing',
                   'number_of_note_views']
        df = df[columns]
        build_events_data_by_sharing_type(df, note_views)

    def get_the_n_most_viewed_notes_and_its_author(self, nvt, note_views, max_rank_number=10):
        df = nvt.get_the_most_viewed_notes_and_its_author(max_rank_number)
        columns = ['note_id', 'number_of_views', 'author_name']
        df = df[columns]
        tuples = iternamedtuples(df, columns)
        note_views['n_most_viewed_notes'] = tuples

    def build_notes_created_data(self, nct):
        notes_created = {}
        dataframes = get_data(nct)
        df = dataframes['df_by_timestamp']
        notes_created['num_rows'] = df.shape[0]
        notes_created['column_name'] = _(u'Notes Created')
        if notes_created['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_notes_created',
                                           'Notes Created')
            notes_created['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            notes_created['events_chart'] = ()
        
        if notes_created['num_rows'] == 1:
            notes_created['tuples'] = build_event_table_data(df)
        else:
            notes_created['tuples'] = ()
        self.build_notes_created_by_resource_type_data(nct, notes_created)
        if 'df_per_device_types' in dataframes.keys():
            self.build_notes_created_by_device_type_data(dataframes['df_per_device_types'], notes_created)
        if 'df_per_enrollment_type' in dataframes.keys():
            self.build_notes_created_by_enrollment_type_data(dataframes['df_per_enrollment_type'], notes_created)
        self.build_notes_created_by_sharing_type_data(nct, notes_created)
        return notes_created

    def build_notes_created_by_resource_type_data(self, nct, notes_created):
        df = nct.analyze_resource_types()
        if df.empty:
            self.options['has_notes_created_per_resource_types'] = False
            return
        self.options['has_notes_created_per_resource_types'] = True
        df = reset_dataframe_(df)
        columns = ['timestamp_period', 'resource_type',
                   'number_of_notes_created']
        df = df[columns]
        build_events_data_by_resource_type(df, notes_created)

    def build_notes_created_by_device_type_data(self, df, notes_created):
        if df.empty:
            self.options['has_notes_created_per_device_types'] = False
            return
        self.options['has_notes_created_per_device_types'] = True
        columns = ['timestamp_period', 'device_type',
                   'number_of_notes_created']
        df = df[columns]
        build_events_data_by_device_type(df, notes_created)

    def build_notes_created_by_enrollment_type_data(self, df, notes_created):
        if df.empty:
            self.options['has_notes_created_per_enrollment_types'] = False
            return
        self.options['has_notes_created_per_enrollment_types'] = True
        columns = ['timestamp_period', 'enrollment_type',
                   'number_of_notes_created']
        df = df[columns]
        build_events_data_by_enrollment_type(df, notes_created)

    def build_notes_created_by_sharing_type_data(self, nct, notes_created):
        df = nct.analyze_sharing_types()
        if df.empty:
            self.options['has_notes_created_per_sharing_types'] = False
            return
        self.options['has_notes_created_per_sharing_types'] = True
        df = reset_dataframe_(df)
        columns = ['timestamp_period', 'sharing',
                   'number_of_notes_created']
        df = df[columns]
        build_events_data_by_sharing_type(df, notes_created)

    def build_notes_liked_data(self, nlt):
        notes_liked = {}
        df = nlt.analyze_events()
        df = reset_dataframe_(df)
        notes_liked['num_rows'] = df.shape[0]
        notes_liked['column_name'] = _(u'Notes Liked')
        if notes_liked['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_note_likes',
                                           'Notes Liked')
            notes_liked['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            notes_liked['events_chart'] = ()
        
        if notes_liked['num_rows'] == 1:
            notes_liked['tuples'] = build_event_table_data(df)
        else:
            notes_liked['tuples'] = ()
        return notes_liked

    def build_notes_favorite_data(self, nft):
        notes_favorite = {}
        df = nft.analyze_events()
        df = reset_dataframe_(df)
        notes_favorite['num_rows'] = df.shape[0]
        notes_favorite['column_name'] = _(u'Notes Favorite')
        if notes_favorite['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_note_favorites',
                                           'Notes Favorite')
            notes_favorite['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            notes_favorite['events_chart'] = ()
        
        if notes_favorite['num_rows'] == 1:
            notes_favorite['tuples'] = build_event_table_data(df)
        else:
            notes_favorite['tuples'] = ()
        return notes_favorite
