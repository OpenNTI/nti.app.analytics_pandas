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

from nti.app.analytics_pandas.views.videos import VideosTimeseriesReportView

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestVideoView(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_video_report(self):
        response = self.testapp.post_json('/dataserver2/pandas_reports/HighlightsReport',
                                          {
                                              'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                              'start_date': '2015-02-01',
                                              'end_date': '2015-02-28'
                                          },
                                          extra_environ=self._make_extra_environ())
        assert_that(response,
                    has_property('content_type', 'application/pdf'))


class TestVideoOptions(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_video__report(self):
        request = DummyRequest(params={'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                       'start_date': '2015-02-01',
                                       'end_date': '2015-02-28'})
        view = VideosTimeseriesReportView(request=request)
        options = view()
        assert_that(options, is_not(none()))
        assert_that(options,
                    has_entries('course_ids', is_([388]),
                                'has_video_events_data', True,
                                'has_videos_watched', True,
                                'has_videos_skipped', True,
                                'has_videos_watched_per_enrollment_types', True,
                                'has_videos_skipped_per_enrollment_types', True))
        assert_that(options,
                    has_entries('data',
                                has_entries('video_events', is_not(none()),
                                            'video_events', 
                                            has_entries('num_rows_video_event_type', 35,
                                                        'by_video_event_type_chart', is_not(none()),
                                                        'tuples_video_event_type', (),
                                                        'num_rows', 25,
                                                        'events_chart', is_not(none()),
                                                        'tuples', (),
                                                        'column_name', u'Videos Watched',
                                                        'num_rows_skip', 10,
                                                        'column_name_skip', u'Videos Skipped',
                                                        'events_chart_skip', is_not(none()),
                                                        'tuples_skip', (),
                                                        'videos_watched', is_not(none()),
                                                        'videos_skipped', is_not(none())
                                                        )
                                            )
                                )
                    )
