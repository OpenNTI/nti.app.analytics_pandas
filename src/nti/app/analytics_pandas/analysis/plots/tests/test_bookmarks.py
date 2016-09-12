#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.bookmarks import BookmarkCreationTimeseries
from nti.analytics_pandas.analysis.plots.bookmarks import BookmarksTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestBookmarksPlot(AnalyticsPandasTestBase):

	def test_explore_events_bookmark_creation(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		bct = BookmarkCreationTimeseries(self.session, start_date, end_date, course_id)
		bctp = BookmarksTimeseriesPlot(bct)
		_ = bctp.explore_events()

	def test_explore_events_bookmark_creation_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		bct = BookmarkCreationTimeseries(self.session, start_date, end_date, course_id, 
										 period='weekly')
		bctp = BookmarksTimeseriesPlot(bct)
		_ = bctp.explore_events(period_breaks='1 week', minor_period_breaks = None)
		
	def test_analyze_bookmark_creation_resource_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		bct = BookmarkCreationTimeseries(self.session, start_date, end_date, course_id)
		bctp = BookmarksTimeseriesPlot(bct)
		_ = bctp.analyze_resource_types()

	def test_analyze_bookmark_creation_device_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		bct = BookmarkCreationTimeseries(self.session, start_date, end_date, course_id)
		bctp = BookmarksTimeseriesPlot(bct)
		_ = bctp.analyze_device_types()

	def test_analyze_bookmark_creation_enrollment_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		bct = BookmarkCreationTimeseries(self.session, start_date, end_date, course_id)
		bctp = BookmarksTimeseriesPlot(bct)
		_ = bctp.analyze_enrollment_types()

	def test_analyze_bookmark_resource_device_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		bct = BookmarkCreationTimeseries(self.session, start_date, end_date, course_id)
		bctp = BookmarksTimeseriesPlot(bct)
		_ = bctp.analyze_resource_device_types()

	def test_get_the_most_active_users(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		bct = BookmarkCreationTimeseries(self.session, start_date, end_date, course_id)
		bctp = BookmarksTimeseriesPlot(bct)
		_ = bctp.plot_the_most_active_users(max_rank_number=10)

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		bct = BookmarkCreationTimeseries(self.session, start_date, end_date, course_id)
		bctp = BookmarksTimeseriesPlot(bct)
		_ = bctp.analyze_events_per_course_sections()

	def test_empty_result(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['123']
		bct = BookmarkCreationTimeseries(self.session, start_date, end_date, course_id)
		bctp = BookmarksTimeseriesPlot(bct)
		_ = bctp.explore_events()
		assert_that(len(_), equal_to(0))
		_ = bctp.analyze_resource_types()
		assert_that(len(_), equal_to(0))
		_ = bctp.analyze_device_types()
		assert_that(len(_), equal_to(0))
		_ = bctp.analyze_enrollment_types()
		assert_that(len(_), equal_to(0))
		_ = bctp.analyze_resource_device_types()
		assert_that(len(_), equal_to(0))
		_ = bctp.plot_the_most_active_users(max_rank_number=10)
		assert_that(len(_), equal_to(0))
		_ = bctp.analyze_events_per_course_sections()
		assert_that(len(_), equal_to(0))
