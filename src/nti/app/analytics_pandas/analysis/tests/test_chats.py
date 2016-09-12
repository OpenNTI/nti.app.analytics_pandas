#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.analysis.chats import ChatsJoinedTimeseries
from nti.analytics_pandas.analysis.chats import ChatsInitiatedTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestChatsInitiatedTimeseries(AnalyticsPandasTestBase):

	def test_analyze_events(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		cit = ChatsInitiatedTimeseries(self.session, start_date, end_date)
		assert_that(cit.dataframe, has_item('timestamp'))
		assert_that(cit.dataframe, has_item('timestamp_period'))
		assert_that(cit.dataframe, has_item('chat_id'))
		assert_that(cit.dataframe, has_item('user_id'))
		df = cit.analyze_events()
		assert_that(df.empty, equal_to(False))
		assert_that(df.columns, has_item('number_of_chats_initiated'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_analyze_application_types(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		cit = ChatsInitiatedTimeseries(self.session, start_date, end_date)
		df = cit.analyze_application_types()
		"""
		#why None?
		#because the session_id in table chatsinitiated are NULL for the given time period
		#compare with the following query:
			select distinct session_id from chatsinitiated
			where date(timestamp) between '2015-10-05' and '2015-10-19'
		"""
		assert_that(df, equal_to(None))

	def test_chats_initiated_weekly(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		cit = ChatsInitiatedTimeseries(self.session, start_date, end_date, period='weekly')
		assert_that(cit.dataframe, has_item('timestamp'))
		assert_that(cit.dataframe, has_item('timestamp_period'))
		assert_that(cit.dataframe, has_item('chat_id'))
		assert_that(cit.dataframe, has_item('user_id'))
		df = cit.analyze_events()
		assert_that(df.empty, equal_to(False))
		assert_that(df.columns, has_item('number_of_chats_initiated'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

class TestChatsJoinedTimeseries(AnalyticsPandasTestBase):

	def test_users_joining_chats(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		cjt = ChatsJoinedTimeseries(self.session, start_date, end_date)
		assert_that(cjt.dataframe, has_item('timestamp'))
		assert_that(cjt.dataframe, has_item('timestamp_period'))
		assert_that(cjt.dataframe, has_item('chat_id'))
		assert_that(cjt.dataframe, has_item('user_id'))
		df = cjt.get_number_of_users_joining_chat()
		assert_that(df.empty, equal_to(False))
		assert_that(df.columns, has_item('number_of_users_join_chats'))

		df = cjt.analyze_number_of_users_join_chats_per_date()
		assert_that(df.empty, equal_to(False))

		df = cjt.analyze_unique_users_per_date()
		assert_that(df.columns, has_item('number_of_unique_users'))

		df = cjt.analyze_one_one_and_group_chat()
		assert_that(df.columns, has_item('chat_type'))
		assert_that(df.columns, has_item('number_of_chats'))
