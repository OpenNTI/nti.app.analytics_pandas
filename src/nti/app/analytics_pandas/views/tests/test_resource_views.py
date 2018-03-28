#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import has_property

from pyramid.testing import DummyRequest

from nti.app.analytics_pandas.tests import PandasReportsLayerTest

from nti.app.analytics_pandas.views.resource_views import ResourceViewsTimeseriesReportView

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestResourceViewsView(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_resource_views_report(self):
        response = self.testapp.post_json('/dataserver2/pandas_reports/ResourceViewsReport',
                                          {
                                              'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                              'start_date': '2015-03-01',
                                              'end_date': '2015-03-31'
                                          },
                                          extra_environ=self._make_extra_environ())
        assert_that(response,
                    has_property('content_type', 'application/pdf'))


class TestResourceViewsOptions(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_resource_views_report(self):
        request = DummyRequest(params={'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                       'start_date': '2015-03-01',
                                       'end_date': '2015-03-31'})
        view = ResourceViewsTimeseriesReportView(request=request)
        options = view()
        assert_that(options, is_not(none()))
        assert_that(options,
                    has_entries('course_ids', is_([388]),
                                'has_resource_view_events', True,
                                'has_resource_views_per_enrollment_types', True,
                                'has_resource_views_per_device_types', True,
                                'has_resource_views_per_resource_types', True))
        assert_that(options,
                    has_entries('data',
                                has_entries('resources_viewed', is_not(none()),
                                            'resources_viewed', 
                                            has_entries('num_rows', 30,
                                                        'events_chart', is_not(none()),
                                                        'tuples', (),
                                                        'column_name', u'Resource Viewed')
                                            )
                                )
                    )

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_resource_views_report_one_day(self):
        request = DummyRequest(params={'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                       'start_date': '2015-04-21',
                                       'end_date': '2015-04-21'})
        view = ResourceViewsTimeseriesReportView(request=request)
        options = view()
        assert_that(options, is_not(none()))
        assert_that(options,
                    has_entries('course_ids', is_([388]),
                                'has_resource_view_events', True,
                                'has_resource_views_per_enrollment_types', True,
                                'has_resource_views_per_device_types', True,
                                'has_resource_views_per_resource_types', True))
        assert_that(options,
                    has_entries('data',
                                has_entries('resources_viewed', is_not(none()),
                                            'resources_viewed', 
                                            has_entries('num_rows', 1,
                                                        'events_chart', (),
                                                        'tuples', is_not(none()),
                                                        'column_name', u'Resource Viewed')
                                            )
                                )
                    )

