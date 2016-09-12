#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.social import ContactsAddedTimeseries
from nti.analytics_pandas.analysis.social import ContactsEventsTimeseries
from nti.analytics_pandas.analysis.social import ContactsRemovedTimeseries
from nti.analytics_pandas.analysis.social import FriendsListsMemberAddedTimeseries

from nti.analytics_pandas.analysis.plots.social import ContactsAddedTimeseriesPlot
from nti.analytics_pandas.analysis.plots.social import ContactsEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.social import ContactsRemovedTimeseriesPlot
from nti.analytics_pandas.analysis.plots.social import FriendsListsMemberAddedTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestContactsEventsTimeseriesPlot(AnalyticsPandasTestBase):

	def test_combine_events(self):
		start_date = '2015-06-01'
		end_date = '2015-10-19'
		period = 'weekly'
		cat = ContactsAddedTimeseries(self.session, start_date, end_date, period=period)
		crt = ContactsRemovedTimeseries(self.session, start_date, end_date, period=period)
		cet = ContactsEventsTimeseries(cat=cat, crt=crt)
		cetp = ContactsEventsTimeseriesPlot(cet)
		_ = cetp.combine_events(period_breaks='1 week')
		assert_that(len(_), equal_to(3))

class TestContactsAddedTimeseriesPlot(AnalyticsPandasTestBase):

	def test_analyze_events(self):
		start_date = '2015-06-01'
		end_date = '2015-10-19'
		period = 'weekly'
		cat = ContactsAddedTimeseries(self.session, start_date, end_date, period=period)
		catp = ContactsAddedTimeseriesPlot(cat)
		_ = catp.analyze_events(period_breaks='1 week')
		assert_that(len(_), equal_to(3))

	def test_analyze_application_types(self):
		start_date = '2015-06-01'
		end_date = '2015-10-19'
		period = 'weekly'
		cat = ContactsAddedTimeseries(self.session, start_date, end_date, period=period)
		catp = ContactsAddedTimeseriesPlot(cat)
		_ = catp.analyze_application_types(period_breaks='1 week')
		assert_that(len(_), equal_to(3))

	def test_plot_the_most_active_users(self):
		start_date = '2015-06-01'
		end_date = '2015-10-19'
		period = 'weekly'
		cat = ContactsAddedTimeseries(self.session, start_date, end_date, period=period)
		catp = ContactsAddedTimeseriesPlot(cat)
		_ = catp.plot_the_most_active_users()
		assert_that(len(_), equal_to(1))

class TestContactsRemovedTimeseriesPlot(AnalyticsPandasTestBase):

	def test_analyze_events(self):
		start_date = '2015-06-01'
		end_date = '2015-10-19'
		period = 'weekly'
		crt = ContactsRemovedTimeseries(self.session, start_date, end_date, period=period)
		crtp = ContactsRemovedTimeseriesPlot(crt)
		_ = crtp.analyze_events(period_breaks='1 week')
		assert_that(len(_), equal_to(3))

	def test_analyze_application_types(self):
		start_date = '2015-06-01'
		end_date = '2015-10-19'
		period = 'weekly'
		crt = ContactsRemovedTimeseries(self.session, start_date, end_date, period=period)
		crtp = ContactsRemovedTimeseriesPlot(crt)
		_ = crtp.analyze_application_types(period_breaks='1 week')
		assert_that(len(_), equal_to(3))

	def test_plot_the_most_active_users(self):
		start_date = '2015-06-01'
		end_date = '2015-10-19'
		period = 'weekly'
		crt = ContactsAddedTimeseries(self.session, start_date, end_date, period=period)
		crtp = ContactsAddedTimeseriesPlot(crt)
		_ = crtp.plot_the_most_active_users()
		assert_that(len(_), equal_to(1))

class TestFriendsListsMemberAddedTimeseriesPlot(AnalyticsPandasTestBase):

	def test_analyze_number_of_friend_list_members_added(self):
		start_date = '2015-06-01'
		end_date = '2015-10-19'
		period = 'weekly'
		flmat = FriendsListsMemberAddedTimeseries(self.session, start_date, end_date, period=period)
		flmatp = FriendsListsMemberAddedTimeseriesPlot(flmat)
		_ = flmatp.analyze_number_of_friend_list_members_added(period_breaks='1 week')
		assert_that(len(_), equal_to(3))
