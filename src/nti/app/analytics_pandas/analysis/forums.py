#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

import numpy as np

from ..queries import QueryForumsCreated
from ..queries import QueryForumCommentLikes
from ..queries import QueryForumsCommentsCreated
from ..queries import QueryForumCommentFavorites

from ..utils import cast_columns_as_category_

from .common import analyze_types_
from .common import add_timestamp_period_
from .common import get_most_active_users_

class ForumsEventsTimeseries(object):
	"""
	combine and analyze forums created and comments created, likes, favorites
	"""

	def __init__(self, fct, fcct, fclt, fcft):
		"""
		fct = ForumsCreatedTimeseries
		fcct = ForumsCommentsCreatedTimeseries
		fclt = ForumCommentLikesTimeseries
		fcft = ForumCommentFavoritesTimeseries
		"""
		self.fct = fct
		self.fcct = fcct
		self.fclt = fclt
		self.fcft = fcft
		if fct is not None:
			self.period = fct.period
		elif fcct is not None:
			self.period = fcct.period
		elif fclt is not None:
			self.period = fclt.period
		elif fcft is not None:
			self.period = fcft.period

	def combine_all_events_per_date(self):
		"""
		put all topics related events (create, view, like and favorite) into one dataframe
		"""
		fct = self.fct
		fcct = self.fcct
		fclt = self.fclt
		fcft = self.fcft

		forums_created_df = fct.analyze_events()
		forum_comments_created_df = fcct.analyze_events()
		forum_comment_likes_df = fclt.analyze_events()
		forum_comment_favorites_df = fcft.analyze_events()

		df = pd.DataFrame(columns=[	'timestamp_period', 'total_events', 'number_of_unique_users', 'ratio', 'event_type'])

		if forums_created_df is not None:
			forums_created_df = self.update_events_dataframe(forums_created_df,
															 column_to_rename='number_of_forums_created',
															 event_type='FORUM CREATED')
			df = df.append(forums_created_df)

		if forum_comments_created_df is not None:
			forum_comments_created_df = forum_comments_created_df[ ['number_of_comment_created',
																	'number_of_unique_users',
																	'ratio'] ]
			forum_comments_created_df = self.update_events_dataframe(forum_comments_created_df,
																	 column_to_rename='number_of_comment_created',
																	 event_type='COMMENTS CREATED')
			df = df.append(forum_comments_created_df)

		if forum_comment_likes_df is not None:
			forum_comment_likes_df = self.update_events_dataframe(forum_comment_likes_df,
																  column_to_rename='number_of_likes',
																  event_type='COMMENT LIKES')
			df = df.append(forum_comment_likes_df)

		if forum_comment_favorites_df is not None:
			forum_comment_favorites_df = self.update_events_dataframe(forum_comment_favorites_df,
																	  column_to_rename='number_of_favorites',
																	  event_type='COMMENT FAVORITES')
			df = df.append(forum_comment_favorites_df)

		df.reset_index(inplace=True, drop=True)
		return df

	def update_events_dataframe(self, df, column_to_rename, event_type):
		df.rename(columns={column_to_rename:'total_events'}, inplace=True)
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['event_type'] = event_type
		return df

class ForumsCreatedTimeseries(object):
	"""
	analyze the number of forums created given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, period='daily'):

		self.session = session
		self.period = period
		qfc = self.query_forums_created = QueryForumsCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qfc.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qfc.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_device_type:
				new_df = qfc.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			if period:
				self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def analyze_events_per_device_types(self):
		if 'device_type' in self.dataframe.columns:
			group_by_items = ['timestamp_period', 'device_type']
			df = self.build_dataframe(group_by_items, self.dataframe)
			return df

	def build_dataframe(self, group_by_items, dataframe):
		agg_columns = {	'forum_id'	: pd.Series.count,
						'user_id'	: pd.Series.nunique }
		df = analyze_types_(dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'forum_id'	: 'number_of_forums_created',
								'user_id'	: 'number_of_unique_users'},
						inplace=True)
			df['ratio'] = df['number_of_forums_created'] / df['number_of_unique_users']
		return df

class ForumsCommentsCreatedTimeseries(object):
	"""
	analyze the number of forums comments created given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, period='daily',
				 with_context_name=True, with_enrollment_type=True):

		self.session = session
		self.period = period
		qfcc = self.query_forums_comments_created = QueryForumsCommentsCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qfcc.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qfcc.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = [	'forum_id', 'parent_user_id', 'user_id', 'course_id']
			if with_device_type:
				new_df = qfcc.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			if with_context_name:
				new_df = qfcc.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qfcc.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('enrollment_type')

			if period:
				self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_device_types(self):
		if 'device_type' in self.dataframe.columns:
			group_by_items = ['timestamp_period', 'device_type']
			df = self.build_dataframe(group_by_items)
			return df

	def analyze_enrollment_types(self):
		if 'enrollment_type' in self.dataframe.columns:
			group_by_items = ['timestamp_period', 'enrollment_type']
			df = self.build_dataframe(group_by_items)
			return df

	def analyze_comments_per_section(self):
		if 'course_id' in self.dataframe.columns:
			group_by_items = ['timestamp_period', 'course_id', 'context_name']
			df = self.build_dataframe(group_by_items)
			return df

	def build_dataframe(self, group_by_items):
		agg_columns = {	'comment_id'	: pd.Series.count,
						'user_id'		: pd.Series.nunique,
						'comment_length': np.mean,
						'like_count'	: np.sum,
						'favorite_count': np.sum}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'comment_id'	 :'number_of_comment_created',
								'user_id'		 :'number_of_unique_users',
								'comment_length' :'average_comment_length'},
					  inplace=True)
			df['ratio'] = df['number_of_comment_created'] / df['number_of_unique_users']
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities' : 'number_of_comments_created'},
							inplace=True)
		return users_df

class ForumCommentLikesTimeseries(object):
	"""
	analyze the number of forum comment likes given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, period='daily',
				 with_context_name=True, with_enrollment_type=True):
		self.session = session
		self.period = period
		qfcl = self.query_forum_comment_likes = QueryForumCommentLikes(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qfcl.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qfcl.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_device_type:
				new_df = qfcl.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			if with_context_name:
				new_df = qfcl.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df

			if with_enrollment_type:
				new_df = qfcl.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df

			if period:
				self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_events_per_course_sections(self):
		group_by_items = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_device_types(self):
		if 'device_type' in self.dataframe.columns:
			group_by_items = ['timestamp_period', 'device_type']
			df = self.build_dataframe(group_by_items)
			return df

	def analyze_enrollment_types(self):
		if 'enrollment_type' in self.dataframe.columns:
			group_by_items = ['timestamp_period', 'enrollment_type']
			df = self.build_dataframe(group_by_items)
			return df

	def build_dataframe(self, group_by_items):
		agg_columns = {	'comment_id'	: pd.Series.count,
						'user_id'		: pd.Series.nunique}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		if df is not None :
			df.rename(columns={	'comment_id'	 :'number_of_likes',
								'user_id'		 :'number_of_unique_users'},
					  inplace=True)
			df['ratio'] = df['number_of_likes'] / df['number_of_unique_users']
		return df

class ForumCommentFavoritesTimeseries(object):
	"""
	analyze the number of forum comment favorites given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, period='daily',
				 with_context_name=True, with_enrollment_type=True):
		self.session = session
		self.period = period
		qfcf = self.query_forum_comment_favorites = QueryForumCommentFavorites(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qfcf.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qfcf.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_device_type:
				new_df = qfcf.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			if with_context_name:
				new_df = qfcf.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df

			if with_enrollment_type:
					new_df = qfcf.add_enrollment_type(self.dataframe, course_id)
					if new_df is not None:
						self.dataframe = new_df

			if period:
				self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_events_per_course_sections(self):
		group_by_items = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_device_types(self):
		if 'device_type' in self.dataframe.columns:
			group_by_items = ['timestamp_period', 'device_type']
			df = self.build_dataframe(group_by_items)
			return df

	def analyze_enrollment_types(self):
		if 'enrollment_type' in self.dataframe.columns:
			group_by_items = ['timestamp_period', 'enrollment_type']
			df = self.build_dataframe(group_by_items)
			return df

	def build_dataframe(self, group_by_items):
		agg_columns = {	'comment_id'	: pd.Series.count,
						'user_id'		: pd.Series.nunique}
		df = analyze_types_(self.dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'comment_id'	 :'number_of_favorites',
								'user_id'		 :'number_of_unique_users'},
					  inplace=True)
			df['ratio'] = df['number_of_favorites'] / df['number_of_unique_users']
		return df
