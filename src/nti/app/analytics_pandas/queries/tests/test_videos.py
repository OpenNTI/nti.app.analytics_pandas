#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.queries.videos import QueryVideoEvents

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestVideos(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestVideos, self).setUp()

	def test_query_video_events_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qve = QueryVideoEvents(self.session)
		dataframe = qve.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(105505))

	def test_query_video_events_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qve = QueryVideoEvents(self.session)
		dataframe = qve.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(1480))

	def test_query_video_events_add_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qve = QueryVideoEvents(self.session)
		dataframe = qve.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(1480))
		new_df = qve.add_device_type(dataframe)
		assert_that(len(dataframe.index), equal_to(len(new_df.index)))
		assert_that(new_df.columns, has_item('device_type'))

	def test_query_video_events_add_resource_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qve = QueryVideoEvents(self.session)
		dataframe = qve.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(1480))
		new_df = qve.add_resource_type(dataframe)
		assert_that(len(dataframe.index), equal_to(len(new_df.index)))
		assert_that(new_df.columns, has_item('resource_type'))
