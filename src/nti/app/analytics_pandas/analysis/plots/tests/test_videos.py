#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.videos import VideoEventsTimeseries
from nti.analytics_pandas.analysis.plots.videos import VideoEventsTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestVideoEventsPlot(AnalyticsPandasTestBase):

	def test_explore_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		vetp = VideoEventsTimeseriesPlot(vet)
		_ = vetp.explore_events(period_breaks='1 week', minor_period_breaks='1 day')

	def test_explore_events_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		vetp = VideoEventsTimeseriesPlot(vet)
		_ = vetp.explore_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_video_events_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		vetp = VideoEventsTimeseriesPlot(vet)
		_ = vetp.analyze_video_events_types(period_breaks='1 week', minor_period_breaks='1 day')

	def test_analyze_video_events_device_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		vetp = VideoEventsTimeseriesPlot(vet)
		_ = vetp.analyze_video_events_device_types(period_breaks='1 week',
												   minor_period_breaks='1 day',
												   video_event_type='WATCH')

	def test_analyze_video_events_enrollment_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		vetp = VideoEventsTimeseriesPlot(vet)
		_ = vetp.analyze_video_events_enrollment_types(period_breaks='1 week',
												   	   minor_period_breaks='1 day',
												   	   video_event_type='WATCH')

	def test_analyze_video_events_per_course_sections(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		vetp = VideoEventsTimeseriesPlot(vet)
		_ = vetp.analyze_video_events_per_course_sections(period_breaks='1 week',
														  minor_period_breaks='1 day',
														  video_event_type='WATCH')
	def test_empty_result(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['123']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		vetp = VideoEventsTimeseriesPlot(vet)
		_ = vetp.analyze_video_events_per_course_sections(period_breaks='1 week',
														  minor_period_breaks='1 day',
														  video_event_type='WATCH')
		assert_that(len(_), equal_to(0))
		_ = vetp.analyze_video_events_enrollment_types(period_breaks='1 week',
												   	   minor_period_breaks='1 day',
												   	   video_event_type='WATCH')
		assert_that(len(_), equal_to(0))
		_ = vetp.analyze_video_events_device_types(period_breaks='1 week',
												   minor_period_breaks='1 day',
												   video_event_type='WATCH')
		assert_that(len(_), equal_to(0))
		_ = vetp.analyze_video_events_types(period_breaks='1 week', minor_period_breaks='1 day')
		assert_that(len(_), equal_to(0))
		_ = vetp.explore_events(period_breaks='1 week', minor_period_breaks='1 day')
		assert_that(len(_), equal_to(0))
