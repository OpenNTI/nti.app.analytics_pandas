#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from ..queries import QueryTopicLikes
from ..queries import QueryTopicsViewed
from ..queries import QueryTopicsCreated
from ..queries import QueryTopicFavorites

from .common import analyze_types_
from .common import add_timestamp_period_
from .common import get_most_active_users_

from ..utils import cast_columns_as_category_

class TopicsEventsTimeseries(object):
	"""
	combine and analyze topics created, viewed, likes and favorites
	"""

	def __init__(self, tct, tvt, tlt, tft):
		"""
		tct = TopicsCreationTimeseries
		tvt = TopicViewsTimeseries
		tlt = TopicLikesTimeseries
		tft = TopicFavoritesTimeseries
		"""
		self.tct = tct
		self.tvt = tvt
		self.tlt = tlt
		self.tft = tft

		if tct is not None:
			self.period = tct.period
		elif tvt is not None:
			self.period = tvt.period
		elif tlt is not None:
			self.period = tlt.period
		elif tft is not None:
			self.period = tft.period
		else:
			self.period = None

	def combine_all_events_per_date(self):
		"""
		put all topics related events (create, view, like and favorite) into one dataframe
		"""
		tct = self.tct
		tvt = self.tvt
		tlt = self.tlt
		tft = self.tft

		topics_created_df = tct.analyze_events()
		topics_viewed_df = tvt.analyze_events()
		topic_likes_df = tlt.analyze_events()
		topic_favorites_df = tft.analyze_events()

		df = pd.DataFrame(columns=[	'timestamp_period', 'total_events',
									'total_unique_users', 'ratio', 'event_type'])

		if topics_created_df is not None:
			topics_created_df = self.update_events_dataframe(topics_created_df,
				column_to_rename='number_of_topics_created', event_type='CREATE')
			df = df.append(topics_created_df)

		if topics_viewed_df is not None:
			topics_viewed_df = self.update_events_dataframe(topics_viewed_df,
				column_to_rename='number_of_topics_viewed', event_type='VIEW')
			df = df.append(topics_viewed_df)

		if topic_likes_df is not None:
			topic_likes_df = self.update_events_dataframe(topic_likes_df,
				column_to_rename='number_of_topic_likes', event_type='LIKE')
			df = df.append(topic_likes_df)

		if topic_favorites_df is not None:
			topic_favorites_df = self.update_events_dataframe(topic_favorites_df,
				column_to_rename='number_of_topic_favorites', event_type='FAVORITE')
			df = df.append(topic_favorites_df)

		df.reset_index(inplace=True, drop=True)
		return df

	def update_events_dataframe(self, df, column_to_rename, event_type):
		df.rename(columns={column_to_rename:'total_events'}, inplace=True)
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['event_type'] = event_type
		return df

class TopicsCreationTimeseries(object):
	"""
	analyze the number of topics created given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, period='daily',
				 with_context_name=True, with_enrollment_type=True):
		self.session = session
		self.period = period
		qtc = self.query_topics_created = QueryTopicsCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qtc.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qtc.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['user_id']

			if with_device_type:
				new_df = qtc.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			if with_context_name:
				new_df = qtc.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qtc.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('enrollment_type')

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)
			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def analyze_events_per_course_sections(self):
		group_by_items = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def analyze_events_per_device_types(self):
		group_by_items = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def analyze_events_per_enrollment_types(self):
		group_by_items = ['timestamp_period', 'enrollment_type']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def build_dataframe(self, group_by_items, dataframe):
		agg_columns = {	'user_id'	: pd.Series.nunique,
						'topic_id' 	: pd.Series.count}
		df = analyze_types_(dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'user_id'	:'number_of_unique_users',
							  	'topic_id'	:'number_of_topics_created'},
						inplace=True)
			df['ratio'] = df['number_of_topics_created'] / df['number_of_unique_users']
		return df


class TopicLikesTimeseries(object):
	"""
	analyze the number of topic likes given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, period='daily',
				 with_context_name=True, with_enrollment_type=True):
		self.session = session
		self.period = period
		qtl = self.query_topic_likes = QueryTopicLikes(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qtl.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qtl.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = [	'user_id', 'topic_id']

			if with_device_type:
				new_df = qtl.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			if with_context_name:
				new_df = qtl.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qtl.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('enrollment_type')

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)
			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def analyze_events_per_course_sections(self):
		group_by_items = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def analyze_events_per_device_types(self, dataframe):
		group_by_items = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_items, dataframe)
		return df

	def analyze_events_per_enrollment_types(self, dataframe):
		group_by_items = ['timestamp_period', 'enrollment_type']
		df = self.build_dataframe(group_by_items, dataframe)
		return df

	def build_dataframe(self, group_by_items, dataframe):
		agg_columns = {	'user_id'	: pd.Series.nunique,
						'topic_id' 	: pd.Series.count}
		df = analyze_types_(dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'user_id'	:'number_of_unique_users',
							  	'topic_id'	:'number_of_topic_likes'},
						inplace=True)
			df['ratio'] = df['number_of_topic_likes'] / df['number_of_unique_users']
		return df

class TopicViewsTimeseries(object):
	"""
	analyze the number of topics viewed given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, period='daily',
				 with_context_name=True, with_enrollment_type=True):
		self.session = session
		self.period = period
		qtv = self.query_topics_viewed = QueryTopicsViewed(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qtv.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qtv.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = [	'user_id', 'topic_id']

			if with_device_type:
				new_df = qtv.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			if with_context_name:
				new_df = qtv.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qtv.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('enrollment_type')

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)
			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_events_per_course_sections(self):
		group_by_items = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_device_types(self):
		group_by_items = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_enrollment_types(self):
		group_by_items = ['timestamp_period', 'enrollment_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_items):
		agg_columns = {	'user_id'	: pd.Series.nunique,
						'topic_id' 	: pd.Series.count}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'user_id'	:'number_of_unique_users',
							  	'topic_id'	:'number_of_topics_viewed'},
						inplace=True)
			df['ratio'] = df['number_of_topics_viewed'] / df['number_of_unique_users']
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_topics_viewed'},
							inplace=True)
		return users_df

class TopicFavoritesTimeseries(object):
	"""
	analyze the number of topic favorites given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, period='daily',
				 with_context_name=True, with_enrollment_type=True):
		self.session = session
		self.period = period
		qtf = self.query_topic_favorites = QueryTopicFavorites(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qtf.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qtf.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['topic_id', 'user_id']

			if with_device_type:
				new_df = qtf.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			if with_context_name:
				new_df = qtf.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qtf.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('enrollment_type')

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)
			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def analyze_events_per_course_sections(self):
		group_by_items = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def analyze_events_per_device_types(self, dataframe):
		group_by_items = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_items, dataframe)
		return df

	def analyze_events_per_enrollment_types(self, dataframe):
		group_by_items = ['timestamp_period', 'enrollment_type']
		df = self.build_dataframe(group_by_items, dataframe)
		return df

	def build_dataframe(self, group_by_items, dataframe):
		agg_columns = {	'user_id'	: pd.Series.nunique,
						'topic_id' 	: pd.Series.count}
		df = analyze_types_(dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'user_id'	:'number_of_unique_users',
							  	'topic_id'	:'number_of_topic_favorites'},
						inplace=True)
			df['ratio'] = df['number_of_topic_favorites'] / df['number_of_unique_users']
		return df
