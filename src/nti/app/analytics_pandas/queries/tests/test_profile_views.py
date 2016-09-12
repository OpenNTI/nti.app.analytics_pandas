#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import greater_than
from hamcrest import assert_that
from hamcrest import has_item

from nti.analytics_pandas.queries.profile_views import QueryEntityProfileViews
from nti.analytics_pandas.queries.profile_views import QueryEntityProfileActivityViews
from nti.analytics_pandas.queries.profile_views import QueryEntityProfileMembershipViews

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestProfileViews(AnalyticsPandasTestBase):

	def test_query_profile_views(self):
		start_date = u'2015-10-01'
		end_date = u'2015-10-15'
		qepv = QueryEntityProfileViews(self.session)
		dataframe = qepv.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), greater_than(0))
		assert_that(dataframe.columns, has_item('timestamp'))
		assert_that(dataframe.columns, has_item('context_path'))
		assert_that(dataframe.columns, has_item('time_length'))
		assert_that(dataframe.columns, has_item('target_id'))
		assert_that(dataframe.columns, has_item('session_id'))
		assert_that(dataframe.columns, has_item('user_id'))

		df = qepv.add_application_type(dataframe)
		assert_that(len(dataframe.index), greater_than(0))
		assert_that(df, has_item('application_type'))

	def test_query_profile_activity_views(self):
		start_date = u'2015-10-01'
		end_date = u'2015-10-15'
		qepav = QueryEntityProfileActivityViews(self.session)
		dataframe = qepav.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), greater_than(0))
		assert_that(dataframe.columns, has_item('timestamp'))
		assert_that(dataframe.columns, has_item('context_path'))
		assert_that(dataframe.columns, has_item('time_length'))
		assert_that(dataframe.columns, has_item('target_id'))
		assert_that(dataframe.columns, has_item('session_id'))
		assert_that(dataframe.columns, has_item('user_id'))

		df = qepav.add_application_type(dataframe)
		assert_that(len(dataframe.index), greater_than(0))
		assert_that(df, has_item('application_type'))

	def test_query_profile_membership_views(self):
		start_date = u'2015-10-01'
		end_date = u'2015-10-15'
		qepmv = QueryEntityProfileMembershipViews(self.session)
		dataframe = qepmv.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), greater_than(0))
		assert_that(dataframe.columns, has_item('timestamp'))
		assert_that(dataframe.columns, has_item('context_path'))
		assert_that(dataframe.columns, has_item('time_length'))
		assert_that(dataframe.columns, has_item('target_id'))
		assert_that(dataframe.columns, has_item('session_id'))
		assert_that(dataframe.columns, has_item('user_id'))

		df = qepmv.add_application_type(dataframe)
		assert_that(len(dataframe.index), greater_than(0))
		assert_that(df, has_item('application_type'))
