#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.analysis.highlights import HighlightsCreationTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestHighlightsEDA(AnalyticsPandasTestBase):

	def test_highlights_creation_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		hct = HighlightsCreationTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(hct.dataframe.index), equal_to(779))
		assert_that(hct.dataframe.columns, has_item('device_type'))
		assert_that(hct.dataframe.columns, has_item('resource_type'))
		assert_that(hct.dataframe.columns, has_item('enrollment_type'))

		df = hct.analyze_events()
		assert_that(len(df.index), equal_to(36))

		df = hct.analyze_device_types()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_highlights_created'))

		df = hct.analyze_resource_types()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_highlights_created'))

		df = hct.analyze_resource_device_types()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_highlights_created'))

		users_df = hct.get_the_most_active_users(max_rank_number = 10)
		assert_that(len(users_df.index), equal_to(10))

		df = hct.analyze_events_per_course_sections()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_highlights_created'))
