#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from ..queries import QueryVideoEvents

from ..utils import cast_columns_as_category_

from .common import analyze_types_
from .common import add_timestamp_period_

class VideoEventsTimeseries(object):
	"""
	analyze the number of video events given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, period='daily',
				 with_context_name=True, with_enrollment_type=True):
		self.session = session
		self.period = period
		qve = self.query_videos_event = QueryVideoEvents(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qve.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qve.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['video_event_type', 'with_transcript']

			self.with_device_type = with_device_type
			if with_device_type:
				new_df = qve.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			if with_context_name:
				new_df = qve.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qve.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('enrollment_type')

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)
			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_video_events(self, video_event_type=None):
		"""
		Generate a dataframe based on given video_event_type
		The dataframe consists of :
		- number of video events
		- number of unique users
		- ratio of video events over unique users
		"""
		group_by_items = ['timestamp_period']
		if video_event_type is None:
			dataframe = self.dataframe
		else:
			if self.dataframe.empty:
				return
			dataframe = self.dataframe[['timestamp_period', 'video_view_id', 'user_id',
										'video_event_type']]
			dataframe = dataframe.loc[dataframe['video_event_type'] == video_event_type]
		df = self.build_dataframe(dataframe, group_by_items)
		return df

	def analyze_video_events_types(self):
		"""
		Generate dataframe based that consists of :
		- number of video events
		- number of unique users
		- ratio of video events over unique users
		"""
		group_by_items = ['timestamp_period', 'video_event_type']
		df = self.build_dataframe(self.dataframe, group_by_items)
		return df

	def analyze_video_events_per_course_sections(self, video_event_type='WATCH'):
		"""
		Generate a dataframe based on given video_event_type value (WATCH/SKIP) per course section
		The dataframe consists of :
		- number of video events
		- number of unique users
		- ratio of video events over unique users
		"""
		if self.dataframe.empty:
			return
		dataframe = self.dataframe[['timestamp_period', 'video_view_id', 'user_id',
									'course_id', 'context_name', 'video_event_type']]
		dataframe = dataframe.loc[dataframe['video_event_type'] == video_event_type]
		group_by_items = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(dataframe, group_by_items)
		return df

	def analyze_video_events_device_types(self, video_event_type):
		"""
		Generate a dataframe based on given video_event_type value (WATCH/SKIP)
		The dataframe consists of :
		- number of video events
		- number of unique users
		- ratio of video events over unique users
		grouped by device_type
		"""
		if self.dataframe.empty:
			return
		dataframe = self.dataframe[['timestamp_period', 'video_view_id', 'user_id',
									'device_type', 'video_event_type']]
		dataframe = dataframe.loc[dataframe['video_event_type'] == video_event_type]
		group_by_items = ['timestamp_period', 'device_type']
		df = self.build_dataframe(dataframe, group_by_items)
		return df

	def analyze_video_events_enrollment_types(self, video_event_type):
		"""
		Generate a dataframe based on given video_event_type value (WATCH/SKIP)
		The dataframe consists of :
		- number of video events
		- number of unique users
		- ratio of video events over unique users
		grouped by enrollment_type
		"""
		if self.dataframe.empty:
			return
		dataframe = self.dataframe[['timestamp_period', 'video_view_id', 'user_id',
									'enrollment_type', 'video_event_type']]
		dataframe = dataframe.loc[dataframe['video_event_type'] == video_event_type]
		group_by_items = ['timestamp_period', 'enrollment_type']
		df = self.build_dataframe(dataframe, group_by_items)
		return df

	def analyze_video_events_transcript(self, video_event_type):
		"""
		Generate a dataframe based on given video_event_type value (WATCH/SKIP)
		The dataframe consists of :
		- number of video events
		- number of unique users
		- ratio of video events over unique users
		grouped by with_transcript values
		"""
		if self.dataframe.empty:
			return
		dataframe = self.dataframe[['timestamp_period', 'video_view_id', 'user_id',
									'with_transcript', 'video_event_type']]
		dataframe = dataframe.loc[dataframe['video_event_type'] == video_event_type]
		group_by_items = ['timestamp_period', 'with_transcript']
		df = self.build_dataframe(dataframe, group_by_items)
		return df

	def build_dataframe(self, dataframe, group_by_items):
		agg_columns = {	'user_id': pd.Series.nunique,
						'video_view_id': pd.Series.count}
		df = analyze_types_(dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'user_id'		:'number_of_unique_users',
								'video_view_id'	:'number_of_video_events'},
						inplace=True)
			df['ratio'] = df['number_of_video_events'] / df['number_of_unique_users']
		return df
