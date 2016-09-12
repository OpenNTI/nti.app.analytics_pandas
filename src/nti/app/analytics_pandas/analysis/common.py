#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from datetime import date
from datetime import datetime
from datetime import timedelta

import pandas as pd

from ..queries import QueryUsers

from ..utils import get_values_of_series_categorical_index_

def first_date_of_the_week(year, week):
	ret = datetime.strptime('%04d-%02d-2' % (year, week), '%Y-%W-%w')
	if date(year, 1, 4).isoweekday() > 4:
		ret -= timedelta(days=7)
	return ret

def add_timestamp_period_(df, period_format=u'%Y-%m-%d', time_period='daily'):
	if 'timestamp' in df.columns:
		if time_period == 'weekly':
			df['timestamp_period'] = df['timestamp'].apply(lambda x: first_date_of_the_week(x.year, x.week))
		else:
			df['timestamp_period'] = df['timestamp'].apply(lambda x: x.strftime(period_format))
	return df

def explore_number_of_events_based_timestamp_date_(df):
	if len(df.index) > 0:
		grouped = df.groupby('timestamp_period')
		df.reset_index(inplace=True)
		events_df = grouped.aggregate(pd.Series.nunique)
		return events_df

def explore_unique_users_based_timestamp_date_(df):
	if len(df.index) > 0:
		grouped = df.groupby('timestamp_period')
		unique_users_per_period_df = grouped.aggregate({'user_id': pd.Series.nunique})
		unique_users_per_period_df.rename(columns={'user_id': 'total_unique_users'},
										  inplace=True)
		return unique_users_per_period_df

def explore_ratio_of_events_over_unique_users_based_timestamp_date_(events_df,
																	events_df_column_name,
																	unique_users_df):
	if events_df is not None and unique_users_df is not None:
		merge_df = events_df.join(unique_users_df)
		merge_df['ratio'] = merge_df[events_df_column_name] / merge_df['total_unique_users']
		return merge_df

def analyze_types_(df, group_by_items, agg_columns=None):
	if len(df.index) > 0:
		check = set(group_by_items) & set(df.columns)
		if len(check) == len(group_by_items):
			grouped = df.groupby(group_by_items)
			if agg_columns is not None:
				events_df = grouped.aggregate(agg_columns)
			else:
				events_df = grouped.aggregate(pd.Series.nunique)
			return events_df

def get_most_active_users_(df, session, max_rank_number=10):
	if df is None or df.empty:
		return
	most_active_user_id = df.groupby('user_id').size().sort_values(ascending=False)[:max_rank_number]
	most_active_user_id_df = most_active_user_id.to_frame(name='number_of_activities')
	most_active_user_id_df.reset_index(level=0, inplace=True)

	users_id = get_values_of_series_categorical_index_(most_active_user_id).tolist()
	most_active_user_df = QueryUsers(session).get_username_filter_by_user_id(users_id)

	most_active_user_df = most_active_user_df.merge(most_active_user_id_df)

	most_active_user_df.sort_values(by='number_of_activities', ascending=[0], inplace=True)
	most_active_user_df.reset_index(inplace=True, drop=True)
	return most_active_user_df

def generate_pivot_table_(df, index_columns, values_columns, agg_funcs):
	table = pd.pivot_table(df,
						   index=index_columns,
						   values=values_columns,
						   aggfunc=agg_funcs, fill_value=0)
	return table

def reset_dataframe_(df):
	df.reset_index(inplace=True)
	df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
	return df
