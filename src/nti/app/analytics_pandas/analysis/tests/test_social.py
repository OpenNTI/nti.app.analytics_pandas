#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.analysis.social import ContactsAddedTimeseries
from nti.analytics_pandas.analysis.social import ContactsEventsTimeseries
from nti.analytics_pandas.analysis.social import ContactsRemovedTimeseries
from nti.analytics_pandas.analysis.social import FriendsListsMemberAddedTimeseries
from nti.analytics_pandas.analysis.social import DynamicFriendsListsMemberAddedTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestContactsEventsTimeseries(AnalyticsPandasTestBase):

	def test_combined_events(self):
		start_date = '2015-01-01'
		end_date = '2015-10-19'
		cat = ContactsAddedTimeseries(self.session, start_date, end_date)
		crt = ContactsRemovedTimeseries(self.session, start_date, end_date)
		cet = ContactsEventsTimeseries(cat=cat, crt=crt)
		df = cet.combine_events()
		assert_that(df.empty, equal_to(False))
		assert_that(df.columns, has_item('timestamp_period'))
		assert_that(df.columns, has_item('total_events'))
		assert_that(df.columns, has_item('event_type'))

class TestContactsAddedTimeseries(AnalyticsPandasTestBase):

	def test_analyze_events(self):
		start_date = '2015-01-01'
		end_date = '2015-10-19'
		cat = ContactsAddedTimeseries(self.session, start_date, end_date)
		assert_that(cat.dataframe, has_item('timestamp'))
		assert_that(cat.dataframe, has_item('timestamp_period'))
		assert_that(cat.dataframe, has_item('target_id'))
		assert_that(cat.dataframe, has_item('user_id'))
		df = cat.analyze_events()
		assert_that(df.empty, equal_to(False))
		assert_that(df.columns, has_item('number_of_contacts_added'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_analyze_application_type(self):
		start_date = '2015-01-01'
		end_date = '2015-10-19'
		cat = ContactsAddedTimeseries(self.session, start_date, end_date)
		df = cat.analyze_application_types()
		assert_that(df.empty, equal_to(False))
		assert_that(df.columns, has_item('number_of_contacts_added'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

class TestContactsRemovedTimeseries(AnalyticsPandasTestBase):

	def test_analyze_events(self):
		start_date = '2015-01-01'
		end_date = '2015-10-19'
		crt = ContactsRemovedTimeseries(self.session, start_date, end_date)
		assert_that(crt.dataframe, has_item('timestamp'))
		assert_that(crt.dataframe, has_item('timestamp_period'))
		assert_that(crt.dataframe, has_item('target_id'))
		assert_that(crt.dataframe, has_item('user_id'))
		df = crt.analyze_events()
		assert_that(df.empty, equal_to(False))
		assert_that(df.columns, has_item('number_of_contacts_removed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_analyze_application_type(self):
		start_date = '2015-01-01'
		end_date = '2015-10-19'
		crt = ContactsRemovedTimeseries(self.session, start_date, end_date)
		df = crt.analyze_application_types()
		assert_that(df.empty, equal_to(False))
		assert_that(df.columns, has_item('number_of_contacts_removed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

class TestDynamicFriendsListsMemberAddedTimeseries(AnalyticsPandasTestBase):

	def test_analyze_number_of_friend_list_members_added(self):
		start_date = '2015-01-01'
		end_date = '2015-10-19'
		dflmat = DynamicFriendsListsMemberAddedTimeseries(self.session, start_date, end_date)
		df = dflmat.analyze_number_of_friend_list_members_added()
		assert_that(df, equal_to(None))

# 		assert_that(df.empty, equal_to(False))
# 		assert_that(df.columns, has_item('timestamp_period'))
# 		assert_that(df.columns, has_item('total_number_of_dynamic_friend_list_members_added'))
# 		assert_that(df.columns, has_item('number_of_friend_lists'))

class TestFriendsListsMemberAddedTimeseries(AnalyticsPandasTestBase):

	def test_analyze_number_of_friend_list_members_added(self):
		start_date = '2015-01-01'
		end_date = '2015-10-19'
		flmat = FriendsListsMemberAddedTimeseries(self.session, start_date, end_date)
		df = flmat.analyze_number_of_friend_list_members_added()
		assert_that(df.empty, equal_to(False))
		assert_that(df.columns, has_item('timestamp_period'))
		assert_that(df.columns, has_item('average_number_of_friend_list_members_added'))
		assert_that(df.columns, has_item('total_number_of_friend_list_members_added'))
		assert_that(df.columns, has_item('number_of_friend_lists'))
