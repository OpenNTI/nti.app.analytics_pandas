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

from nti.app.analytics_pandas.views.forums import ForumsTimeseriesReportView

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestForumsView(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_forum_report(self):
        response = self.testapp.post_json('/dataserver2/pandas_reports/ForumsReport',
                                          {
                                              'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                              'start_date': '2015-01-01',
                                              'end_date': '2015-05-31'
                                          },
                                          extra_environ=self._make_extra_environ())
        assert_that(response,
                    has_property('content_type', 'application/pdf'))


class TestForumOptions(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_forum_report(self):
        request = DummyRequest(params={'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                       'start_date': '2015-01-01',
                                       'end_date': '2015-05-31'})
        view = ForumsTimeseriesReportView(request=request)
        options = view()
        assert_that(options, is_not(none()))
        assert_that(options,
                    has_entries('course_ids', is_([388]),
                                'has_forums_created_data', True,
                                'has_forum_comments_created_data', True,
                                'has_forum_comments_created_per_enrollment_types', True))
        assert_that(options,
                    has_entries('data',
                                has_entries('forums_created', is_not(none()),
                                            'forums_created', 
                                            has_entries('num_rows', 1,
                                                        'events_chart', (),
                                                        'tuples', is_not(none()),
                                                        'column_name', u'Forums Created'),
                                            'forum_comments_created', is_not(none()),
                                            'forum_comments_created', 
                                            has_entries('num_rows', 70,
                                                        'events_chart', is_not(none()),
                                                        'tuples', (),
                                                        'column_name', u'Forum Comments')
                                            )
                                )
                    )
    
    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_forum_report_one_day(self):
        request = DummyRequest(params={'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                       'start_date': '2015-01-12',
                                       'end_date': '2015-01-12'})
        view = ForumsTimeseriesReportView(request=request)
        options = view()
        assert_that(options, is_not(none()))
        assert_that(options,
                    has_entries('course_ids', is_([388]),
                                'has_forums_created_data', True,
                                'has_forum_comments_created_data', True,
                                'has_forum_comments_created_per_enrollment_types', True))
        assert_that(options,
                    has_entries('data',
                                has_entries('forums_created', is_not(none()),
                                            'forums_created', 
                                            has_entries('num_rows', 1,
                                                        'events_chart', (),
                                                        'tuples', is_not(none()),
                                                        'column_name', u'Forums Created'),
                                            'forum_comments_created', is_not(none()),
                                            'forum_comments_created', 
                                            has_entries('num_rows', 1,
                                                        'events_chart', (),
                                                        'tuples', is_not(none()),
                                                        'column_name', u'Forum Comments')
                                            )
                                )
                    )
        