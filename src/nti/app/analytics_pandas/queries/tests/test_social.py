#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that
from hamcrest import greater_than

from nti.analytics_pandas.queries.social import QueryContactsAdded
from nti.analytics_pandas.queries.social import QueryContactsRemoved
from nti.analytics_pandas.queries.social import QueryFriendsListsCreated
from nti.analytics_pandas.queries.social import QueryFriendsListsMemberAdded
from nti.analytics_pandas.queries.social import QueryFriendsListsMemberRemoved
from nti.analytics_pandas.queries.social import QueryDynamicFriendsListsCreated
from nti.analytics_pandas.queries.social import QueryDynamicFriendsListsMemberAdded
from nti.analytics_pandas.queries.social import QueryDynamicFriendsListsMemberRemoved

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestContacts(AnalyticsPandasTestBase):

	def test_query_contacts_added(self):
		start_date = u'2015-01-01'
		end_date = u'2015-10-19'
		qca = QueryContactsAdded(self.session)
		dataframe = qca.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), greater_than(0))

	def test_query_contacts_removed(self):
		start_date = u'2015-01-01'
		end_date = u'2015-10-19'
		qcr = QueryContactsRemoved(self.session)
		dataframe = qcr.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), greater_than(0))

class TestDynamicFriendsLists(AnalyticsPandasTestBase):

	def test_query_dynamic_friend_lists_created(self):
		start_date = u'2015-01-01'
		end_date = u'2015-10-19'
		qdflc = QueryDynamicFriendsListsCreated(self.session)
		dataframe = qdflc.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), greater_than(0))

	def test_query_dynamic_friend_list_member_added(self):
		"""
		check result againts query:
		select * from DynamicFriendsListsMemberAdded where date(timestamp) between '2015-01-01' and '2015-10-19'
		"""
		start_date = u'2015-01-01'
		end_date = u'2015-10-19'
		qdflma = QueryDynamicFriendsListsMemberAdded(self.session)
		dataframe = qdflma.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(0))

	def test_query_dynamic_friend_list_member_removed(self):
		"""
		check result againts query:
		select * from DynamicFriendsListsMemberRemoved where date(timestamp) between '2015-01-01' and '2015-10-19'
		"""
		start_date = u'2015-01-01'
		end_date = u'2015-10-19'
		qdflmr = QueryDynamicFriendsListsMemberRemoved(self.session)
		dataframe = qdflmr.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(0))

class TestFriendsLists(AnalyticsPandasTestBase):

	def test_query_friend_lists_created(self):
		start_date = u'2015-01-01'
		end_date = u'2015-10-19'
		qflc = QueryFriendsListsCreated(self.session)
		dataframe = qflc.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), greater_than(0))

	def test_query_friend_list_member_added(self):
		start_date = u'2015-01-01'
		end_date = u'2015-10-19'
		qflma = QueryFriendsListsMemberAdded(self.session)
		dataframe = qflma.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), greater_than(0))

	def test_query_friend_list_member_removed(self):
		"""
		check result againts query:
		select * from FriendsListsMemberRemoved where date(timestamp) between '2015-01-01' and '2015-10-19'
		"""
		start_date = u'2015-01-01'
		end_date = u'2015-10-19'
		qflmr = QueryFriendsListsMemberRemoved(self.session)
		dataframe = qflmr.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(0))
