#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.highlights import HighlightsCreationTimeseries
from nti.analytics_pandas.analysis.plots.highlights import HighlightsCreationTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestHighlightsCreationPlot(AnalyticsPandasTestBase):

	def test_explore_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		hct = HighlightsCreationTimeseries(self.session, start_date, end_date, course_id)
		hctp = HighlightsCreationTimeseriesPlot(hct)
		hctp.explore_events()

	def test_explore_events_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		hct = HighlightsCreationTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		hctp = HighlightsCreationTimeseriesPlot(hct)
		hctp.explore_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_device_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		hct = HighlightsCreationTimeseries(self.session, start_date, end_date, course_id)
		hctp = HighlightsCreationTimeseriesPlot(hct)
		hctp.analyze_device_types()

	def test_analyze_enrollment_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		hct = HighlightsCreationTimeseries(self.session, start_date, end_date, course_id)
		hctp = HighlightsCreationTimeseriesPlot(hct)
		hctp.analyze_enrollment_types()

	def test_analyze_resource_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		hct = HighlightsCreationTimeseries(self.session, start_date, end_date, course_id)
		hctp = HighlightsCreationTimeseriesPlot(hct)
		hctp.analyze_resource_types()

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		hct = HighlightsCreationTimeseries(self.session, start_date, end_date, course_id)
		hctp = HighlightsCreationTimeseriesPlot(hct)
		hctp.analyze_events_per_course_sections()

	def test_plot_most_active_users(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		hct = HighlightsCreationTimeseries(self.session, start_date, end_date, course_id)
		hctp = HighlightsCreationTimeseriesPlot(hct)
		hctp.plot_the_most_active_users()

	def test_empty_result(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['123']
		hct = HighlightsCreationTimeseries(self.session, start_date, end_date, course_id)
		hctp = HighlightsCreationTimeseriesPlot(hct)
		hctp.plot_the_most_active_users()
		assert_that(len(_), equal_to(0))
		hctp.analyze_events_per_course_sections()
		assert_that(len(_), equal_to(0))
		hctp.analyze_resource_types()
		assert_that(len(_), equal_to(0))
		hctp.analyze_enrollment_types()
		assert_that(len(_), equal_to(0))
		hctp.analyze_device_types()
		assert_that(len(_), equal_to(0))
		hctp.explore_events()
		assert_that(len(_), equal_to(0))
