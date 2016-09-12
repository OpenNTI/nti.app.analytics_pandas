#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.analysis.notes import NoteLikesTimeseries
from nti.analytics_pandas.analysis.notes import NotesViewTimeseries
from nti.analytics_pandas.analysis.notes import NotesEventsTimeseries
from nti.analytics_pandas.analysis.notes import NotesCreationTimeseries
from nti.analytics_pandas.analysis.notes import NoteFavoritesTimeseries
from nti.analytics_pandas.analysis.plots.notes import NotesViewTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NotesEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NotesCreationTimeseriesPlot

from nti.analytics_pandas.analysis.forums import ForumsEventsTimeseries
from nti.analytics_pandas.analysis.forums import ForumsCreatedTimeseries
from nti.analytics_pandas.analysis.forums import ForumCommentLikesTimeseries
from nti.analytics_pandas.analysis.forums import ForumsCommentsCreatedTimeseries
from nti.analytics_pandas.analysis.forums import ForumCommentFavoritesTimeseries

from nti.analytics_pandas.analysis.plots.forums import ForumsEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.forums import ForumsCreatedTimeseriesPlot
from nti.analytics_pandas.analysis.plots.forums import ForumCommentLikesTimeseriesPlot
from nti.analytics_pandas.analysis.plots.forums import ForumsCommentsCreatedTimeseriesPlot

from nti.analytics_pandas.analysis.topics import TopicLikesTimeseries
from nti.analytics_pandas.analysis.topics import TopicViewsTimeseries
from nti.analytics_pandas.analysis.topics import TopicsEventsTimeseries
from nti.analytics_pandas.analysis.topics import TopicsCreationTimeseries
from nti.analytics_pandas.analysis.topics import TopicFavoritesTimeseries

from nti.analytics_pandas.analysis.plots.topics import TopicViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.topics import TopicLikesTimeseriesPlot
from nti.analytics_pandas.analysis.plots.topics import TopicsEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.topics import TopicsCreationTimeseriesPlot
from nti.analytics_pandas.analysis.plots.topics import TopicFavoritesTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestNotesCreationPlot(AnalyticsPandasTestBase):

	def test_explore_events_notes_creation(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.explore_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_device_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.analyze_device_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_resource_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.analyze_resource_types(period_breaks='1 day', minor_period_breaks=None)

	def test_plot_most_active_users(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.plot_the_most_active_users()

	def test_analyze_sharing_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.analyze_sharing_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		_ = nctp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks=None)

class TestNoteViewsPlot(AnalyticsPandasTestBase):

	def test_analyze_total_events_based_on_sharing_type(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.analyze_total_events_based_on_sharing_type(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_total_events_based_on_device_type(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.analyze_total_events_based_on_device_type(period_breaks='1 day', minor_period_breaks=None)


	def test_plot_most_active_users(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.plot_the_most_active_users()

	def test_explore_events(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.explore_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_total_events_based_on_resource_type(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.analyze_total_events_based_on_resource_type(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_unique_events_based_on_sharing_type(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.analyze_unique_events_based_on_sharing_type(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_total_events_per_course_sections(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		_ = nvtp.analyze_total_events_per_course_sections(period_breaks='1 day', minor_period_breaks=None)

class TestNotesEventsPlot(AnalyticsPandasTestBase):

	def test_notes_events(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)

		net = NotesEventsTimeseries(nct, nvt, nlt, nft)
		netp = NotesEventsTimeseriesPlot(net)
		_ = netp.explore_all_events(period_breaks='1 day', minor_period_breaks=None)

class TestForumsEventsTimeseriesPlot(AnalyticsPandasTestBase):

	def test_explore_all_events(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id)
		fcft = ForumCommentFavoritesTimeseries(self.session, start_date, end_date, course_id)
		fet = ForumsEventsTimeseries(fct, fcct, fclt, fcft)
		fetp = ForumsEventsTimeseriesPlot(fet)
		_ = fetp.explore_all_events(period_breaks='1 day', minor_period_breaks=None)

class TestForumCommentsCreatedPlot(AnalyticsPandasTestBase):

	def test_explore_events_forums_comments_created(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcctp = ForumsCommentsCreatedTimeseriesPlot(fcct)
		_ = fcctp.explore_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_device_types_forums_comments_created(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcctp = ForumsCommentsCreatedTimeseriesPlot(fcct)
		_ = fcctp.analyze_device_types(period_breaks='1 day', minor_period_breaks=None)

	def test_the_most_active_users(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcctp = ForumsCommentsCreatedTimeseriesPlot(fcct)
		_ = fcctp.plot_the_most_active_users()

	def test_analyze_comments_per_section_2(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcctp = ForumsCommentsCreatedTimeseriesPlot(fcct)
		_ = fcctp.analyze_comments_per_section(period_breaks='1 day', minor_period_breaks=None)

class TestForumCommentLikesPlot(AnalyticsPandasTestBase):

	def test_analyze_forum_comment_likes(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id)
		fcltp = ForumCommentLikesTimeseriesPlot(fclt)
		_ = fcltp.analyze_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_device_types_forum_comment_likes(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id)
		fcltp = ForumCommentLikesTimeseriesPlot(fclt)
		_ = fcltp.analyze_device_types(period_breaks='1 day', minor_period_breaks=None)

class TestForumsCreatedPlot(AnalyticsPandasTestBase):

	def test_explore_events_forums_created(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fctp = ForumsCreatedTimeseriesPlot(fct)
		_ = fctp.explore_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_device_types_plot(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fctp = ForumsCreatedTimeseriesPlot(fct)
		_ = fctp.analyze_device_types(period_breaks='1 day', minor_period_breaks=None)

class TestTopicsEventsPlot(AnalyticsPandasTestBase):

	def test_topics_events(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tct = TopicsCreationTimeseries(self.session, start_date, end_date, course_id)
		tvt = TopicViewsTimeseries(self.session, start_date, end_date, course_id)
		tlt = TopicLikesTimeseries(self.session, start_date, end_date, course_id)
		tft = TopicFavoritesTimeseries(self.session, start_date, end_date, course_id)
		tet = TopicsEventsTimeseries(tct, tvt, tlt, tft)
		tetp = TopicsEventsTimeseriesPlot(tet)
		_ = tetp.explore_all_events(period_breaks='1 day', minor_period_breaks=None)

class TestTopicsCreationPlot(AnalyticsPandasTestBase):

	def test_explore_events_topics_created(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tct = TopicsCreationTimeseries(self.session, start_date, end_date, course_id)
		tctp = TopicsCreationTimeseriesPlot(tct)
		_ = tctp.explore_events(period_breaks='1 day', minor_period_breaks=None)

class TestTopicViewsPlot(AnalyticsPandasTestBase):

	def test_explore_events_topics_viewed(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tvt = TopicViewsTimeseries(self.session, start_date, end_date, course_id)
		tvtp = TopicViewsTimeseriesPlot(tvt)
		_ = tvtp.explore_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_device_type(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tvt = TopicViewsTimeseries(self.session, start_date, end_date, course_id)
		tvtp = TopicViewsTimeseriesPlot(tvt)
		_ = tvtp.analyze_device_types(period_breaks='1 day', minor_period_breaks=None)

	def test_plot_the_most_active_users(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tvt = TopicViewsTimeseries(self.session, start_date, end_date, course_id)
		tvtp = TopicViewsTimeseriesPlot(tvt)
		_ = tvtp.plot_the_most_active_users()

class TestTopicLikesPlot(AnalyticsPandasTestBase):

	def test_explore_events_topics_viewed(self):
		start_date = '2015-10-05'
		end_date = '2015-10-27'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tlt = TopicLikesTimeseries(self.session, start_date, end_date, course_id)
		tltp = TopicLikesTimeseriesPlot(tlt)
		_ = tltp.explore_events(period_breaks='1 day', minor_period_breaks=None)

class TestTopicFavoritesPlot(AnalyticsPandasTestBase):

	def test_explore_events_topics_viewed(self):
		start_date = '2015-10-05'
		end_date = '2015-10-27'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tft = TopicFavoritesTimeseries(self.session, start_date, end_date, course_id)
		tftp = TopicFavoritesTimeseriesPlot(tft)
		_ = tftp.explore_events(period_breaks='1 day', minor_period_breaks=None)
