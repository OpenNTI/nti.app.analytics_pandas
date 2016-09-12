#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.enrollments import CourseDropsTimeseries
from nti.analytics_pandas.analysis.enrollments import CourseEnrollmentsTimeseries
from nti.analytics_pandas.analysis.enrollments import CourseCatalogViewsTimeseries
from nti.analytics_pandas.analysis.enrollments import CourseEnrollmentsEventsTimeseries

from nti.analytics_pandas.analysis.plots.enrollments import CourseDropsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.enrollments import CourseEnrollmentsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.enrollments import CourseCatalogViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.enrollments import CourseEnrollmentsEventsTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestCourseCatalogViewsPlot(AnalyticsPandasTestBase):

	def test_explore_events_course_catalog_views(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		ccvt = CourseCatalogViewsTimeseries(self.session, start_date, end_date, course_id)
		ccvtp = CourseCatalogViewsTimeseriesPlot(ccvt)
		_ = ccvtp.explore_events()

	def test_explore_events_course_catalog_views_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		ccvt = CourseCatalogViewsTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		ccvtp = CourseCatalogViewsTimeseriesPlot(ccvt)
		_ = ccvtp.explore_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_device_types_plot(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		ccvt = CourseCatalogViewsTimeseries(self.session, start_date, end_date, course_id)
		ccvtp = CourseCatalogViewsTimeseriesPlot(ccvt)
		_ = ccvtp.analyze_device_types()

	def test_empty_result(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['123']
		ccvt = CourseCatalogViewsTimeseries(self.session, start_date, end_date, course_id)
		ccvtp = CourseCatalogViewsTimeseriesPlot(ccvt)
		_ = ccvtp.explore_events()
		assert_that(len(_), equal_to(0))
		_ = ccvtp.analyze_device_types()
		assert_that(len(_), equal_to(0))

class TestCourseEnrollmentsPlot(AnalyticsPandasTestBase):

	def test_explore_events_course_enrollments(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cet = CourseEnrollmentsTimeseries(self.session, start_date, end_date, course_id)
		cetp = CourseEnrollmentsTimeseriesPlot(cet)
		_ = cetp.explore_events()

	def test_explore_events_course_enrollments_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cet = CourseEnrollmentsTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		cetp = CourseEnrollmentsTimeseriesPlot(cet)
		_ = cetp.explore_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_device_enrollment_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cet = CourseEnrollmentsTimeseries(self.session, start_date, end_date, course_id)
		cetp = CourseEnrollmentsTimeseriesPlot(cet)
		_ = cetp.analyze_device_enrollment_types()

	def test_empty_result(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['123']
		cet = CourseEnrollmentsTimeseries(self.session, start_date, end_date, course_id)
		cetp = CourseEnrollmentsTimeseriesPlot(cet)
		_ = cetp.explore_events()
		assert_that(len(_), equal_to(0))
		_ = cetp.analyze_device_enrollment_types()
		assert_that(len(_), equal_to(0))

class TestCourseDropsPlot(AnalyticsPandasTestBase):

	def test_explore_events_course_drops(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cdt = CourseDropsTimeseries(self.session, start_date, end_date, course_id)
		cdtp = CourseDropsTimeseriesPlot(cdt)
		_ = cdtp.explore_events()

	def test_explore_events_course_drops_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cdt = CourseDropsTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		cdtp = CourseDropsTimeseriesPlot(cdt)
		_ = cdtp.explore_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_device_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cdt = CourseDropsTimeseries(self.session, start_date, end_date, course_id)
		cdtp = CourseDropsTimeseriesPlot(cdt)
		_ = cdtp.analyze_device_types()

	def test_analyze_enrollment_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cdt = CourseDropsTimeseries(self.session, start_date, end_date, course_id)
		cdtp = CourseDropsTimeseriesPlot(cdt)
		_ = cdtp.analyze_enrollment_types()

	def test_empty_result(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['123']
		cdt = CourseDropsTimeseries(self.session, start_date, end_date, course_id)
		cdtp = CourseDropsTimeseriesPlot(cdt)
		_ = cdtp.analyze_enrollment_types()
		assert_that(len(_), equal_to(0))
		_ = cdtp.analyze_device_types()
		assert_that(len(_), equal_to(0))
		_ = cdtp.explore_events()
		assert_that(len(_), equal_to(0))

class TestEnrollmentsEventsPlot(AnalyticsPandasTestBase):

	def test_explore_course_enrollments_vs_drops(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cet = CourseEnrollmentsTimeseries(self.session, start_date, end_date, course_id)
		cdt = CourseDropsTimeseries(self.session, start_date, end_date, course_id)
		ceet = CourseEnrollmentsEventsTimeseries(cet, cdt=cdt)
		ceetp = CourseEnrollmentsEventsTimeseriesPlot(ceet)
		_ = ceetp.explore_course_enrollments_vs_drops()

	def test_explore_course_enrollments_vs_drops_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cet = CourseEnrollmentsTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		cdt = CourseDropsTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		ceet = CourseEnrollmentsEventsTimeseries(cet, cdt=cdt)
		ceetp = CourseEnrollmentsEventsTimeseriesPlot(ceet)
		_ = ceetp.explore_course_enrollments_vs_drops(period_breaks='1 week', minor_period_breaks=None)


	def test_explore_course_catalog_views_vs_enrollments(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cet = CourseEnrollmentsTimeseries(self.session, start_date, end_date, course_id)
		ccvt = CourseCatalogViewsTimeseries(self.session, start_date, end_date, course_id)
		ceet = CourseEnrollmentsEventsTimeseries(cet, ccvt=ccvt)
		ceetp = CourseEnrollmentsEventsTimeseriesPlot(ceet)
		_ = ceetp.explore_course_catalog_views_vs_enrollments()

	def test_explore_course_catalog_views_vs_enrollments_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		cet = CourseEnrollmentsTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		ccvt = CourseCatalogViewsTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		ceet = CourseEnrollmentsEventsTimeseries(cet, ccvt=ccvt)
		ceetp = CourseEnrollmentsEventsTimeseriesPlot(ceet)
		_ = ceetp.explore_course_catalog_views_vs_enrollments(period_breaks='1 week', minor_period_breaks=None)

	def test_empty_result(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['123']
		cet = CourseEnrollmentsTimeseries(self.session, start_date, end_date, course_id)
		ccvt = CourseCatalogViewsTimeseries(self.session, start_date, end_date, course_id)
		ceet = CourseEnrollmentsEventsTimeseries(cet, ccvt=ccvt)
		ceetp = CourseEnrollmentsEventsTimeseriesPlot(ceet)
		_ = ceetp.explore_course_catalog_views_vs_enrollments()
		assert_that(len(_), equal_to(0))
		_ = ceetp.explore_course_enrollments_vs_drops()
		assert_that(len(_), equal_to(0))
