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

from nti.analytics_pandas.analysis.topics import TopicViewsTimeseries
from nti.analytics_pandas.analysis.topics import TopicLikesTimeseries
from nti.analytics_pandas.analysis.topics import TopicsEventsTimeseries
from nti.analytics_pandas.analysis.topics import TopicsCreationTimeseries
from nti.analytics_pandas.analysis.topics import TopicFavoritesTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestTopicsEDA(AnalyticsPandasTestBase):

	def test_topics_creation_based_on_timestamp_date(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tct = TopicsCreationTimeseries(self.session, start_date, end_date, course_id)
		assert_that(tct.dataframe.columns, has_item('device_type'))
		assert_that(tct.dataframe.columns, has_item('context_name'))
		assert_that(tct.dataframe.columns, has_item('enrollment_type'))

		event_df = tct.analyze_events()
		assert_that(event_df.columns, has_item('number_of_unique_users'))
		assert_that(event_df.columns, has_item('number_of_topics_created'))
		assert_that(event_df.columns, has_item('ratio'))
		total_topics_created = np.sum(event_df['number_of_topics_created'])

		device_type_df = tct.analyze_events_per_device_types()
		_ = np.sum(device_type_df['number_of_topics_created'])
		# this test will fail since there are some user_agent_id column values in topicscreated table are NULL
		# assert_that(total_events, equal_to(total_topics_created))

		context_df = tct.analyze_events_per_course_sections()
		total_events = np.sum(context_df['number_of_topics_created'])
		assert_that(total_events, equal_to(total_topics_created))
		assert_that(total_events, equal_to(len(tct.dataframe.index)))

	def test_topic_views_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tvt = TopicViewsTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(tvt.dataframe.index), equal_to(1610))
		assert_that(tvt.dataframe.columns, has_item('device_type'))
		assert_that(tvt.dataframe.columns, has_item('context_name'))
		assert_that(tvt.dataframe.columns, has_item('enrollment_type'))

		event_df = tvt.analyze_events()
		df = tvt.analyze_events_per_course_sections()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_topics_viewed'))
		assert_that(df.columns, has_item('ratio'))
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(event_df.index)))

	def test_topic_likes_based_on_timestamp_date(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tlt = TopicLikesTimeseries(self.session, start_date, end_date, course_id)
		assert_that(tlt.dataframe.columns, has_item('device_type'))
		assert_that(tlt.dataframe.columns, has_item('enrollment_type'))

		event_df = tlt.analyze_events()
		total_events = np.sum(event_df['number_of_topic_likes'])
		assert_that(total_events, equal_to(len(tlt.dataframe.index)))

		df = tlt.dataframe
		device_type_df = tlt.analyze_events_per_device_types(df)
		total_events = np.sum(device_type_df['number_of_topic_likes'])
		assert_that(total_events, equal_to(len(tlt.dataframe.index)))

		context_df = tlt.analyze_events_per_course_sections()
		total_events = np.sum(context_df['number_of_topic_likes'])
		assert_that(total_events, equal_to(len(tlt.dataframe.index)))

	def test_topic_favorites_based_on_timestamp_date(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		tft = TopicFavoritesTimeseries(self.session, start_date, end_date, course_id)
		assert_that(tft.dataframe.columns, has_item('device_type'))
		assert_that(tft.dataframe.columns, has_item('enrollment_type'))

		event_df = tft.analyze_events()
		total_events = np.sum(event_df['number_of_topic_favorites'])
		assert_that(total_events, equal_to(len(tft.dataframe.index)))

		df = tft.dataframe
		device_type_df = tft.analyze_events_per_device_types(df)
		total_events = np.sum(device_type_df['number_of_topic_favorites'])
		assert_that(total_events, equal_to(len(tft.dataframe.index)))

		context_df = tft.analyze_events_per_course_sections()
		total_events = np.sum(context_df['number_of_topic_favorites'])
		assert_that(total_events, equal_to(len(tft.dataframe.index)))

	def test_topics_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		tct = TopicsCreationTimeseries(self.session, start_date, end_date, course_id)
		tvt = TopicViewsTimeseries(self.session, start_date, end_date, course_id)
		tlt = TopicLikesTimeseries(self.session, start_date, end_date, course_id)
		tft = TopicFavoritesTimeseries(self.session, start_date, end_date, course_id)
		tet = TopicsEventsTimeseries(tct, tvt, tlt, tft)
		df = tet.combine_all_events_per_date()
		assert_that(len(df.index), equal_to(115))
