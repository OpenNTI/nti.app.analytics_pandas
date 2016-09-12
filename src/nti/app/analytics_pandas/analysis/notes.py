#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from ..queries import QueryUsers
from ..queries import QueryNoteLikes
from ..queries import QueryNotesViewed
from ..queries import QueryNotesCreated
from ..queries import QueryNoteFavorites

from ..utils import cast_columns_as_category_
from ..utils import get_values_of_series_categorical_index_

from .common import analyze_types_
from .common import add_timestamp_period_
from .common import get_most_active_users_

class NotesEventsTimeseries(object):
	"""
	combine and analyze notes created, viewed, likes and favorites
	"""
	def __init__(self, nct, nvt, nlt, nft):
		"""
		nct = NotesCreationTimeseries
		nvt = NotesViewTimeseries
		nlt = NoteLikesTimeseries
		nft = NoteFavoritesTimeseries
		"""
		self.nct = nct
		self.nvt = nvt
		self.nlt = nlt
		self.nft = nft

		if nct is not None:
			self.period = nct.period
		elif nvt is not None:
			self.period = nvt.period
		elif nlt is not None:
			self.period = nlt.period
		elif nft is not None:
			self.period = nft.period

	def combine_all_events(self):
		"""
		put all notes related events (create, view, like and favorite) into one dataframe
		"""
		nct = self.nct
		nvt = self.nvt
		nlt = self.nlt
		nft = self.nft

		note_likes_df = nlt.analyze_events()
		notes_created_df = nct.analyze_events()
		note_favorites_df = nft.analyze_events()
		notes_viewed_df = nvt.analyze_total_events()

		df = pd.DataFrame(columns=[	'timestamp_period', 'total_events',
									'number_of_unique_users', 'ratio', 'event_type'])

		if notes_created_df is not None:
			notes_created_df = self.update_events_dataframe(notes_created_df,
				column_to_rename='number_of_notes_created', event_type='CREATE')
			df = df.append(notes_created_df)

		if notes_viewed_df is not None:
			notes_viewed_df = self.update_events_dataframe(notes_viewed_df,
				column_to_rename='number_of_note_views', event_type='VIEW')
			df = df.append(notes_viewed_df)

		if note_likes_df is not None:
			note_likes_df = self.update_events_dataframe(note_likes_df,
				column_to_rename='number_of_note_likes', event_type='LIKE')
			df = df.append(note_likes_df)

		if note_favorites_df is not None:
			note_favorites_df = self.update_events_dataframe(note_favorites_df,
				column_to_rename='number_of_note_favorites', event_type='FAVORITE')
			df = df.append(note_favorites_df)

		df.reset_index(inplace=True, drop=True)
		return df

	def update_events_dataframe(self, df, column_to_rename, event_type):
		df.rename(columns={column_to_rename:'total_events'}, inplace=True)
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['event_type'] = event_type
		return df

class NotesCreationTimeseries(object):
	"""
	analyze the number of notes created given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True,
				 period='daily', with_context_name=True,
				 with_enrollment_type=True):
		self.session = session
		self.period = period
		qnc = self.query_notes_created = QueryNotesCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qnc.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qnc.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = [	'note_id', 'user_id', 'sharing']

			if with_device_type:
				new_df = qnc.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			if with_resource_type:
				new_df = qnc.add_resource_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('resource_type')

			if with_context_name:
				new_df = qnc.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qnc.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('enrollment_type')

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		"""
		group notes created dataframe by timestamp_period
		count the number of notes created, unique users and ratio in each group
		return the result as dataframe
		"""
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(self.dataframe, group_by_items)
		return df

	def analyze_events_per_course_sections(self):
		"""
		group notes created dataframe by timestamp_period, course_id and context_name
		count the number of notes created, unique users and ratio in each group
		return the result as dataframe
		"""
		group_by_items = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(self.dataframe, group_by_items)
		return df

	def analyze_device_types(self, dataframe):
		"""
		group notes created dataframe by timestamp_period and device_type
		count the number of notes created, unique users and ratio in each group
		return the result as dataframe
		"""
		group_by_items = ['timestamp_period', 'device_type']
		df = self.build_dataframe(dataframe, group_by_items)
		return df

	def analyze_enrollment_types(self, dataframe):
		"""
		group notes created dataframe by timestamp_period and enrollment_type
		count the number of notes created, unique users and ratio in each group
		return the result as dataframe
		"""
		group_by_items = ['timestamp_period', 'enrollment_type']
		df = self.build_dataframe(dataframe, group_by_items)
		return df

	def analyze_resource_types(self):
		"""
		group notes created dataframe by timestamp_period and resource types
		count the number of notes created, unique users and ratio in each group
		return the result as dataframe
		"""
		group_by_items = ['timestamp_period', 'resource_type']
		df = self.build_dataframe(self.dataframe, group_by_items)
		return df

	def analyze_resource_device_types(self):
		"""
		group notes created dataframe by timestamp_period, resource and device types
		count the number of notes created, unique users and ratio in each group
		return the result as dataframe
		"""
		group_by_items = ['timestamp_period', 'resource_type', 'device_type']
		df = self.build_dataframe(self.dataframe, group_by_items)
		return df

	def build_dataframe(self, dataframe, group_by_items):
		agg_columns = {	'user_id'	: pd.Series.nunique,
						'note_id' 	: pd.Series.count}
		df = analyze_types_(dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={
							'user_id'	:'number_of_unique_users',
							'note_id'	:'number_of_notes_created'},
					  inplace=True)
			df['ratio'] = df['number_of_notes_created'] / df['number_of_unique_users']
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_notes_created'},
							inplace=True)
		return users_df

	def analyze_sharing_types(self, dataframe):
		"""
		group notes created dataframe by timestamp_period and sharing types
		count the number of notes created, unique users and ratio in each group
		return the result as dataframe
		"""
		group_by_items = ['timestamp_period', 'sharing']
		df = self.build_dataframe(dataframe, group_by_items)
		return df

	def analyze_notes_created_on_videos(self):
		"""
		select only notes created on videos and return dataframes grouped by sharing and device types
		Each dataframe has columns:
		- number_of_notes_created
		- number_of_unique_users
		- ratio
		"""
		if self.dataframe.empty:
			return
		dataframe = self.dataframe[['timestamp_period', 'resource_type',
									'device_type', 'note_id', 'user_id', 'sharing']]
		dataframe = dataframe.loc[((dataframe['resource_type'] == 'video') | (dataframe['resource_type'] == 'slide video'))]
		sharing_df = self.analyze_sharing_types(dataframe)
		device_df = self.analyze_device_types(dataframe)
		return (sharing_df, device_df)

class NotesViewTimeseries(object):
	"""
	analyze the number of notes viewed given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True,
				 period='daily', with_sharing_type=True,
				 with_context_name=True, with_enrollment_type=True):
		self.session = session
		self.period = period
		qnv = self.query_notes_viewed = QueryNotesViewed(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qnv.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qnv.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['note_id', 'user_id']

			if with_device_type:
				new_df = qnv.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			if with_resource_type:
				new_df = qnv.add_resource_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('resource_type')

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

			if with_sharing_type:
				new_df = qnv.add_sharing_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('sharing')

			if with_context_name:
				new_df = qnv.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qnv.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('enrollment_type')

			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_unique_events_based_on_device_type(self):
		"""
		group notes viewed dataframe by timestamp_period and device_type
		count the number of unique users and unique notes in each group
		return the result as dataframe

		"""
		group_by_items = ['timestamp_period', 'device_type']
		df = self.build_dataframe_unique_events(group_by_items)
		return df

	def analyze_unique_events_based_on_resource_type(self):
		"""
		group notes viewed dataframe by timestamp_period and resource_type
		count the number of unique users and unique notes in each group
		return the result as dataframe

		"""
		group_by_items = ['timestamp_period', 'resource_type']
		df = self.build_dataframe_unique_events(group_by_items)
		return df

	def analyze_unique_events_based_on_sharing_type(self):
		"""
		group notes viewed dataframe by timestamp_period and sharing type
		count the number of unique users and unique notes in each group
		return the result as dataframe

		"""
		group_by_items = ['timestamp_period', 'sharing']
		df = self.build_dataframe_unique_events(group_by_items)
		return df

	def build_dataframe_unique_events(self, group_by_items):
		agg_columns = {	'user_id'	: pd.Series.nunique,
						'note_id' 	: pd.Series.nunique}

		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'user_id'	:'number_of_unique_users',
								'note_id'	:'number_of_unique_notes_viewed'},
					  inplace=True)
		return df

	def analyze_total_events(self):
		"""
		group notes viewed dataframe by timestamp_period
		count the total number of notes views, unique users and ratio of number of
		notes viewed over unique users
		"""
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_total_events_based_on_device_type(self):
		"""
		group notes viewed dataframe by timestamp_period and device_type
		count the total number of notes views, unique users and ratio of number of
		notes viewed over unique users
		"""
		group_by_items = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_total_events_based_on_enrollment_type(self):
		"""
		group notes viewed dataframe by timestamp_period and enrollment_type
		count the total number of notes views, unique users and ratio of number of
		notes viewed over unique users
		"""
		group_by_items = ['timestamp_period', 'enrollment_type']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_total_events_based_on_resource_type(self):
		"""
		group notes viewed dataframe by timestamp_period and resource_type
		count the total number of notes views, unique users and ratio of number of
		notes viewed over unique users
		"""
		group_by_items = ['timestamp_period', 'resource_type']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_total_events_based_on_sharing_type(self):
		"""
		group notes viewed dataframe by timestamp_period and sharing type
		count the total number of notes views, unique users and ratio of number of
		notes viewed over unique users
		"""
		group_by_items = ['timestamp_period', 'sharing']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_total_events_per_course_sections(self):
		"""
		group notes viewed dataframe by timestamp_period, course_id, and context_name
		count the total number of notes views, unique users and ratio of number of
		notes viewed over unique users
		"""
		group_by_items = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_items):
		agg_columns = {	'note_id' 	: pd.Series.count,
						'user_id'	: pd.Series.nunique}

		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'note_id'	:'number_of_note_views',
								'user_id'	:'number_of_unique_users'},
					  inplace=True)

			df['ratio'] = df['number_of_note_views'] / df['number_of_unique_users']
		return df

	def get_the_most_viewed_notes(self, max_rank_number=10):
		"""
		find the top n most viewed notes and return as pandas.Series
		"""
		if self.dataframe.empty:
			return
		df = self.dataframe
		most_viewed = df.groupby('note_id').size().sort_values(ascending=False)[:max_rank_number]
		return most_viewed

	def get_the_most_viewed_notes_and_its_author(self, max_rank_number=10):
		most_views = self.get_the_most_viewed_notes(max_rank_number)
		if most_views is None:
			return
		df = most_views.to_frame(name='number_of_views')
		df.reset_index(level=0, inplace=True)

		notes_id = get_values_of_series_categorical_index_(most_views).tolist()
		note_author_df = QueryNotesCreated(self.session).get_author_id_filter_by_note_id(notes_id)

		authors_id = note_author_df['user_id'].values.tolist()
		author_name_df = QueryUsers(self.session).get_username_filter_by_user_id(authors_id)

		df = df.merge(note_author_df).merge(author_name_df)
		df.rename(columns={'user_id':'author_id', 'username': 'author_name'}, inplace=True)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		user_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if user_df is None:
			return
		user_df.rename(columns={'number_of_activities':'number_of_note_views'}, inplace=True)
		return user_df

class NoteLikesTimeseries(object):
	"""
	analyze the number of note likes given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True,
				 period='daily', with_context_name=True,
				 with_enrollment_type=True):
		self.session = session
		self.period = period
		qnl = self.query_notes_viewed = QueryNoteLikes(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qnl.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qnl.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_device_type:
				new_df = qnl.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			if with_resource_type:
				new_df = qnl.add_resource_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

			if with_context_name:
				new_df = qnl.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df

			if with_enrollment_type:
				new_df = qnl.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df

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

	def analyze_events_per_resource_types(self):
		group_by_items = ['timestamp_period', 'resource_type']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def build_dataframe(self, group_by_items, dataframe):
		agg_columns = {	'user_id'	: pd.Series.nunique,
						'note_id' 	: pd.Series.count}
		df = analyze_types_(dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'user_id'	:'number_of_unique_users',
							  	'note_id'	:'number_of_note_likes'},
					  inplace=True)
			df['ratio'] = df['number_of_note_likes'] / df['number_of_unique_users']
		return df

class NoteFavoritesTimeseries(object):
	"""
	analyze the number of note favorites given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True,
				 period='daily', with_context_name=True,
				 with_enrollment_type=True):
		self.session = session
		self.period = period
		qnf = self.query_notes_viewed = QueryNoteFavorites(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qnf.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qnf.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_device_type:
				new_df = qnf.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			if with_resource_type:
				new_df = qnf.add_resource_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

			if with_context_name:
				new_df = qnf.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df

			if with_enrollment_type:
				new_df = qnf.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df

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

	def analyze_events_per_resource_types(self):
		group_by_items = ['timestamp_period', 'resource_type']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def build_dataframe(self, group_by_items, dataframe):
		agg_columns = {	'user_id'	: pd.Series.nunique,
						'note_id' 	: pd.Series.count}
		df = analyze_types_(dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'user_id'	:'number_of_unique_users',
							  	'note_id'	:'number_of_note_favorites'},
					  inplace=True)
			df['ratio'] = df['number_of_note_favorites'] / df['number_of_unique_users']
		return df
