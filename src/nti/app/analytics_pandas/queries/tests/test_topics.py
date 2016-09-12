#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.queries.topics import QueryTopicLikes
from nti.analytics_pandas.queries.topics import QueryTopicsViewed
from nti.analytics_pandas.queries.topics import QueryTopicsCreated
from nti.analytics_pandas.queries.topics import QueryTopicFavorites

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestTopics(AnalyticsPandasTestBase):

	def test_query_topics_created_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qtc = QueryTopicsCreated(self.session)
		dataframe = qtc.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe), equal_to(219))

	def test_query_topics_created_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qtc = QueryTopicsCreated(self.session)
		dataframe = qtc.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe), equal_to(151))

	def test_query_topics_created_add_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qtc = QueryTopicsCreated(self.session)
		dataframe = qtc.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe), equal_to(151))
		new_df = qtc.add_device_type(dataframe)
		assert_that(len(dataframe.index), equal_to(len(new_df.index)))
		assert_that(new_df.columns, has_item('device_type'))

	def test_query_topics_viewed_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qtv = QueryTopicsViewed(self.session)
		dataframe = qtv.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe), equal_to(12797))

	def test_query_topics_viewed_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qtv = QueryTopicsViewed(self.session)
		dataframe = qtv.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe), equal_to(1610))

	def test_query_topics_viewed_add_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qtv = QueryTopicsViewed(self.session)
		dataframe = qtv.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe), equal_to(1610))
		new_df = qtv.add_device_type(dataframe)
		assert_that(len(dataframe.index), equal_to(len(new_df.index)))
		assert_that(new_df.columns, has_item('device_type'))

	def test_query_topic_favorites_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qtf = QueryTopicFavorites(self.session)
		dataframe = qtf.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe), equal_to(14))

	def test_query_topic_favorites_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qtf = QueryTopicFavorites(self.session)
		dataframe = qtf.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe), equal_to(6))

	def test_query_topic_favorites_add_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qtf = QueryTopicFavorites(self.session)
		dataframe = qtf.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe), equal_to(6))
		new_df = qtf.add_device_type(dataframe)
		assert_that(len(dataframe.index), equal_to(len(new_df.index)))
		assert_that(new_df.columns, has_item('device_type'))

	def test_query_topic_likes_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qtl = QueryTopicLikes(self.session)
		dataframe = qtl.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe), equal_to(1))

	def test_query_topic_likes_by_period_of_time_and_course_id(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qtl = QueryTopicLikes(self.session)
		dataframe = qtl.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe), equal_to(0))

	def test_query_topic_likes_add_device_type(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qtl = QueryTopicLikes(self.session)
		dataframe = qtl.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe), equal_to(0))
		new_df = qtl.add_device_type(dataframe)
		assert_that(new_df, equal_to(None))
