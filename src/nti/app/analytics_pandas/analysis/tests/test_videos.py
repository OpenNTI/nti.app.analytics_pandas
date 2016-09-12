#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

import numpy as np

from nti.analytics_pandas.analysis.videos import  VideoEventsTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestVideosEDA(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestVideosEDA, self).setUp()

	def test_video_events_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(vet.dataframe.index), equal_to(1480))
		assert_that(vet.dataframe.columns, has_item('device_type'))
		assert_that(vet.dataframe.columns, has_item('context_name'))
		assert_that(vet.dataframe.columns, has_item('enrollment_type'))

		event_by_date_df = vet.analyze_video_events()
		assert_that(len(event_by_date_df.index), equal_to(95))

		total_events = np.sum(event_by_date_df['number_of_video_events'])
		assert_that(total_events, equal_to(len(vet.dataframe.index)))

	def test_analyze_video_events_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		df = vet.analyze_video_events_types()
		df2 = vet.analyze_video_events()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

	def test_analyze_video_events_device_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		df = vet.analyze_video_events_device_types(video_event_type='WATCH')
		df2 = vet.analyze_video_events(video_event_type='WATCH')
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

	def test_analyze_video_events_per_course_sections(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		df = vet.analyze_video_events_per_course_sections(video_event_type='WATCH')
		df2 = vet.analyze_video_events(video_event_type='WATCH')
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

	def test_analyze_video_events_transcript(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		vet = VideoEventsTimeseries(self.session, start_date, end_date, course_id)
		df = vet.analyze_video_events_transcript(video_event_type='WATCH')
		df2 = vet.analyze_video_events(video_event_type='WATCH')
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))
