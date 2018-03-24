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

from nti.app.analytics_pandas.views.topics import TopicsTimeseriesReportView

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestTopicView(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_topic_report(self):
        response = self.testapp.post_json('/dataserver2/pandas_reports/BookmarksReport',
                                          {
                                              'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                              'start_date': '2015-01-01',
                                              'end_date': '2015-01-31'
                                          },
                                          extra_environ=self._make_extra_environ())
        assert_that(response,
                    has_property('content_type', 'application/pdf'))


class TestTopicOptions(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_topic_report(self):
        request = DummyRequest(params={'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                       'start_date': '2015-01-01',
                                       'end_date': '2015-01-31'})
        view = TopicsTimeseriesReportView(request=request)
        options = view()
        assert_that(options, is_not(none()))
        assert_that(options,
                    has_entries('course_ids', is_([388]),
                                'has_topics_created_data', True,
                                'has_topic_views_data', True,
                                'has_topic_likes_data', False,
                                'has_topic_favorites_data', False))
        assert_that(options,
                    has_entries('data',
                                has_entries('topics_created', is_not(none()),
                                            'topics_created', 
                                            has_entries('num_rows', 2,
                                                        'events_chart', is_not(none()),
                                                        'tuples', is_not(none()),
                                                        'column_name', u'Topics Created'),
                                            'topics_viewed', is_not(none()),
                                            'topics_viewed', 
                                            has_entries('num_rows', 20,
                                                        'events_chart', is_not(none()),
                                                        'tuples', is_not(none()),
                                                        'column_name', u'Topics Viewed')
                                            )
                                )
                    )