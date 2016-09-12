#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.analysis.bookmarks import BookmarkCreationTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestBookmarksEDA(AnalyticsPandasTestBase):

	def test_bookmarks_creation_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		bct = BookmarkCreationTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(bct.dataframe.index), equal_to(54))
		assert_that(bct.dataframe.columns, has_item('resource_type'))
		assert_that(bct.dataframe.columns, has_item('device_type'))
		assert_that(bct.dataframe.columns, has_item('enrollment_type'))

		df = bct.analyze_events()
		assert_that(len(df.index), equal_to(20))

		df, resource_df = bct.analyze_resource_types()
		assert_that(len(df), equal_to(22))
		assert_that(len(df.sum(level='timestamp_period')), equal_to(20))
		assert_that(len(df.sum(level='resource_type')), equal_to(2))
		assert_that(len(resource_df.index), equal_to(2))

		df = bct.analyze_device_types()
		assert_that(len(df), equal_to(20))
		assert_that(len(df.sum(level='timestamp_period')), equal_to(20))
		assert_that(len(df.sum(level='device_type')), equal_to(1))

		users_df = bct.get_the_most_active_users(max_rank_number=10)

		# #there is only one users creating 54 bookmarks within the time period (user_id = 56606)
		assert_that(len(users_df.index), equal_to(1))

		df = bct.analyze_events_per_course_sections()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(20))
