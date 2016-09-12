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

from ..queries import QueryResources
from ..queries import QueryCourseResourceViews

from ..utils import cast_columns_as_category_
from ..utils import get_values_of_series_categorical_index_

from .common import analyze_types_
from .common import add_timestamp_period_
from .common import get_most_active_users_

class ResourceViewsTimeseries(object):
	"""
	analyze the number of resource views given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True,
				 period='daily', with_context_name=True,
				 with_enrollment_type=True):
		self.session = session
		self.end_date = end_date
		self.start_date = start_date
		self.period = period
		qrv = self.query_resources_view = QueryCourseResourceViews(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qrv.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qrv.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['resource_id', 'user_id']
			if with_device_type:
				new_df = qrv.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			if with_resource_type:
				new_df = qrv.add_resource_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('resource_type')

			if with_context_name:
				new_df = qrv.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qrv.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('enrollment_type')

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)
			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		"""
		Group course resource views dataframe by timestamp_period
		Count the number of unique users, number of resource views
		and number of unique resources in each group return the result as dataframe
		"""
		group_by_columns = ['timestamp_period']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_per_course_sections(self):
		"""
		Analyze course resource views per course sections
		Return a dataframe consisting of:
		- number of unique users,
		- number of resource views
		- number of unique resources
		"""
		group_by_columns = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_based_on_resource_type(self):
		"""
		group course resource views dataframe by timestamp_period and resource_type
		count the number of unique users, number of resource views and number of unique
		resources in each group return the result as dataframe

		"""
		group_by_columns = ['timestamp_period', 'resource_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_based_on_device_type(self):
		"""
		group course resource views dataframe by timestamp_period and device_type
		count the number of unique users, number of resource views and number of unique
		resources in each group return the result as dataframe

		"""
		group_by_columns = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_based_on_enrollment_type(self):
		"""
		group course resource views dataframe by timestamp_period and enrollment_type
		count the number of unique users, number of resource views and number of unique
		resources in each group return the result as dataframe

		"""
		group_by_columns = ['timestamp_period', 'enrollment_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_based_on_resource_device_type(self):
		"""
		group course resource views dataframe by timestamp_period, resource_type and
		device_type count the number of unique users, number of resource views and
		number of unique resources in each group return the result as dataframe

		"""
		group_by_columns = ['timestamp_period', 'resource_type', 'device_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'user_id'			: pd.Series.nunique,
						'resource_view_id' 	: pd.Series.count,
						'resource_id'		: pd.Series.nunique}
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'user_id'	:'number_of_unique_users',
								'resource_view_id'	:'number_of_resource_views',
								'resource_id': 'number_of_unique_resource'},
						inplace=True)
			df['ratio'] = df['number_of_resource_views'] / df['number_of_unique_users']
		return df

	def get_the_most_active_users(self, max_rank_number=10):
		"""
		find n-most active users, return dataframe having user_id and username columns
		"""
		return get_most_active_users_(self.dataframe, self.session, max_rank_number)

	def get_the_most_viewed_resources(self, max_rank_number=10):
		"""
		find the top n most viewed resources
		return a dataframe with columns:
			resource_id, resource_display_name, resource_type, and number_of_views
		"""
		temp_df = self.dataframe

		most_views = temp_df.groupby('resource_id').size().order(ascending=False)[:max_rank_number]
		df = most_views.to_frame(name='number_of_views')
		df.reset_index(level=0, inplace=True)

		resources_id = get_values_of_series_categorical_index_(most_views).tolist()
		qr = QueryResources(self.session)
		resource_df = qr.get_resource_display_name_given_id(resources_id)
		resource_df.reset_index(inplace=True, drop=True)

		resource_type_df = temp_df[['resource_id', 'resource_type']][temp_df['resource_id'].isin(resources_id)]
		resource_type_df.drop_duplicates(subset=['resource_id', 'resource_type'], inplace=True)
		resource_type_df.reset_index(inplace=True, drop=True)

		df = df.merge(resource_df).merge(resource_type_df)
		return df

	def analyze_user_activities_on_resource_views(self):
		"""
		analyze how users viewing resources based on resource and device type
		"""
		df = self.dataframe
		group_by_columns = ['timestamp_period', 'user_id', 'resource_type', 'device_type']
		agg_columns = { 'time_length': [np.mean, np.sum],
						'resource_id': pd.Series.nunique,
						'resource_view_id': pd.Series.count }
		result = df.groupby(group_by_columns).aggregate(agg_columns)
		result.reset_index(inplace=True)
		result.rename(columns={	'resource_id' 		: 'number_of_unique_resource',
								'resource_view_id'	: 'number_of_resource_views' },
					  inplace=True)
		return result
