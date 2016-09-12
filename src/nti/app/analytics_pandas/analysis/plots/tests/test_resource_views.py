#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.resource_views import ResourceViewsTimeseries
from nti.analytics_pandas.analysis.plots.resource_views import ResourceViewsTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestResourceViewsPlot(AnalyticsPandasTestBase):

	def test_explore_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id)
		rvtp = ResourceViewsTimeseriesPlot(rvt)
		rvtp.explore_events()

	def test_explore_events_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		rvtp = ResourceViewsTimeseriesPlot(rvt)
		rvtp.explore_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id)
		rvtp = ResourceViewsTimeseriesPlot(rvt)
		rvtp.analyze_events_per_course_sections()

	def test_analyze_events_per_enrollment_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id)
		rvtp = ResourceViewsTimeseriesPlot(rvt)
		rvtp.analyze_enrollment_type()

	def test_resource_and_device_type_analysis(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id)
		rvtp = ResourceViewsTimeseriesPlot(rvt)
		rvtp.analyze_resource_type()
		rvtp.analyze_device_type()

	def test_plot_most_active_users(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id)
		rvtp = ResourceViewsTimeseriesPlot(rvt)
		rvtp.plot_most_active_users()

	def test_empty_result(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['123']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id)
		rvtp = ResourceViewsTimeseriesPlot(rvt)
		rvtp.plot_most_active_users()
		assert_that(len(_), equal_to(0))
		rvtp.analyze_resource_type()
		assert_that(len(_), equal_to(0))
		rvtp.analyze_device_type()
		assert_that(len(_), equal_to(0))
		rvtp.analyze_enrollment_type()
		assert_that(len(_), equal_to(0))
		rvtp.analyze_events_per_course_sections()
		assert_that(len(_), equal_to(0))
		rvtp.explore_events()
		assert_that(len(_), equal_to(0))
