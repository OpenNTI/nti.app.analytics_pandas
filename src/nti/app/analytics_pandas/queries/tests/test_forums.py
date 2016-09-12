#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.queries.forums import QueryForumsCreated
from nti.analytics_pandas.queries.forums import QueryForumCommentLikes
from nti.analytics_pandas.queries.forums import QueryForumsCommentsCreated
from nti.analytics_pandas.queries.forums import QueryForumCommentFavorites

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestForums(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestForums, self).setUp()

	def test_query_forums_created_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qfc = QueryForumsCreated(self.session)
		dataframe = qfc.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(34))

	def test_query_forums_created_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qfc = QueryForumsCreated(self.session)
		dataframe = qfc.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(4))

	def test_query_forums_created_add_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qfc = QueryForumsCreated(self.session)
		dataframe = qfc.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(4))
		new_df = qfc.add_device_type(dataframe)
		##why None? because all session_id value in dataframe are null
		assert_that(new_df, equal_to(None))


	def test_query_forums_comments_created_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qfcc = QueryForumsCommentsCreated(self.session)
		dataframe = qfcc.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(3164))

	def test_query_forums_comments_created_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qfcc = QueryForumsCommentsCreated(self.session)
		dataframe = qfcc.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(205))

	def test_query_forums_comments_created_add_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qfcc = QueryForumsCommentsCreated(self.session)
		dataframe = qfcc.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(205))
		new_df = qfcc.add_device_type(dataframe)
		assert_that(len(dataframe.index), equal_to(len(new_df)))
		assert_that(new_df.columns, has_item('device_type'))

	def test_query_forums_comment_favorites_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qfcf = QueryForumCommentFavorites(self.session)
		dataframe = qfcf.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(0))

	def test_query_forums_comment_favorites_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qfcf = QueryForumCommentFavorites(self.session)
		dataframe = qfcf.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(0))

	def test_query_forums_comment_favorites_add_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qfcf = QueryForumCommentFavorites(self.session)
		dataframe = qfcf.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(0))
		new_df = qfcf.add_device_type(dataframe)
		assert_that(new_df, equal_to(None))

	def test_query_forums_comment_likes_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qfcl = QueryForumCommentLikes(self.session)
		dataframe = qfcl.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(78))

	def test_query_forums_comment_likes_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qfcl = QueryForumCommentLikes(self.session)
		dataframe = qfcl.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(0))

	def test_query_forums_comment_likes_add_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qfcl = QueryForumCommentLikes(self.session)
		dataframe = qfcl.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(0))
		new_df = qfcl.add_device_type(dataframe)
		assert_that(new_df, equal_to(None))
