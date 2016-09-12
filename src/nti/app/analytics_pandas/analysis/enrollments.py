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

from ..queries import QueryCourseDrops
from ..queries import QueryEnrollmentTypes
from ..queries import QueryCourseEnrollments
from ..queries import QueryCourseCatalogViews

from .common import analyze_types_
from .common import add_timestamp_period_

class CourseCatalogViewsTimeseries(object):
	"""
	analyze the number of course catalog views given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, period='daily'):
		self.session = session
		self.period = period
		qccv = self.query_course_catalog_views = QueryCourseCatalogViews(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qccv.filter_by_period_of_time_and_course_id(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qccv.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_device_type:
				new_df = qccv.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def analyze_device_types(self):
		group_by_items = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def build_dataframe(self, group_by_items, base_dataframe):
		agg_columns = {	'time_length'	: np.mean,
						'user_id'		: pd.Series.nunique,
						'session_id'	: pd.Series.count}
		df = analyze_types_(base_dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'user_id'		:'number_of_unique_users',
								'time_length'	:'average_time_length',
								'session_id'	:'number_of_course_catalog_views'},
								inplace=True)
			df['ratio'] = df['number_of_course_catalog_views'] / df['number_of_unique_users']
		return df

class CourseEnrollmentsTimeseries(object):
	"""
	analyze the number of course enrollments given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, period='daily', enrollment_type=True):
		self.session = session
		self.period = period
		qce = self.query_course_enrollments = QueryCourseEnrollments(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qce.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qce.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_device_type:
				new_df = qce.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

			if enrollment_type:
				qet = QueryEnrollmentTypes(session)
				enrollment_type_df = qet.get_enrollment_types()
				self.dataframe = self.dataframe.merge(enrollment_type_df, how='left')

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def analyze_device_enrollment_types(self):
		group_by_items = ['timestamp_period', 'device_type', 'type_name']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def build_dataframe(self, group_by_items, base_dataframe):
		agg_columns = {	'user_id'	: pd.Series.nunique,
						'session_id': pd.Series.nunique}
		df = analyze_types_(base_dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={	'user_id':'number_of_enrollments'}, inplace=True)
		return df

class CourseDropsTimeseries(object):
	"""
	analyze the number of course drops given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_device_type=True, period='daily', enrollment_type=True):

		self.session = session
		self.period = period
		qcd = self.query_course_drops = QueryCourseDrops(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qcd.filter_by_period_of_time_and_course_id(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qcd.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			if with_device_type:
				new_df = qcd.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

			if enrollment_type:
				qet = QueryEnrollmentTypes(session)
				cet = QueryCourseEnrollments(session)
				enrollment_type_df = qet.get_enrollment_types()
				user_enrollment_type_df = cet.filter_by_user_id(course_id)
				user_enrollment_type_df = user_enrollment_type_df.merge(enrollment_type_df)
				self.dataframe = self.dataframe.merge(user_enrollment_type_df, how='left')

	def analyze_events(self):
		group_by_items = ['timestamp_period']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def analyze_device_types(self):
		group_by_items = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def analyze_enrollment_types(self):
		group_by_items = ['timestamp_period', 'type_name']
		df = self.build_dataframe(group_by_items, self.dataframe)
		return df

	def build_dataframe(self, group_by_items, base_dataframe):
		agg_columns = {	'user_id'	: pd.Series.nunique}
		df = analyze_types_(base_dataframe, group_by_items, agg_columns)
		if df is not None:
			df.rename(columns={'user_id':'number_of_course_drops'}, inplace=True)
		return df

class CourseEnrollmentsEventsTimeseries(object):

	def __init__(self, cet, cdt=None, ccvt=None):
		"""
		cet = CourseEnrollmentsTimeseries
		cdt = CourseDropsTimeseries
		ccvt = CourseCatalogViewsTimeseries
		"""
		self.cet = cet
		self.cdt = cdt
		self.ccvt = ccvt
		self.period = cet.period

	def explore_course_enrollments_vs_drops(self):
		df = pd.DataFrame(columns=[	'timestamp_period', 'total_events', 'event_type'])
		if self.cdt is None:
			return df

		cet = self.cet
		cdt = self.cdt

		enrollments_df = cet.analyze_events()
		drops_df = cdt.analyze_events()

		if enrollments_df is not None:
			enrollments_df = self.update_events_dataframe(enrollments_df,
				column_to_rename='number_of_enrollments', event_type='ENROLLMENT')
			df = df.append(enrollments_df)

		if drops_df is not None:
			drops_df = self.update_events_dataframe(drops_df,
				column_to_rename='number_of_course_drops', event_type='DROP')
			df = df.append(drops_df)

		df.reset_index(inplace=True, drop=True)
		return df

	def explore_course_catalog_views_vs_enrollments(self):
		df = pd.DataFrame(columns=[	'timestamp_period', 'total_events', 'event_type'])
		if self.ccvt is None:
			return df
		cet = self.cet
		ccvt = self.ccvt

		enrollments_df = cet.analyze_events()
		catalog_views_df = ccvt.analyze_events()

		if enrollments_df is not None:
			enrollments_df = self.update_events_dataframe(enrollments_df,
				column_to_rename='number_of_enrollments', event_type='ENROLLMENT')
			df = df.append(enrollments_df)

		if catalog_views_df is not None:
			catalog_views_df = self.update_events_dataframe(catalog_views_df,
				column_to_rename='number_of_course_catalog_views', event_type='CATALOG VIEWS')
			df = df.append(catalog_views_df)

		df.reset_index(inplace=True, drop=True)
		return df

	def update_events_dataframe(self, df, column_to_rename, event_type):
		df.rename(columns={column_to_rename:'total_events'}, inplace=True)
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['event_type'] = event_type
		return df
