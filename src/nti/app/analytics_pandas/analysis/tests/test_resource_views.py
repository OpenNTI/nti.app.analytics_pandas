#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.analysis.resource_views import ResourceViewsTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestResourceViewsEDA(AnalyticsPandasTestBase):

	def test_resource_views_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(rvt.dataframe.index), equal_to(4240))
		assert_that(rvt.dataframe.columns, has_item('device_type'))
		assert_that(rvt.dataframe.columns, has_item('resource_type'))
		assert_that(rvt.dataframe.columns, has_item('context_name'))
		assert_that(rvt.dataframe.columns, has_item('enrollment_type'))

		event_df = rvt.analyze_events()
		assert_that(len(event_df.index), equal_to(129))

		df = rvt.analyze_events_based_on_resource_type()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_resource_views'))

		df = rvt.analyze_events_based_on_device_type()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_resource_views'))

		df = rvt.analyze_events_based_on_resource_device_type()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_resource_views'))

		df = rvt.get_the_most_active_users()
		assert_that(df.columns, has_item('user_id'))
		assert_that(df.columns, has_item('number_of_activities'))
		assert_that(len(df.index), equal_to(10))

		df = rvt.get_the_most_viewed_resources()
		assert_that(df.columns, has_item('resource_id'))
		assert_that(df.columns, has_item('resource_display_name'))
		assert_that(df.columns, has_item('resource_type'))
		assert_that(df.columns, has_item('number_of_views'))
		assert_that(len(df.index), equal_to(10))

		df = rvt.analyze_events_per_course_sections()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_resource_views'))
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(event_df.index)))
