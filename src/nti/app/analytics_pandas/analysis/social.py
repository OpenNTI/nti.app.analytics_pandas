#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from ..queries import QueryContactsAdded
from ..queries import QueryContactsRemoved
from ..queries import QueryFriendsListsMemberAdded
from ..queries import QueryDynamicFriendsListsMemberAdded

from ..utils import cast_columns_as_category_

from .common import analyze_types_
from .common import reset_dataframe_
from .common import add_timestamp_period_
from .common import get_most_active_users_

class ContactsEventsTimeseries(object):
	"""
	combined all contacts related events
	"""
	def __init__(self, cat=None, crt=None):
		"""
		cat = ContactsAddedTimeseries
		crt = ContactsRemovedTimeseries
		"""
		self.cat = cat
		self.crt = crt

		if cat is not None:
			self.period = cat.period
		elif crt is not None:
			self.period = crt.period
		else:
			self.period = None

	def combine_events(self):
		df = pd.DataFrame(columns=[	'timestamp_period', 'total_events', 'event_type'])
		if self.cat is not None:
			cat = self.cat
			contacts_added_df = cat.analyze_events()
			if contacts_added_df is not None:
				contacts_added_df = self.update_events_dataframe(
												contacts_added_df,
												column_to_rename='number_of_contacts_added',
												event_type='Contacts Added')
				df = df.append(contacts_added_df)

		if self.crt is not None:
			crt = self.crt
			contacts_removed_df = crt.analyze_events()
			if contacts_removed_df is not None:
				contacts_removed_df = self.update_events_dataframe(
												contacts_removed_df,
												column_to_rename='number_of_contacts_removed',
												event_type='Contacts Removed')
				df = df.append(contacts_removed_df)

		df.reset_index(inplace=True, drop=True)
		return df

	def update_events_dataframe(self, df, column_to_rename, event_type):
		df.rename(columns={column_to_rename:'total_events'}, inplace=True)
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['event_type'] = event_type
		return df

class ContactsAddedTimeseries(object):
	"""
	analyze the number of contacts added
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 period='daily'):
		self.session = session
		self.period = period
		qca = QueryContactsAdded(self.session)

		self.dataframe = qca.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['user_id']
			if with_application_type:
				new_df = qca.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)
			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_application_types(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'target_id' : pd.Series.count,
						'user_id'	: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'target_id'	:'number_of_contacts_added',
								'user_id'	:'number_of_unique_users'},
						inplace=True)
			df['ratio'] = df['number_of_contacts_added'] / df['number_of_unique_users']
			df = reset_dataframe_(df)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_contacts_added'},
							inplace=True)
		return users_df

class ContactsRemovedTimeseries(object):
	"""
	analyze the number of contacts removed
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 period='daily'):
		self.session = session
		self.period = period
		qcr = QueryContactsRemoved(self.session)

		self.dataframe = qcr.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['user_id']
			if with_application_type:
				new_df = qcr.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)
			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_application_types(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'target_id' : pd.Series.count,
						'user_id'	: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'target_id'	:'number_of_contacts_removed',
								'user_id'	:'number_of_unique_users'},
						inplace=True)
			df['ratio'] = df['number_of_contacts_removed'] / df['number_of_unique_users']
			df = reset_dataframe_(df)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_contacts_removed'},
							inplace=True)
		return users_df

class DynamicFriendsListsMemberAddedTimeseries(object):
	"""
	analyze dynamic friend lists member added
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 period=True):
		self.session = session
		self.period = period
		qdflma = QueryDynamicFriendsListsMemberAdded(session)

		self.dataframe = qdflma.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_application_type:
				new_df = qdflma.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			if period:
				self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

	def get_number_of_friend_list_members(self):
		group_by_items = ['timestamp_period', 'dfl_id']
		df = self.build_dataframe(group_by_items)
		if df is not None:
			df = reset_dataframe_(df)
		return df

	def get_application_types_used_to_add_members(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'target_id'	: pd.Series.count }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'target_id' :'number_of_dynamic_friend_list_members_added'},
						inplace=True)
		return df

	def analyze_number_of_friend_list_members_added(self):
		df = self.get_number_of_friend_list_members()
		if df is not None:
			df = df.groupby(['timestamp_period']).agg({'number_of_dynamic_friend_list_members_added' :[pd.Series.mean, pd.Series.sum],
													   'dfl_id' : pd.Series.nunique})

			levels = df.columns.levels
			labels = df.columns.labels
			df.columns = levels[1][labels[1]]
			df.rename(columns={	'mean' :'average_number_of_dynamic_friend_list_members_added',
								'sum'  :'total_number_of_dynamic_friend_list_members_added',
								'nunique' :'number_of_friend_lists'},
				 	  inplace=True)
			df = reset_dataframe_(df)
			return df

class FriendsListsMemberAddedTimeseries(object):
	"""
	analyze friend lists member added
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 period=True):
		self.session = session
		self.period = period
		qflma = QueryFriendsListsMemberAdded(session)

		self.dataframe = qflma.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_application_type:
				new_df = qflma.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			if period:
				self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

	def get_number_of_friend_list_members(self):
		group_by_items = ['timestamp_period', 'friends_list_id']
		df = self.build_dataframe(group_by_items)
		if df is not None:
			df = reset_dataframe_(df)
		return df

	def get_application_types_used_to_add_members(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'target_id'	: pd.Series.count }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'target_id' :'number_of_friend_list_members_added'},
						inplace=True)
		return df

	def analyze_number_of_friend_list_members_added(self):
		df = self.get_number_of_friend_list_members()
		if df is not None:
			df = df.groupby(['timestamp_period']).agg({'number_of_friend_list_members_added' :[pd.Series.mean, pd.Series.sum],
													   'friends_list_id' : pd.Series.nunique})
			levels = df.columns.levels
			labels = df.columns.labels
			df.columns = levels[1][labels[1]]
			df.rename(columns={	'mean' :'average_number_of_friend_list_members_added',
								'sum'  :'total_number_of_friend_list_members_added',
								'nunique' :'number_of_friend_lists'},
				 	  inplace=True)
			df = reset_dataframe_(df)
			return df
