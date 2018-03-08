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

from nti.analytics_pandas.analysis import HighlightsCreationTimeseries

from nti.analytics_pandas.analysis.common import reset_dataframe_

from nti.app.analytics_pandas.views import MessageFactory as _

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

@view_config(name="HighlightsReport")
class HighlightsTimeseriesReportView(AbstractReportView):

    @property
    def report_title(self):
        return _(u'Highlights Report')

    def _build_data(self, data=_('sample highlights report')):
        keys = self.options.keys()
        if 'has_highlights_created_data' not in keys:
            self.options['has_highlights_created_data'] = False
        if 'has_highlights_created_per_resource_types' not in keys:
            self.options['has_highlights_created_per_resource_types'] = False 
        if 'has_highlights_created_per_enrollment_types' not in keys:
            self.options['has_highlights_created_per_enrollment_types'] = False
        self.options['data'] = data
        return self.options

    def __call__(self):
        values = self.readInput()
        if "MimeType" not in values.keys():
            values["MimeType"] = 'application/vnd.nextthought.reports.highlighteventstimeseriescontext'
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
            hct = HighlightsCreationTimeseries(self.db.session,
                                          self.options['start_date'],
                                          self.options['end_date'],
                                          self.options['course_ids'] or (),
                                          period=self.options['period'])
            if not hct.dataframe.empty:
                self.options['has_highlights_created_data'] = True
                data['highlights_created'] = self.build_highlights_created_data(hct)
        self._build_data(data)
        return self.options

    def build_highlights_created_data(self, hct):
        highlights_created = {}
        df = hct.analyze_events()
        df = reset_dataframe_(df)
        highlights_created['num_rows'] = df.shape[0]
        highlights_created['column_name'] = _(u'Highlights Created')
        if highlights_created['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_highlights_created',
                                           'Highlights Created')
            highlights_created['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            highlights_created['events_chart'] = ()
        
        if highlights_created['num_rows'] == 1:
            highlights_created['tuples'] = build_event_table_data(df)
        else:
            highlights_created['tuples'] = ()
        self.build_highlights_created_by_resource_type_data(hct, highlights_created)
        self.build_highlights_created_by_enrollment_type_data(hct, highlights_created)
        return highlights_created

    def build_highlights_created_by_resource_type_data(self, hct, highlights_created):
        df =hct.analyze_resource_types()
        if df.empty:
            self.options['has_highlights_created_per_resource_types'] = False
            return
        self.options['has_highlights_created_per_resource_types'] = True
        df = reset_dataframe_(df)
        columns = ['timestamp_period', 'resource_type',
                   'number_of_highlights_created']
        df = df[columns]
        build_events_data_by_resource_type(df, highlights_created)

    def build_highlights_created_by_enrollment_type_data(self, hct, highlights_created):
        df = hct.analyze_enrollment_types()
        if df.empty:
            self.options['has_highlights_created_per_enrollment_types'] = False
            return
        df = reset_dataframe_(df)
        self.options['has_highlights_created_per_enrollment_types'] = True
        columns = ['timestamp_period', 'enrollment_type',
                   'number_of_highlights_created']
        df = df[columns]
        build_events_data_by_enrollment_type(df, highlights_created)
