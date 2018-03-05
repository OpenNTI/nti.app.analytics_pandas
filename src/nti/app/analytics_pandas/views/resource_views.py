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

from nti.analytics_pandas.analysis import ResourceViewsTimeseries

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
from nti.app.analytics_pandas.views.commons import build_events_created_by_device_type
from nti.app.analytics_pandas.views.commons import build_events_created_by_enrollment_type

from nti.app.analytics_pandas.views.mixins import AbstractReportView

logger = __import__('logging').getLogger(__name__)


@view_config(name="ResourceViewsReport")
class ResourceViewsTimeseriesReportView(AbstractReportView):

    @property
    def report_title(self):
        return _(u'Resource Views Report')

    def _build_data(self, data=_('sample resource views report')):
        keys = self.options.keys()
        if 'has_resource_view_events' not in keys:
            self.options['has_resource_view_events'] = False

        if 'has_resource_views_per_enrollment_types' not in keys:
            self.options['has_resource_views_per_enrollment_types'] = False

        if 'has_resource_views_per_device_types' not in keys:
            self.options['has_resource_views_per_device_types'] = False

        if 'has_resource_views_per_resource_types' not in keys:
            self.options['has_resource_views_per_resource_types'] = False

        if 'has_resource_view_users' not in keys:
            self.options['has_resource_view_users'] = False

        self.options['data'] = data
        return self.options

    def __call__(self):
        values = self.readInput()
        if "MimeType" not in values.keys():
            values["MimeType"] = 'application/vnd.nextthought.reports.resourceviewstimeseriescontext'
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
            rvt = ResourceViewsTimeseries(self.db.session,
                                          self.options['start_date'],
                                          self.options['end_date'],
                                          self.options['course_ids'] or (),
                                          period=self.options['period'])
            if not rvt.dataframe.empty:
                self.options['has_resource_view_events'] = True
                data['resources_viewed'] = self.build_resources_viewed_data(rvt)

        values = self.readInput()
        self._build_data(data)
        return self.options

    def build_resources_viewed_data(self, rvt):
        resource_views = {}
        dataframes = get_data(rvt)
        resource_views['num_rows'] = dataframes['df_by_timestamp'].shape[0]
        resource_views['column_name'] = u'Resource Viewed'
        # Building chart Data
        if resource_views['num_rows'] > 1:
            chart = build_event_chart_data(dataframes['df_by_timestamp'],
                                           'number_of_resource_views',
                                           'Resource Viewed')
            resource_views['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            resource_views['events_chart'] = False
        
        if resource_views['num_rows'] == 1:
            columns =dataframes['df_by_timestamp'].columns.tolist()
            resource_views['tuples'] = build_event_table_data(
                dataframes['df_by_timestamp'], columns)
        else:
            resource_views['tuples'] = False
        
        self.build_resources_viewed_by_type_data(rvt, resource_views)

        if 'df_per_device_types' in dataframes.keys():
            self.options['has_resource_views_per_device_types'] = True
            self.build_resources_viewed_by_device_type_data(
                dataframes['df_per_device_types'], resource_views
            )
        else:
            self.options['has_resource_views_per_device_types'] = False

        if 'df_per_enrollment_type' in dataframes.keys():
            self.options['has_resource_views_per_enrollment_types'] = True
            self.build_resources_viewed_by_enrollment_type_data(
                dataframes['df_per_enrollment_type'], resource_views
            )
        else:
            self.options['has_resource_views_per_enrollment_types'] = False

        self.get_the_n_most_viewed_resources(rvt, resource_views, 10)
        return resource_views

    def build_resources_viewed_by_type_data(self, rvt, resource_views):
        df = rvt.analyze_events_based_on_resource_type()
        if not df.empty:
            self.options['has_resource_views_per_resource_types'] = True
        else:
            return
        df = reset_dataframe_(df)
        columns = ['timestamp_period', 'resource_type',
                   'number_of_resource_views']
        df = df[columns]
        df['timestamp_period'] = df['timestamp_period'].astype(str)
        timestamp_num = len(np.unique(df['timestamp_period'].values.ravel()))
        resource_views['num_rows_resource_type'] = df.shape[0]
        
        if resource_views['num_rows_resource_type'] > 1 and timestamp_num > 1:
            chart = build_event_grouped_chart_data(df, 'resource_type')
            resource_views['by_resource_type_chart'] = save_chart_to_temporary_file(chart)
        else:
            resource_views['by_resource_type_chart'] = False
            
        if resource_views['num_rows_resource_type'] == 1 or timestamp_num == 1:
            resource_views['tuples_resource_type'] = build_event_grouped_table_data(df)
            resource_views['resource_col'] = 'Resource Type'
        else:
            resource_views['tuples_resource_type'] = False

    def build_resources_viewed_by_device_type_data(self, df, resource_views):
        columns = ['timestamp_period', 'device_type',
                   'number_of_resource_views']
        df = df[columns]
        build_events_created_by_device_type(df, resource_views)

    def build_resources_viewed_by_enrollment_type_data(self, df, resource_views):
        columns = ['timestamp_period', 'enrollment_type',
                   'number_of_resource_views']
        df = df[columns]
        build_events_created_by_enrollment_type(df, resource_views)

    def get_the_n_most_viewed_resources(self, rvt, resource_views, max_rank_number=10):
        df = rvt.get_the_most_viewed_resources(max_rank_number)
        columns = ['number_of_views', 'resource_display_name', 'resource_type']
        df = df[columns]
        tuples = iternamedtuples(df, columns)
        resource_views['n_most_viewed_resources'] = tuples
