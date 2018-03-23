#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.view import view_config

from nti.analytics_pandas.analysis import CourseDropsTimeseries
from nti.analytics_pandas.analysis import CourseCatalogViewsTimeseries
from nti.analytics_pandas.analysis import CourseEnrollmentsTimeseries
from nti.analytics_pandas.analysis import CourseEnrollmentsEventsTimeseries

from nti.analytics_pandas.analysis.common import reset_dataframe_

from nti.app.analytics_pandas.views import MessageFactory as _

from nti.app.analytics_pandas.views.commons import add_one_more_day
from nti.app.analytics_pandas.views.commons import get_default_start_end_date
from nti.app.analytics_pandas.views.commons import build_event_chart_data
from nti.app.analytics_pandas.views.commons import build_event_table_data
from nti.app.analytics_pandas.views.commons import build_timeseries_chart
from nti.app.analytics_pandas.views.commons import save_chart_to_temporary_file
from nti.app.analytics_pandas.views.commons import build_event_grouped_chart_data
from nti.app.analytics_pandas.views.commons import build_event_grouped_table_data
from nti.app.analytics_pandas.views.commons import get_course_id_and_name_given_ntiid
from nti.app.analytics_pandas.views.commons import build_events_data_by_sharing_type
from nti.app.analytics_pandas.views.commons import build_events_data_by_resource_type
from nti.app.analytics_pandas.views.commons import build_events_data_by_enrollment_type

from nti.app.analytics_pandas.views.mixins import AbstractReportView

logger = __import__('logging').getLogger(__name__)

@view_config(name="EnrollmentsReport")
class EnrollmentsTimeseriesReportView(AbstractReportView):

    @property
    def report_title(self):
        return _(u'Enrollments Report')

    def _build_data(self, data=_('sample enrollments report')):
        keys = self.options.keys()
        if 'has_enrollment_data' not in keys:
            self.options['has_enrollment_data'] = False
            self.options['has_enrollment_type_data'] = False
        if 'has_catalog_views_data' not in keys:
            self.options['has_catalog_views_data'] = False
        self.options['data'] = data
        return self.options

    def __call__(self):
        values = self.readInput()
        if 'start_date' and 'end_date' not in values.keys():
            values['start_date'], values['end_date'] = get_default_start_end_date()
        if "MimeType" not in values.keys():
            values["MimeType"] = 'application/vnd.nextthought.reports.enrollmenteventstimeseriescontext'
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
            cet = CourseEnrollmentsTimeseries(self.db.session,
                                          self.options['start_date'],
                                          self.options['end_date'],
                                          self.options['course_ids'] or (),
                                          period=self.options['period'])
            if not cet.dataframe.empty:
                data['enrollments'] = self.build_enrollment_data(cet)

            ccvt = CourseCatalogViewsTimeseries(self.db.session,
                                          self.options['start_date'],
                                          self.options['end_date'],
                                          self.options['course_ids'] or (),
                                          period=self.options['period'])

            if not ccvt.dataframe.empty:
                data['catalog_views'] = self.build_catalog_views_data(ccvt)

        self._build_data(data)
        return self.options

    def build_enrollment_data(self,cet):
        df = cet.analyze_events()
        if df.empty:
            self.options['has_enrollment_data'] = False
            return
        self.options['has_enrollment_data'] = True
        df = reset_dataframe_(df)
        df = df[['timestamp_period', 'number_of_enrollments']]
        enrollments = {}
        enrollments['num_rows'] = df.shape[0]
        enrollments['column_name'] = _(u'Enrollments')
        if enrollments['num_rows'] > 1:
            chart = build_timeseries_chart(df, 'Enrollments')
            enrollments['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            enrollments['events_chart'] = ()
        
        if enrollments['num_rows'] == 1:
            enrollments['tuples'] = build_event_table_data(df, column_list=('date', 'number_of_events'))
        else:
            enrollments['tuples'] = ()
        self.build_enrollment_type_data(cet, enrollments)
        return enrollments

    def build_enrollment_type_data(self, cet, enrollments):
        df = cet.analyze_enrollment_types()
        if df.empty:
            self.options['has_enrollment_type_data'] = False
            return
        df = reset_dataframe_(df)
        self.options['has_enrollment_type_data'] = True
        columns = ['timestamp_period', 'type_name',
                   'number_of_enrollments']
        df = df[columns]
        df.columns = ['timestamp_period', 'enrollment_type', 'number_of_enrollments']
        build_events_data_by_enrollment_type(df, enrollments)

    def build_catalog_views_data(self, ccvt):
        df = ccvt.analyze_events()
        if df.empty:
            self.options['has_catalog_views_data'] = False
            return
        self.options['has_catalog_views_data'] = True
        df = reset_dataframe_(df)
        df = df[['timestamp_period', 'number_of_unique_users', 'number_of_course_catalog_views', 'ratio']]
        catalog_views = {}
        catalog_views['num_rows'] = df.shape[0]
        catalog_views['column_name'] = _(u'Catalog Views')
        if catalog_views['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_course_catalog_views',
                                           'Catalog Views')
            catalog_views['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            catalog_views['events_chart'] = ()
        
        if catalog_views['num_rows'] == 1:
            catalog_views['tuples'] = build_event_table_data(df)
        else:
            catalog_views['tuples'] = ()
        return catalog_views


