#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import none
from hamcrest import is_
from hamcrest import is_not
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import greater_than_or_equal_to

from pyramid.testing import DummyRequest

from nti.app.analytics_pandas.tests import PandasReportsLayerTest

from nti.app.analytics_pandas.views.bookmarks import BookmarksTimeseriesReportView

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestBookmarksView(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_bookmarks_report(self):
        response = self.testapp.post_json('/dataserver2/pandas_reports/BookmarksReport',
                                          {
                                              'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                              'start_date' : '2015-01-01',
                                              'end_date' : '2015-05-31'
                                          },
                                          extra_environ=self._make_extra_environ())
        assert_that(response,
                    has_property('content_type', 'application/pdf'))

class TestBookmarkOptions(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_assessment_report(self):
        request = DummyRequest(params={'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113', 
                                       'start_date' : '2015-01-01',
                                       'end_date' : '2015-05-31'})
        view = BookmarksTimeseriesReportView(request=request)
        options = view()
        assert_that(options, is_not(none()))
        assert_that(options['course_ids'][0], is_(388))
        assert_that(options['has_bookmarks_created_data'], is_(True))
        assert_that(options['has_bookmarks_created_per_resource_types'], is_(True))
        assert_that(options['has_bookmarks_created_per_enrollment_types'], is_(True))
        assert_that(options['data'], is_not(none()))
        assert_that(options['data']['bookmarks_created'], is_not(none()))
        assert_that(options['data']['bookmarks_created']['num_rows'], is_(20))
        assert_that(options['data']['bookmarks_created']['events_chart'], is_not(none()))
        assert_that(options['data']['bookmarks_created']['tuples'], is_(()))
