#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.profile_views import EntityProfileViewsTimeseries
from nti.analytics_pandas.analysis.profile_views import EntityProfileViewEventsTimeseries
from nti.analytics_pandas.analysis.profile_views import  EntityProfileActivityViewsTimeseries
from nti.analytics_pandas.analysis.profile_views import EntityProfileMembershipViewsTimeseries

from nti.analytics_pandas.analysis.plots.profile_views import EntityProfileViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.profile_views import EntityProfileViewEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.profile_views import EntityProfileActivityViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.profile_views import EntityProfileMembershipViewsTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestProfileViewsPlot(AnalyticsPandasTestBase):
	def test_explore_events(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epvt = EntityProfileViewsTimeseries(self.session, start_date, end_date)
		epvtp = EntityProfileViewsTimeseriesPlot(epvt)
		_ = epvtp.explore_events()
		assert_that(len(_), equal_to(3))

	def test_analyze_application_types(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epvt = EntityProfileViewsTimeseries(self.session, start_date, end_date)
		epvtp = EntityProfileViewsTimeseriesPlot(epvt)
		_ = epvtp.analyze_application_types()
		assert_that(len(_), equal_to(3))

	def test_analyze_viewer_types(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epvt = EntityProfileViewsTimeseries(self.session, start_date, end_date)
		epvtp = EntityProfileViewsTimeseriesPlot(epvt)
		_ = epvtp.analyze_views_by_owner_or_by_others()
		assert_that(len(_), equal_to(3))

	def test_plot_the_most_active_users(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epvt = EntityProfileViewsTimeseries(self.session, start_date, end_date)
		epvtp = EntityProfileViewsTimeseriesPlot(epvt)
		_ = epvtp.plot_the_most_active_users()
		assert_that(len(_), equal_to(1))

	def test_plot_the_most_viewed_profiles(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epvt = EntityProfileViewsTimeseries(self.session, start_date, end_date)
		epvtp = EntityProfileViewsTimeseriesPlot(epvt)
		_ = epvtp.plot_the_most_viewed_profiles()
		assert_that(len(_), equal_to(1))

class TestProfileActivityViewsPlot(AnalyticsPandasTestBase):

	def test_explore_events(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epavt = EntityProfileActivityViewsTimeseries(self.session, start_date, end_date)
		epavtp = EntityProfileActivityViewsTimeseriesPlot(epavt)
		_ = epavtp.explore_events()
		assert_that(len(_), equal_to(3))

	def test_analyze_application_types(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epavt = EntityProfileActivityViewsTimeseries(self.session, start_date, end_date)
		epavtp = EntityProfileActivityViewsTimeseriesPlot(epavt)
		_ = epavtp.analyze_application_types()
		assert_that(len(_), equal_to(3))

	def test_analyze_views_by_owner_or_by_others(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epavt = EntityProfileActivityViewsTimeseries(self.session, start_date, end_date)
		epavtp = EntityProfileActivityViewsTimeseriesPlot(epavt)
		_ = epavtp.analyze_views_by_owner_or_by_others()
		assert_that(len(_), equal_to(3))

	def test_plot_the_most_active_users(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epavt = EntityProfileActivityViewsTimeseries(self.session, start_date, end_date)
		epavtp = EntityProfileActivityViewsTimeseriesPlot(epavt)
		_ = epavtp.plot_the_most_active_users()
		assert_that(len(_), equal_to(1))

	def test_plot_the_most_viewed_profiles(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epavt = EntityProfileActivityViewsTimeseries(self.session, start_date, end_date)
		epavtp = EntityProfileActivityViewsTimeseriesPlot(epavt)
		_ = epavtp.plot_the_most_viewed_profile_activities()
		assert_that(len(_), equal_to(1))

class TestProfileMembershipViewsPlot(AnalyticsPandasTestBase):

	def test_explore_events(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epmvt = EntityProfileMembershipViewsTimeseries(self.session, start_date, end_date)
		epmvtp = EntityProfileMembershipViewsTimeseriesPlot(epmvt)
		_ = epmvtp.explore_events()
		assert_that(len(_), equal_to(3))

	def test_analyze_application_types(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epmvt = EntityProfileMembershipViewsTimeseries(self.session, start_date, end_date)
		epmvtp = EntityProfileMembershipViewsTimeseriesPlot(epmvt)
		_ = epmvtp.analyze_application_types()
		assert_that(len(_), equal_to(3))

	def test_analyze_views_by_owner_or_by_others(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epmvt = EntityProfileMembershipViewsTimeseries(self.session, start_date, end_date)
		epmvtp = EntityProfileMembershipViewsTimeseriesPlot(epmvt)
		_ = epmvtp.analyze_views_by_owner_or_by_others()
		assert_that(len(_), equal_to(3))

	def test_plot_the_most_active_users(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epmvt = EntityProfileMembershipViewsTimeseries(self.session, start_date, end_date)
		epmvtp = EntityProfileMembershipViewsTimeseriesPlot(epmvt)
		_ = epmvtp.plot_the_most_active_users()
		assert_that(len(_), equal_to(1))

	def test_plot_the_most_viewed_profiles(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epmvt = EntityProfileMembershipViewsTimeseries(self.session, start_date, end_date)
		epmvtp = EntityProfileMembershipViewsTimeseriesPlot(epmvt)
		_ = epmvtp.plot_the_most_viewed_profile_memberships()
		assert_that(len(_), equal_to(1))

class TestEntityProfileViewEventsTimeseries(AnalyticsPandasTestBase):

	def test_combined_events(self):
		start_date = '2015-10-05'
		end_date = '2015-10-19'
		epvt = EntityProfileViewsTimeseries(self.session, start_date, end_date)
		epavt = EntityProfileActivityViewsTimeseries(self.session, start_date, end_date)
		epmvt = EntityProfileMembershipViewsTimeseries(self.session, start_date, end_date)
		epvet = EntityProfileViewEventsTimeseries(epvt=epvt, epavt=epavt, epmvt=epmvt)

		epvetp = EntityProfileViewEventsTimeseriesPlot(epvet)
		_ = epvetp.combine_events()
		assert_that(len(_), equal_to(3))
