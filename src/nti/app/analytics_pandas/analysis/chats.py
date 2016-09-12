#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from ..queries import QueryChatsJoined
from ..queries import QueryChatsInitiated

from .common import analyze_types_
from .common import reset_dataframe_
from .common import add_timestamp_period_
from .common import get_most_active_users_

class ChatsInitiatedTimeseries(object):
	"""
	analyze the number of chats initiated
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 period='daily',
				 with_enrollment_type=True):
		self.session = session
		self.period = period
		qci = QueryChatsInitiated(self.session)

		self.dataframe = qci.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_application_type:
				new_df = qci.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_application_types(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'chat_id' 	: pd.Series.nunique,
						'user_id'	: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'chat_id'	:'number_of_chats_initiated',
								'user_id'	:'number_of_unique_users'},
						inplace=True)
			df['ratio'] = df['number_of_chats_initiated'] / df['number_of_unique_users']
			df = reset_dataframe_(df)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_chats_initiated'},
							inplace=True)
		return users_df

class ChatsJoinedTimeseries(object):
	"""
	analyze the number of chats initiated
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 period='daily',
				 with_enrollment_type=True):
		self.session = session
		self.period = period
		qcj = QueryChatsJoined(self.session)

		self.dataframe = qcj.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_application_type:
				new_df = qcj.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

	def get_number_of_users_joining_chat(self):
		group_by_items = ['timestamp_period', 'chat_id']
		df = self.build_dataframe(group_by_items)
		if df is not None:
			df = reset_dataframe_(df)
		return df

	def get_application_types_used_to_join_chats(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'user_id'	: pd.Series.count }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'user_id' :'number_of_users_join_chats'},
						inplace=True)
		return df

	def analyze_number_of_users_join_chats_per_date(self):
		df = self.get_number_of_users_joining_chat()
		if df is not None:
			df = df.groupby(['timestamp_period']).agg({'number_of_users_join_chats' :[pd.Series.mean, pd.Series.sum],
													   'chat_id' : pd.Series.nunique})

			# #should reset multindex dataframe
			levels = df.columns.levels
			labels = df.columns.labels
			df.columns = levels[1][labels[1]]
			df.rename(columns={	'mean' :'average_number_of_users_join_chats',
								'sum'  :'total_number_of_users_join_chats',
								'nunique' :'number_of_chats_created'},
				 	  inplace=True)
			df = reset_dataframe_(df)
			return df

	def analyze_unique_users_per_date(self):
		df = self.dataframe.groupby(['timestamp_period']).agg({'user_id' : pd.Series.nunique})
		if df is not None:
			df.rename(columns={	'user_id' :'number_of_unique_users'},
						inplace=True)
			df = reset_dataframe_(df)
		return df

	def count_number_of_chats_per_date(self, df):
		if not df.empty:
			df = df.groupby(['timestamp_period']).agg({'chat_id' : pd.Series.count})
			df.rename(columns={'chat_id' : 'number_of_chats'}, inplace=True)
			df = reset_dataframe_(df)
		return df

	def analyze_chat_and_group_chat(self):
		df = self.get_number_of_users_joining_chat()
		if df is not None:
			chat_df = df[df['number_of_users_join_chats'] == 2]
			chat_df = self.count_number_of_chats_per_date(chat_df)
			group_chat_df = df[df['number_of_users_join_chats'] > 2]
			group_chat_df = self.count_number_of_chats_per_date(group_chat_df)
			return (chat_df, group_chat_df)

	def count_number_of_one_one_or_group_chat_per_date(self, df):
		if not df.empty:
			df = df.groupby(['timestamp_period', 'chat_type']).agg({'chat_id' : pd.Series.count})
			df.rename(columns={'chat_id' : 'number_of_chats'}, inplace=True)
			df = reset_dataframe_(df)
		return df

	def analyze_one_one_and_group_chat(self):
		df = self.get_number_of_users_joining_chat()
		def label_chat(number_of_users_join_chats):
			if number_of_users_join_chats == 2 :
				return 'one one chat'
			elif number_of_users_join_chats > 2:
				return 'group chat'
			else:
				return 'not a chat'
		index = df['number_of_users_join_chats']
		df['chat_type'] = index.apply(lambda x: label_chat(x))
		df = self.count_number_of_one_one_or_group_chat_per_date(df)
		return df
