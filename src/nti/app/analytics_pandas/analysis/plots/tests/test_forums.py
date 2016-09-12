#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.forums import ForumsEventsTimeseries
from nti.analytics_pandas.analysis.forums import ForumsCreatedTimeseries
from nti.analytics_pandas.analysis.forums import ForumCommentLikesTimeseries
from nti.analytics_pandas.analysis.forums import ForumsCommentsCreatedTimeseries
from nti.analytics_pandas.analysis.forums import ForumCommentFavoritesTimeseries

from nti.analytics_pandas.analysis.plots.forums import ForumsEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.forums import ForumsCreatedTimeseriesPlot
from nti.analytics_pandas.analysis.plots.forums import ForumCommentLikesTimeseriesPlot
from nti.analytics_pandas.analysis.plots.forums import ForumsCommentsCreatedTimeseriesPlot
from nti.analytics_pandas.analysis.plots.forums import ForumCommentFavoritesTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestForumsCreatedPlot(AnalyticsPandasTestBase):

	def test_explore_events_forums_created(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fctp = ForumsCreatedTimeseriesPlot(fct)
		_ = fctp.explore_events()

	def test_explore_events_forums_created_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		fctp = ForumsCreatedTimeseriesPlot(fct)
		_ = fctp.explore_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_device_types_plot(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fctp = ForumsCreatedTimeseriesPlot(fct)
		_ = fctp.analyze_device_types()

	def test_empty_result(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['123']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fctp = ForumsCreatedTimeseriesPlot(fct)
		_ = fctp.analyze_device_types()
		assert_that(len(_), equal_to(0))
		_ = fctp.explore_events()
		assert_that(len(_), equal_to(0))

class TestForumCommentsCreatedPlot(AnalyticsPandasTestBase):

	def test_explore_events_forums_comments_created(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcctp = ForumsCommentsCreatedTimeseriesPlot(fcct)
		_ = fcctp.explore_events()

	def test_explore_events_forums_comments_created_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		fcctp = ForumsCommentsCreatedTimeseriesPlot(fcct)
		_ = fcctp.explore_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_device_types_forums_comments_created(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcctp = ForumsCommentsCreatedTimeseriesPlot(fcct)
		_ = fcctp.analyze_device_types()

	def test_the_most_active_users(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcctp = ForumsCommentsCreatedTimeseriesPlot(fcct)
		_ = fcctp.plot_the_most_active_users()

	def test_analyze_comments_per_section(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcctp = ForumsCommentsCreatedTimeseriesPlot(fcct)
		_ = fcctp.analyze_comments_per_section()

	def test_analyze_comments_per_section_2(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcctp = ForumsCommentsCreatedTimeseriesPlot(fcct)
		_ = fcctp.analyze_comments_per_section(period_breaks='1 day', minor_period_breaks=None)

	def test_empty_result(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['123']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcctp = ForumsCommentsCreatedTimeseriesPlot(fcct)
		_ = fcctp.analyze_comments_per_section(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))
		_ = fcctp.plot_the_most_active_users()
		assert_that(len(_), equal_to(0))
		_ = fcctp.analyze_device_types()
		assert_that(len(_), equal_to(0))
		_ = fcctp.explore_events()
		assert_that(len(_), equal_to(0))

class TestForumCommentLikesPlot(AnalyticsPandasTestBase):

	def test_analyze_forum_comment_likes(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id)
		fcltp = ForumCommentLikesTimeseriesPlot(fclt)
		_ = fcltp.analyze_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_forum_comment_likes_weekly(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		fcltp = ForumCommentLikesTimeseriesPlot(fclt)
		_ = fcltp.analyze_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_device_types(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id)
		fcltp = ForumCommentLikesTimeseriesPlot(fclt)
		_ = fcltp.analyze_device_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id)
		fcltp = ForumCommentLikesTimeseriesPlot(fclt)
		_ = fcltp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks=None)

	def test_empty_result(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['123']
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id)
		fcltp = ForumCommentLikesTimeseriesPlot(fclt)
		_ = fcltp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))
		_ = fcltp.analyze_device_types(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))
		_ = fcltp.analyze_events(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))


class TestForumCommentFavoritesPlot(AnalyticsPandasTestBase):

	def test_analyze_device_types_forum_comment_favorites(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fcft = ForumCommentFavoritesTimeseries(self.session, start_date, end_date, course_id)
		fcftp = ForumCommentFavoritesTimeseriesPlot(fcft)
		_ = fcftp.analyze_device_types()

	def test_analyze_device_types_forum_comment_favorites_weekly(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fcft = ForumCommentFavoritesTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		fcftp = ForumCommentFavoritesTimeseriesPlot(fcft)
		_ = fcftp.analyze_device_types(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_events(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fcft = ForumCommentFavoritesTimeseries(self.session, start_date, end_date, course_id)
		fcftp = ForumCommentFavoritesTimeseriesPlot(fcft)
		_ = fcftp.explore_events()

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fcft = ForumCommentFavoritesTimeseries(self.session, start_date, end_date, course_id)
		fcftp = ForumCommentFavoritesTimeseriesPlot(fcft)
		_ = fcftp.analyze_events_per_course_sections()


	def test_empty_result(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['123']
		fcft = ForumCommentFavoritesTimeseries(self.session, start_date, end_date, course_id)
		fcftp = ForumCommentFavoritesTimeseriesPlot(fcft)
		_ = fcftp.analyze_events_per_course_sections()
		assert_that(len(_), equal_to(0))
		_ = fcftp.explore_events()
		assert_that(len(_), equal_to(0))
		_ = fcftp.analyze_device_types()
		assert_that(len(_), equal_to(0))

class TestForumEventsPlot(AnalyticsPandasTestBase):

	def test_explore_all_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id)
		fcft = ForumCommentFavoritesTimeseries(self.session, start_date, end_date, course_id)
		fet = ForumsEventsTimeseries(fct, fcct, fclt, fcft)
		fetp = ForumsEventsTimeseriesPlot(fet)
		_ = fetp.explore_all_events()

	def test_explore_all_events_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		fcft = ForumCommentFavoritesTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		fet = ForumsEventsTimeseries(fct, fcct, fclt, fcft)
		fetp = ForumsEventsTimeseriesPlot(fet)
		_ = fetp.explore_all_events(period_breaks='1 week', minor_period_breaks=None)

	def test_empty_result(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['123']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id)
		fcft = ForumCommentFavoritesTimeseries(self.session, start_date, end_date, course_id)
		fet = ForumsEventsTimeseries(fct, fcct, fclt, fcft)
		fetp = ForumsEventsTimeseriesPlot(fet)
		_ = fetp.explore_all_events()
		assert_that(len(_), equal_to(0))
