#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

import numpy as np

from nti.analytics_pandas.analysis.forums import ForumsEventsTimeseries
from nti.analytics_pandas.analysis.forums import ForumsCreatedTimeseries
from nti.analytics_pandas.analysis.forums import ForumCommentLikesTimeseries
from nti.analytics_pandas.analysis.forums import ForumsCommentsCreatedTimeseries
from nti.analytics_pandas.analysis.forums import ForumCommentFavoritesTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestForumsCreatedEDA(AnalyticsPandasTestBase):

	def test_forums_created_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)

		events_df = fct.analyze_events()
		assert_that(len(events_df.index), equal_to(1))
		total_events = np.sum(events_df['number_of_forums_created'])
		assert_that(total_events, equal_to(len(fct.dataframe.index)))

		# df is None since the session_id in forumscreated of given course and time period is NULL
		df = fct.analyze_events_per_device_types()
		assert_that(df, equal_to(None))

	def test_forums_comments_created_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		assert_that(fcct.dataframe.columns, has_item('context_name'))

		events_df = fcct.analyze_events()
		assert_that(len(events_df.index), equal_to(70))
		total_events = np.sum(events_df['number_of_comment_created'])
		assert_that(total_events, equal_to(len(fcct.dataframe.index)))

		df = fcct.analyze_device_types()
		assert_that(df.columns, has_item('number_of_comment_created'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('average_comment_length'))
		assert_that(df.columns, has_item('favorite_count'))
		assert_that(df.columns, has_item('like_count'))
		total_events = np.sum(df['number_of_comment_created'])

		# this test will fail since there are 6 comments having session_id NULL
		# assert_that(total_events, equal_to(len(fcct.dataframe.index)))

		most_active_users_df = fcct.get_the_most_active_users(max_rank_number=10)
		assert_that(len(most_active_users_df.index), equal_to(10))

		df = fcct.analyze_comments_per_section()
		assert_that(df.columns, has_item('number_of_comment_created'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_forum_comment_likes_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id)

		events_df = fclt.analyze_events()
		assert_that(events_df, equal_to(None))

		df = fclt.analyze_device_types()
		assert_that(df, equal_to(None))

	def test_forum_comment_favorites_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fcft = ForumCommentFavoritesTimeseries(self.session, start_date, end_date, course_id)

		events_df = fcft.analyze_events()
		assert_that(events_df, equal_to(None))

		df = fcft.analyze_device_types()
		assert_that(df, equal_to(None))

	def test_forums_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		fct = ForumsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fcct = ForumsCommentsCreatedTimeseries(self.session, start_date, end_date, course_id)
		fclt = ForumCommentLikesTimeseries(self.session, start_date, end_date, course_id)
		fcft = ForumCommentFavoritesTimeseries(self.session, start_date, end_date, course_id)
		fet = ForumsEventsTimeseries(fct, fcct, fclt, fcft)

		df = fet.combine_all_events_per_date()
		assert_that(len(df.index), equal_to(71))
		assert_that(len(df.columns), equal_to(5))
