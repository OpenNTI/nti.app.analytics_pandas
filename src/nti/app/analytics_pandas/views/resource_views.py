#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.view import view_config

from nti.app.analytics_pandas.views import MessageFactory as _
from nti.app.analytics_pandas.views.commons import build_event_table_data
from nti.app.analytics_pandas.views.commons import build_event_chart_data
from nti.app.analytics_pandas.views.commons import save_chart_to_temporary_file
from nti.app.analytics_pandas.views.commons import build_event_grouped_table_data
from nti.app.analytics_pandas.views.commons import build_event_grouped_chart_data
from nti.app.analytics_pandas.views.commons import get_course_id_and_name_given_ntiid

from nti.app.analytics_pandas.views.mixins import AbstractReportView

from nti.analytics_pandas.analysis import ResourceViewsTimeseries

logger = __import__('logging').getLogger(__name__)

@view_config(name="ResourceViewsReport")
class ResourceViewsTimeseriesReportView(AbstractReportView):

    @property
    def report_title(self):
        return _(u'Resource Views')

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
            rvt = ResourceViewsTimeseries(self.db.session,
                                      self.options['start_date'],
                                      self.options['end_date'],
                                      self.options['course_ids'] or (),
                                      period=self.options['period'])
            if not rvt.dataframe.empty:
                self.options['has_resource_view_events'] = True

        self._build_data(data)
        return self.options

    def build_topic_creation_data(self, rvt):
        resource_views = {}
        dataframes = get_data(tct)
        resource_views['num_rows'] = dataframes['df_by_timestamp'].shape[0]

        # Building table data
        resource_views['tuples'] = build_event_table_data(
            dataframes['df_by_timestamp'])
        resource_views['column_name'] = u'Topics Created'

        # Building chart Data
        if resource_views['num_rows'] > 1:
            chart = build_event_chart_data(dataframes['df_by_timestamp'],
                                       'number_of_resource_views',
                                       'Topics Created')
            resource_views['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            resource_views['events_chart'] = False
        
        return resource_views