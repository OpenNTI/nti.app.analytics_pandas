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
from ..queries import QueryEntityProfileViews
from ..queries import QueryEntityProfileActivityViews
from ..queries import QueryEntityProfileMembershipViews

from ..utils import cast_columns_as_category_
from ..utils import get_values_of_series_categorical_index_

from .common import analyze_types_
from .common import reset_dataframe_
from .common import add_timestamp_period_
from .common import get_most_active_users_

class EntityProfileViewEventsTimeseries(object):
	"""
	combined all profile views related events
	"""

	def __init__(self, epvt=None, epavt=None, epmvt=None):
		"""
		epvt = EntityProfileViewsTimeseries
		epavt = EntityProfileActivityViewsTimeseries
		epmvt = EntityProfileMembershipViewsTimeseries
		"""
		self.epvt = epvt
		self.epavt = epavt
		self.epmvt = epmvt

		if epvt is not None:
			self.period = epvt.period
		elif epavt is not None:
			self.period = epavt.period
		elif epmvt is not None:
			self.period = epmvt.period
		else:
			self.period = None

	def combine_events(self):
		df = pd.DataFrame(columns=[	'timestamp_period', 'total_events', 'event_type'])
		if self.epvt is not None:
			epvt = self.epvt
			profile_views_df = epvt.analyze_events()
			if profile_views_df is not None:
				profile_views_df = self.update_events_dataframe(
												profile_views_df,
												column_to_rename='number_of_profile_views',
												event_type='Profile View')
				df = df.append(profile_views_df)

		if self.epavt is not None:
			epavt = self.epavt
			profile_activity_views_df = epavt.analyze_events()
			if profile_activity_views_df is not None:
				profile_activity_views_df = self.update_events_dataframe(
												profile_activity_views_df,
												column_to_rename='number_of_profile_activity_views',
												event_type='Activity View')
				df = df.append(profile_activity_views_df)

		if self.epmvt is not None:
			epmvt = self.epmvt
			profile_membership_views_df = epmvt.analyze_events()
			if profile_membership_views_df is not None:
				profile_membership_views_df = self.update_events_dataframe(
													profile_membership_views_df,
													column_to_rename='number_of_profile_membership_views',
													event_type='Membership View')
				df = df.append(profile_membership_views_df)

		df.reset_index(inplace=True, drop=True)
		return df

	def update_events_dataframe(self, df, column_to_rename, event_type):
		df.rename(columns={column_to_rename:'total_events'}, inplace=True)
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['event_type'] = event_type
		return df

class EntityProfileViewsTimeseries(object):
	"""
	analyze the profile views
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 period='daily',
				 with_enrollment_type=True):
		self.session = session
		self.period = period
		qepv = QueryEntityProfileViews(self.session)

		self.dataframe = qepv.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['target_id', 'user_id']
			if with_application_type:
				new_df = qepv.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)
			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(self.dataframe, group_by_items)
		return df

	def analyze_application_types(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(self.dataframe, group_by_items)
		return df

	def build_dataframe(self, dataframe, group_by_columns):
		agg_columns = {	'target_id' 	: pd.Series.count,
						'user_id'		: pd.Series.nunique }
		df = analyze_types_(dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'target_id'	:'number_of_profile_views',
								'user_id'	:'number_of_unique_users'},
						inplace=True)
			df['ratio'] = df['number_of_profile_views'] / df['number_of_unique_users']
			df = reset_dataframe_(df)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_profile_views'},
							inplace=True)
		return users_df

	def get_the_most_viewed_profiles(self, max_rank_number=10):
		most_viewed_profiles_df = get_the_most_viewed_profile(df=self.dataframe,
															  field_name='number_of_profile_viewed',
															  max_rank_number=max_rank_number,
															  session=self.session)
		return most_viewed_profiles_df

	def analyze_views_by_owner_or_by_others(self):
		df = self.dataframe.copy(deep=True)
		df['viewers'] = df.apply(lambda x : viewers(x), axis=1)
		group_by_items = ['timestamp_period', 'viewers']
		new_df = self.build_dataframe(df, group_by_items)
		return new_df

class EntityProfileActivityViewsTimeseries(object):
	"""
	analyze the profile activity views
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 period='daily',
				 with_enrollment_type=True):
		self.session = session
		self.period = period
		qepav = QueryEntityProfileActivityViews(self.session)

		self.dataframe = qepav.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['target_id', 'user_id']
			if with_application_type:
				new_df = qepav.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)
			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(self.dataframe, group_by_items)
		return df

	def analyze_application_types(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(self.dataframe, group_by_items)
		return df

	def build_dataframe(self, dataframe, group_by_columns):
		agg_columns = {	'target_id' 	: pd.Series.count,
						'user_id'		: pd.Series.nunique }
		df = analyze_types_(dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'target_id'	:'number_of_profile_activity_views',
								'user_id'	:'number_of_unique_users'},
						inplace=True)
			df['ratio'] = df['number_of_profile_activity_views'] / df['number_of_unique_users']
			df = reset_dataframe_(df)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_profile_activity_views'},
							inplace=True)
		return users_df

	def get_the_most_viewed_profile_activities(self, max_rank_number=10):
		most_viewed_profiles_df = get_the_most_viewed_profile(df=self.dataframe,
															  field_name='number_of_profile_activity_viewed',
															  max_rank_number=max_rank_number,
															  session=self.session)
		return most_viewed_profiles_df

	def analyze_views_by_owner_or_by_others(self):
		df = self.dataframe.copy(deep=True)
		df['viewers'] = df.apply(lambda x : viewers(x), axis=1)
		group_by_items = ['timestamp_period', 'viewers']
		new_df = self.build_dataframe(df, group_by_items)
		return new_df

class EntityProfileMembershipViewsTimeseries(object):
	"""
	analyze the profile membership views
	"""

	def __init__(self, session, start_date, end_date,
				 with_application_type=True,
				 period='daily',
				 with_enrollment_type=True):
		self.session = session
		self.period = period
		qepmv = QueryEntityProfileMembershipViews(self.session)

		self.dataframe = qepmv.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['target_id', 'user_id']
			if with_application_type:
				new_df = qepmv.add_application_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)
			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(self.dataframe, group_by_items)
		return df

	def analyze_application_types(self):
		group_by_items = ['timestamp_period', 'application_type']
		df = self.build_dataframe(self.dataframe, group_by_items)
		return df

	def build_dataframe(self, dataframe, group_by_columns):
		agg_columns = {	'target_id' 	: pd.Series.count,
						'user_id'		: pd.Series.nunique }
		df = analyze_types_(dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'target_id'	:'number_of_profile_membership_views',
								'user_id'	:'number_of_unique_users'},
						inplace=True)
			df['ratio'] = df['number_of_profile_membership_views'] / df['number_of_unique_users']
			df = reset_dataframe_(df)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_profile_membership_views'},
							inplace=True)
		return users_df

	def get_the_most_viewed_profile_memberships(self, max_rank_number=10):
		most_viewed_profiles_df = get_the_most_viewed_profile(df=self.dataframe,
															  field_name='number_of_profile_membership_viewed',
															  max_rank_number=max_rank_number,
															  session=self.session)
		return most_viewed_profiles_df

	def analyze_views_by_owner_or_by_others(self):
		df = self.dataframe.copy(deep=True)
		df['viewers'] = df.apply(lambda x : viewers(x), axis=1)
		group_by_items = ['timestamp_period', 'viewers']
		new_df = self.build_dataframe(df, group_by_items)
		return new_df

def viewers (row):
	if row['user_id'] == row['target_id']:
		return 'owner'
	else:
		return 'others'

def get_the_most_viewed_profile(df, field_name, max_rank_number, session):
	if df is None or df.empty:
		return
	most_viewed_profiles_id = df.groupby('target_id').size().sort_values(ascending=False)[:max_rank_number]
	most_viewed_profiles_df = most_viewed_profiles_id.to_frame(name=field_name)
	most_viewed_profiles_df.reset_index(level=0, inplace=True)

	target_id = get_values_of_series_categorical_index_(most_viewed_profiles_id).tolist()
	target_df = QueryUsers(session).get_username_filter_by_user_id(target_id)
	target_df.rename(columns={'user_id' : 'target_id', 'username': 'profile'},
					 inplace=True)

	most_viewed_profiles_df = target_df.merge(most_viewed_profiles_df)

	most_viewed_profiles_df.sort_values(by=field_name, ascending=[0], inplace=True)
	most_viewed_profiles_df.reset_index(inplace=True, drop=True)
	return most_viewed_profiles_df
