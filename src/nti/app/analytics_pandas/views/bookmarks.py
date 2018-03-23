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

from nti.analytics_pandas.analysis import BookmarkCreationTimeseries

from nti.analytics_pandas.analysis.common import reset_dataframe_

from nti.app.analytics_pandas.views import MessageFactory as _

from nti.app.analytics_pandas.views.commons import add_one_more_day
from nti.app.analytics_pandas.views.commons import get_default_start_end_date
from nti.app.analytics_pandas.views.commons import build_event_chart_data
from nti.app.analytics_pandas.views.commons import build_event_table_data
from nti.app.analytics_pandas.views.commons import save_chart_to_temporary_file
from nti.app.analytics_pandas.views.commons import build_event_grouped_chart_data
from nti.app.analytics_pandas.views.commons import build_event_grouped_table_data
from nti.app.analytics_pandas.views.commons import get_course_id_and_name_given_ntiid
from nti.app.analytics_pandas.views.commons import build_events_data_by_sharing_type
from nti.app.analytics_pandas.views.commons import build_events_data_by_resource_type
from nti.app.analytics_pandas.views.commons import build_events_data_by_enrollment_type

from nti.app.analytics_pandas.views.mixins import AbstractReportView

logger = __import__('logging').getLogger(__name__)

@view_config(name="BookmarksReport")
class BookmarksTimeseriesReportView(AbstractReportView):

    @property
    def report_title(self):
        return _(u'Bookmarks Report')

    def _build_data(self, data=_('sample bookmarks report')):
        keys = self.options.keys()
        if 'has_bookmarks_created_data' not in keys:
            self.options['has_bookmarks_created_data'] = False
        if 'has_bookmarks_created_per_resource_types' not in keys:
            self.options['has_bookmarks_created_per_resource_types'] = False 
        if 'has_bookmarks_created_per_enrollment_types' not in keys:
            self.options['has_bookmarks_created_per_enrollment_types'] = False
        self.options['data'] = data
        return self.options

    def __call__(self):
        values = self.readInput()
        if 'start_date' and 'end_date' not in values.keys():
            values['start_date'], values['end_date'] = get_default_start_end_date()
        if "MimeType" not in values.keys():
            values["MimeType"] = 'application/vnd.nextthought.reports.bookmarkeventstimeseriescontext'
        self.options['ntiid'] = values['ntiid']
        course_ids, course_names = get_course_id_and_name_given_ntiid(self.db.session,
                                                                      self.options['ntiid'])
        data = {}
        if course_ids and course_names:
            self.options['course_ids'] = course_ids
            self.options['course_names'] = ", ".join(map(str, course_names or ()))
            self.options['start_date'] = values['start_date']
            self.options['end_date'] = add_one_more_day(values['end_date'])
            if 'period' in values.keys():
                self.options['period'] = values['period']
            else:
                self.options['period'] = u'daily'
            bct = BookmarkCreationTimeseries(self.db.session,
                                          self.options['start_date'],
                                          self.options['end_date'],
                                          self.options['course_ids'] or (),
                                          period=self.options['period'])
            if not bct.dataframe.empty:
                self.options['has_bookmarks_created_data'] = True
                data['bookmarks_created'] = self.build_bookmarks_created_data(bct)
        self._build_data(data)
        return self.options

    def build_bookmarks_created_data(self, bct):
        bookmarks_created = {}
        df = bct.analyze_events()
        df = reset_dataframe_(df)
        bookmarks_created['num_rows'] = df.shape[0]
        bookmarks_created['column_name'] = _(u'Bookmarks Created')
        if bookmarks_created['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_bookmarks_created',
                                           'Bookmarks Created')
            bookmarks_created['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            bookmarks_created['events_chart'] = ()
        
        if bookmarks_created['num_rows'] == 1:
            bookmarks_created['tuples'] = build_event_table_data(df)
        else:
            bookmarks_created['tuples'] = ()
        self.build_bookmarks_created_by_resource_type_data(bct, bookmarks_created)
        self.build_bookmarks_created_by_enrollment_type_data(bct, bookmarks_created)
        return bookmarks_created

    def build_bookmarks_created_by_resource_type_data(self, bct, bookmarks_created):
        resources = bct.analyze_resource_types()
        if resources[0] is not None:
            df = resources[0]
            if df.empty:
                self.options['has_bookmarks_created_per_resource_types'] = False
                return
            self.options['has_bookmarks_created_per_resource_types'] = True
            df = reset_dataframe_(df)
            columns = ['timestamp_period', 'resource_type',
                       'number_of_bookmarks_created']
            df = df[columns]
            build_events_data_by_resource_type(df, bookmarks_created)

    def build_bookmarks_created_by_enrollment_type_data(self, bct, bookmarks_created):
        df = bct.analyze_enrollment_types()
        if df.empty:
            self.options['has_bookmarks_created_per_enrollment_types'] = False
            return
        df = reset_dataframe_(df)
        self.options['has_bookmarks_created_per_enrollment_types'] = True
        columns = ['timestamp_period', 'enrollment_type',
                   'number_of_bookmarks_created']
        df = df[columns]
        build_events_data_by_enrollment_type(df, bookmarks_created)
