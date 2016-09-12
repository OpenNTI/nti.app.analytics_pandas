#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import numpy as np

import pandas as pd

from ..queries import QueryBookmarksCreated

from ..utils import cast_columns_as_category_

from .common import analyze_types_
from .common import add_timestamp_period_
from .common import get_most_active_users_

class BookmarkCreationTimeseries(object):
	"""
	analyze the number of bookmarks creation given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True,
				 period='daily', with_context_name=True,
				 with_enrollment_type=True):
		self.session = session
		self.period = period
		qbc = self.query_bookmarks_created = QueryBookmarksCreated(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qbc.filter_by_course_id_and_period_of_time(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qbc.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['bookmark_id', 'user_id']

			if with_resource_type:
				new_df = qbc.add_resource_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('resource_type')

			if with_device_type:
				new_df = qbc.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			if with_context_name:
				new_df = qbc.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qbc.add_enrollment_type(self.dataframe, course_id)
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

	def analyze_resource_types(self):
		group_by_items = ['timestamp_period', 'resource_type']
		df = self.build_dataframe(group_by_items)
		if df is not None:
			resource_df = df[['number_of_bookmarks_created']]
			resource_df.reset_index(inplace=True)
			grouped = resource_df.groupby(['resource_type'])
			resource_df = grouped.aggregate({'number_of_bookmarks_created': np.sum})
			return (df, resource_df)
		else:
			return (df, None)

	def analyze_device_types(self):
		group_by_items = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_items)
		return df

	def analyze_enrollment_types(self):
		group_by_items = ['timestamp_period', 'enrollment_type']
		df = self.build_dataframe(group_by_items)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'bookmark_id' 	: pd.Series.nunique,
						'user_id'		: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'bookmark_id'	:'number_of_bookmarks_created',
								'user_id'		:'number_of_unique_users'},
						inplace=True)
			df['ratio'] = df['number_of_bookmarks_created'] / df['number_of_unique_users']
		return df

	def analyze_resource_device_types(self):
		group_by_items = ['timestamp_period', 'resource_type', 'device_type']
		df = self.build_dataframe(group_by_items)
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		users_df = get_most_active_users_(self.dataframe, self.session, max_rank_number)
		if users_df is not None:
			users_df.rename(columns={'number_of_activities': 'number_of_bookmarks_created'},
							inplace=True)
		return users_df
