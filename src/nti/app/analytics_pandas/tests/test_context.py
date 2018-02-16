#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import equal_to
from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import contains_inanyorder

from nti.app.analytics_pandas.tests import AppAnalyticsTestBase

from nti.app.analytics_pandas.views.assessments import AssessmentsEventsTimeseriesContext

from nti.app.analytics_pandas.views.bookmarks import BookmarksTimeseriesContext

from nti.app.analytics_pandas.views.enrollments import EnrollmentTimeseriesContext

from nti.app.analytics_pandas.views.forums import ForumsTimeseriesContext

from nti.app.analytics_pandas.views.highlights import HighlightsTimeseriesContext

from nti.app.analytics_pandas.views.notes import NoteEventsTimeseriesContext

from nti.app.analytics_pandas.views.resource_views import ResourceViewsTimeseriesContext

from nti.app.analytics_pandas.views.social import SocialTimeseriesContext

from nti.app.analytics_pandas.views.tests import _build_sample_context

from nti.app.analytics_pandas.views.topics import TopicsTimeseriesContext

from nti.app.analytics_pandas.views.videos import VideosTimeseriesContext

from nti.externalization.externalization import to_external_object
from nti.externalization.externalization import StandardExternalFields

CLASS = StandardExternalFields.CLASS
MIMETYPE = StandardExternalFields.MIMETYPE


class TestContextInternalization(AppAnalyticsTestBase):
    """
    Test that all externalizations of report contexts work correctly.
    Some take less parameters, so those tests are a bit different.
    """

    def _req_sample_context(self, obj, clazz):
        name = clazz.__name__
        assert_that(obj, has_entries(CLASS, is_(name),
                                     MIMETYPE, is_not(none()),
                                     "start_date", "2015-10-05",
                                     "end_date", "2015-10-20",
                                     "courses", contains_inanyorder("1068", "1096",
                                                                    "1097", "1098", "1099"),
                                     "period_breaks", "1 week",
                                     "minor_period_breaks", "1 day",
                                     "theme_bw_", equal_to(True),
                                     "number_of_most_active_user", equal_to(10),
                                     "period", "daily"))

    def test_assessment_context(self):
        context = _build_sample_context(AssessmentsEventsTimeseriesContext)
        ext_obj = to_external_object(context)
        self._req_sample_context(ext_obj, AssessmentsEventsTimeseriesContext)

    def test_bookmark_context(self):
        context = _build_sample_context(BookmarksTimeseriesContext)
        ext_obj = to_external_object(context)
        self._req_sample_context(ext_obj, BookmarksTimeseriesContext)

    def test_enrollments_context(self):
        context = _build_sample_context(EnrollmentTimeseriesContext)
        ext_obj = to_external_object(context)
        self._req_sample_context(ext_obj, EnrollmentTimeseriesContext)

    def test_forum_context(self):
        context = _build_sample_context(ForumsTimeseriesContext)
        ext_obj = to_external_object(context)
        self._req_sample_context(ext_obj, ForumsTimeseriesContext)

    def test_highlights_context(self):
        context = _build_sample_context(HighlightsTimeseriesContext)
        ext_obj = to_external_object(context)
        self._req_sample_context(ext_obj, HighlightsTimeseriesContext)

    def test_notes_context(self):
        context = _build_sample_context(NoteEventsTimeseriesContext)
        ext_obj = to_external_object(context)
        self._req_sample_context(ext_obj, NoteEventsTimeseriesContext)

    def test_resource_view_context(self):
        context = _build_sample_context(ResourceViewsTimeseriesContext)
        ext_obj = to_external_object(context)
        self._req_sample_context(ext_obj, ResourceViewsTimeseriesContext)

    def test_social_context(self):
        theme_bw_ = True
        period = "daily"
        end_date = '2015-10-20'
        start_date = '2015-10-05'
        period_breaks = '1 week'
        minor_period_breaks = '1 day'
        number_of_most_active_user = 10
        context = SocialTimeseriesContext(start_date=start_date,
                                          end_date=end_date,
                                          period_breaks=period_breaks,
                                          minor_period_breaks=minor_period_breaks,
                                          theme_bw_=theme_bw_,
                                          number_of_most_active_user=number_of_most_active_user,
                                          period=period)
        ext_obj = to_external_object(context)
        assert_that(ext_obj, 
                    has_entries(MIMETYPE, is_not(none()),
                                "start_date", "2015-10-05",
                                "end_date", "2015-10-20",
                                "period_breaks", "1 week",
                                "minor_period_breaks", "1 day",
                                "theme_bw_", equal_to(True),
                                "number_of_most_active_user", equal_to(10),
                                "period", "daily"))

    def test_topics_context(self):
        context = _build_sample_context(TopicsTimeseriesContext)
        ext_obj = to_external_object(context)
        self._req_sample_context(ext_obj, TopicsTimeseriesContext)

    def test_videos_context(self):
        context = _build_sample_context(VideosTimeseriesContext)
        ext_obj = to_external_object(context)
        self._req_sample_context(ext_obj, VideosTimeseriesContext)
