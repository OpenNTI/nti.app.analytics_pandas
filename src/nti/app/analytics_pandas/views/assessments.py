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
        if 'has_assignments_taken' not in keys:
            self.options['has_assignments_taken'] = False
            self.options['has_assignments_taken_per_enrollment_type'] = False
        if 'has_self_assessment_taken' not in keys:
            self.options['has_self_assessment_taken'] = False
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
            avt = AssignmentViewsTimeseries(self.db.session,
                                        self.options['start_date'],
                                        self.options['end_date'],
                                        self.options['course_ids'] or (),
                                        period=self.options['period'])
            att = AssignmentsTakenTimeseries(self.db.session,
                                        self.options['start_date'],
                                        self.options['end_date'],
                                        self.options['course_ids'] or (),
                                        period=self.options['period'])
            savt = SelfAssessmentViewsTimeseries(self.db.session,
                                        self.options['start_date'],
                                        self.options['end_date'],
                                        self.options['course_ids'] or (),
                                        period=self.options['period'])
            satt = SelfAssessmentsTakenTimeseries(self.db.session,
                                        self.options['start_date'],
                                        self.options['end_date'],
                                        self.options['course_ids'] or (),
                                        period=self.options['period'])
            aet = AssessmentEventsTimeseries(avt, att, savt, satt)
            data['assessment_events'] = self.build_assessment_events_data(aet)
            data['assignments_taken'] = self.build_graded_assignment_taken_data(att)
            data['self_assessment_taken'] = self.build_self_assessment_taken_data(satt)
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

    def build_graded_assignment_taken_data(self, att):
        df = att.analyze_events()
        df = reset_dataframe_(df)
        if df.empty:
            self.options['has_assignments_taken'] = False
            return
        assignments = {}
        self.options['has_assignments_taken'] = True
        assignments['num_rows'] = df.shape[0]
        assignments['column_name'] = _(u'Assignments Taken')
        if assignments['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_assignments_taken',
                                           'Assignments Taken')
            assignments['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            assignments['events_chart'] = ()
        
        if assignments['num_rows'] == 1:
            columns = ('date', 'number_of_events', 'number_of_unique_users','ratio')
            assignments['tuples'] = build_event_table_data(df, columns)
        else:
            assignments['tuples'] = ()
        self.build_graded_assignment_taken_by_enrollment_type_data(att, assignments)
        return assignments

    def build_graded_assignment_taken_by_enrollment_type_data(self, att, assignments):
        df = att.analyze_events_group_by_enrollment_type()
        df = reset_dataframe_(df)
        if df.empty:
            self.options['has_assignments_taken_per_enrollment_type'] = False
            return
        self.options['has_assignments_taken_per_enrollment_type'] = True
        columns = ['timestamp_period', 'enrollment_type',
                   'number_assignments_taken']
        df = df[columns]
        build_events_data_by_enrollment_type(df, assignments)
             

    def build_self_assessment_taken_data(self, satt):
        df = satt.analyze_events()
        df = reset_dataframe_(df)
        if df.empty:
            self.options['has_self_assessment_taken'] = False
            return
        self_assessment = {}
        self.options['has_self_assessment_taken'] = True
        self_assessment['num_rows'] = df.shape[0]
        self_assessment['column_name'] = _(u'Self Assessments Taken')
        if self_assessment['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_self_assessments_taken',
                                           'Self Assessments Taken')
            self_assessment['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            self_assessment['events_chart'] = ()
        
        if self_assessment['num_rows'] == 1:
            columns = ('date', 'number_of_events', 'number_of_unique_users','ratio')
            self_assessment['tuples'] = build_event_table_data(df, columns)
        else:
            self_assessment['tuples'] = ()
        return self_assessment
