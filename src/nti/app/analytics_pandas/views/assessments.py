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

from nti.analytics_pandas.analysis import AssessmentEventsTimeseries
from nti.analytics_pandas.analysis import AssignmentViewsTimeseries
from nti.analytics_pandas.analysis import AssignmentsTakenTimeseries
from nti.analytics_pandas.analysis import SelfAssessmentViewsTimeseries
from nti.analytics_pandas.analysis import SelfAssessmentsTakenTimeseries

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

@view_config(name="AssessmentsReport")
class AssessmentsTimeseriesReportView(AbstractReportView):

    @property
    def report_title(self):
        return _(u'Assessments Report')

    def _build_data(self, data=_('sample assessments report')):
        keys = self.options.keys()
        if 'has_assessment_event_data' not in keys:
            self.options['has_assessment_event_data'] = False
        self.options['data'] = data
        return self.options

    def __call__(self):
        values = self.readInput()
        if "MimeType" not in values.keys():
            values["MimeType"] = 'application/vnd.nextthought.reports.assessmenteventstimeseriescontext'
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
            aet = AssessmentEventsTimeseries(self.db.session,
                                        self.options['start_date'],
                                        self.options['end_date'],
                                        self.options['course_ids'] or (),
                                        period=self.options['period'])
            if not aet.dataframe.empty:
                self.build_assessment_events_data(aet)
                data['assessment_events'] = self.build_assessment_events_data(aet)
        self._build_data(data)
        return self.options

    def build_assessment_events_data(self, aet):
        assessment_events = {}
        df = aet.combine_events()
        if df.empty:
            self.options['has_assessment_event_data'] = False
            return
        self.options['has_assessment_event_data'] = True
        df = reset_dataframe_(df)
        columns = ['timestamp_period', 'event_type', 'total_events']
        df = df[columns]
        df['timestamp_period'] = df['timestamp_period'].astype(str)
        timestamp_num = len(df['timestamp_period'].unique())
        assessment_events['num_rows'] = df.shape[0]
        assessment_events['column_name'] = _(u'Total Events')
        if assessment_events['num_rows'] > 1 and timestamp_num > 1:
            chart = build_event_grouped_chart_data(df, 'event_type')
            assessment_events['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            assessment_events['events_chart'] = ()
            
        if assessment_events['num_rows'] == 1 or timestamp_num == 1:
            assessment_events['tuples'] = build_event_grouped_table_data(df)
            assessment_events['assessment_col'] = 'Assessment Events'
        else:
            assessment_events['tuples'] = ()
        return assessment_events
