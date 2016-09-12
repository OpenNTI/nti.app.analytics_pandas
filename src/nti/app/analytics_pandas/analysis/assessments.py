#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import ast
import pandas as pd

from nti.analytics_pandas.analysis.common import analyze_types_
from nti.analytics_pandas.analysis.common import add_timestamp_period_

from nti.analytics_pandas.queries import QueryAssignmentViews
from nti.analytics_pandas.queries import QueryAssignmentsTaken
from nti.analytics_pandas.queries import QueryAssignmentDetails
from nti.analytics_pandas.queries import QueryCourseEnrollments
from nti.analytics_pandas.queries import QuerySelfAssessmentViews
from nti.analytics_pandas.queries import QuerySelfAssessmentsTaken

from nti.analytics_pandas.utils import cast_columns_as_category_
from nti.analytics_pandas.utils import get_values_of_series_categorical_index_

class AssessmentEventsTimeseries(object):

	def __init__(self, avt=None, att=None, savt=None, satt=None):
		"""
		avt = AssignmentViewsTimeseries
		att = AssignmentsTakenTimeseries
		savt = SelfAssessmentViewsTimeseries
		satt = SelfAssessmentsTakenTimeseries
		"""
		self.avt = avt
		self.att = att
		self.savt = savt
		self.satt = satt

		if self.avt is not None:
			self.period = avt.period
		elif self.att is not None:
			self.period = att.period
		elif self.savt is not None:
			self.period = savt.period
		elif self.satt is not None:
			self.period = satt.period

	def combine_events(self):
		df = pd.DataFrame(columns=[	'timestamp_period', 'total_events', 'event_type'])
		if self.avt is not None:
			avt = self.avt
			assignment_views_df = avt.analyze_events()
			if assignment_views_df is not None:
				assignment_views_df = self.update_events_dataframe(assignment_views_df,
					column_to_rename='number_assignments_viewed',
					event_type='Assignment View')
				df = df.append(assignment_views_df)

		if self.att is not None:
			att = self.att
			assignments_taken_df = att.analyze_events()
			if assignments_taken_df is not None:
				assignments_taken_df = self.update_events_dataframe(assignments_taken_df,
					column_to_rename='number_assignments_taken',
					event_type='Assignment Taken')
				df = df.append(assignments_taken_df)

		if self.savt is not None:
			savt = self.savt
			self_assessment_views_df = savt.analyze_events()
			if self_assessment_views_df is not None:
				self_assessment_views_df = self.update_events_dataframe(self_assessment_views_df,
					column_to_rename='number_self_assessments_viewed',
					event_type='Self Asst. View')
				df = df.append(self_assessment_views_df)

		if self.satt is not None:
			satt = self.satt
			self_assessments_taken_df = satt.analyze_events()
			if self_assessments_taken_df is not None:
				self_assessments_taken_df = self.update_events_dataframe(self_assessments_taken_df,
					column_to_rename='number_self_assessments_taken',
					event_type='Self Asst. Taken')
				df = df.append(self_assessments_taken_df)

		df.reset_index(inplace=True, drop=True)
		return df

	def update_events_dataframe(self, df, column_to_rename, event_type):
		df.rename(columns={column_to_rename:'total_events'}, inplace=True)
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['event_type'] = event_type
		return df

	def analyze_assessments_taken_over_total_enrollments(self):
		if self.att is None or self.satt is None:
			return
		att = self.att
		satt = self.satt
		assignments_df = att.analyze_assignment_taken_over_total_enrollments_ts()
		self_assessment_df = satt.analyze_self_assessments_taken_over_total_enrollments_ts()

		if assignments_df is None or self_assessment_df is None:
			return

		assignments_df['assessment_type'] = 'assignments'
		self_assessment_df['assessment_type'] = 'self assessment'
		df = assignments_df.append(self_assessment_df)
		return df

class AssignmentViewsTimeseries(object):
	"""
	analyze the number of assignment views given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True,
				 period='daily', with_context_name=True,
				 with_enrollment_type=True):

		self.session = session
		self.period = period
		qav = self.query_assignment_view = QueryAssignmentViews(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qav.filter_by_course_id_and_period_of_time(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qav.filter_by_period_of_time(start_date, end_date)

		categorical_columns = ['assignment_view_id', 'user_id']

		if not self.dataframe.empty:
			if with_resource_type:
				new_df = qav.add_resource_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('resource_type')

			if with_device_type:
				new_df = qav.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

			if with_context_name:
				new_df = qav.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qav.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('enrollment_type')

			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		"""
		return a dataframe contains:
		 - the number of assignment views,
		 - the number of unique user viewing assignment
		 - ratio of assignment views over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_per_course_sections(self):
		"""
		return a dataframe contains:
		 - the number of assignment views,
		 - the number of unique user viewing assignment
		 - ratio of assignment views over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_group_by_device_type(self):
		"""
		return a dataframe contains:
		 - the number of assignment views,
		 - the number of unique user viewing assignment
		 - ratio of assignment views over unique users
		grouped by device type on each available date
		"""
		group_by_columns = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_group_by_enrollment_type(self):
		"""
		return a dataframe contains:
		 - the number of assignment views,
		 - the number of unique user viewing assignment
		 - ratio of assignment views over unique users
		grouped by enrollment type on each available date
		"""
		group_by_columns = ['timestamp_period', 'enrollment_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_group_by_resource_type(self):
		"""
		return a dataframe contains:
		 - the number of assignment views,
		 - the number of unique user viewing assignment
		 - ratio of assignment views over unique users
		grouped by device type on each available date
		"""
		group_by_columns = ['timestamp_period', 'resource_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'assignment_view_id': pd.Series.count,
						'user_id'			: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'assignment_view_id':'number_assignments_viewed',
								'user_id'			:'number_of_unique_users'},
					  inplace=True)
			df['ratio'] = df['number_assignments_viewed'] / df['number_of_unique_users']
		return df

class AssignmentsTakenTimeseries(object):
	"""
	analyze the number of assignments taken given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True,
				 period='daily', with_assignment_title=True,
				 with_context_name=True, with_enrollment_type=True):

		self.session = session
		self.period = period
		self.course_id = course_id
		qat = self.query_assignments_taken = QueryAssignmentsTaken(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qat.filter_by_course_id_and_period_of_time(start_date,
																		end_date,
																		course_id)
		else:
			self.dataframe = qat.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['user_id']

			if with_device_type:
				new_df = qat.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

			if with_assignment_title:
				new_df = qat.add_assignment_title(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('assignment_title')

			if with_context_name:
				new_df = qat.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qat.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('enrollment_type')

			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		"""
		return a dataframe contains:
		 - the number of assignments taken
		 - the number of unique user taking assignments
		 - ratio of assignments taken over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_per_course_sections(self):
		"""
		return a dataframe contains:
		 - the number of assignments taken
		 - the number of unique user taking assignments
		 - ratio of assignments taken over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_group_by_device_type(self):
		"""
		return a dataframe contains:
		 - the number of assignments taken
		 - the number of unique user taking assignments
		 - ratio of assignments taken over unique users
		grouped by device type on each available date
		"""
		group_by_columns = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_group_by_enrollment_type(self):
		"""
		return a dataframe contains:
		 - the number of assignments taken
		 - the number of unique user taking assignments
		 - ratio of assignments taken over unique users
		grouped by enrollment type on each available date
		"""
		group_by_columns = ['timestamp_period', 'enrollment_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'assignment_taken_id'	: pd.Series.count,
						'user_id'				: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'assignment_taken_id'	:'number_assignments_taken',
								'user_id'				:'number_of_unique_users'},
					  inplace=True)
			df['ratio'] = df['number_assignments_taken'] / df['number_of_unique_users']
		return df

	def analyze_assignment_taken_over_total_enrollments(self):
		if not self.dataframe.empty:
			dataframe = self.dataframe[['assignment_title', 'assignment_taken_id']]
			group_by_columns = ['assignment_title']
			agg_columns = {'assignment_taken_id' : pd.Series.count}

			df = analyze_types_(dataframe, group_by_columns, agg_columns)
			df.rename(columns={'assignment_taken_id' :'number_assignments_taken'}, inplace=True)

			qce = QueryCourseEnrollments(self.session)
			total_enrollments = qce.count_enrollments(self.course_id)

			df['ratio'] = df['number_assignments_taken'] / total_enrollments
			return df

	def analyze_assignment_taken_over_total_enrollments_ts(self):
		if not self.dataframe.empty:
			dataframe = self.dataframe[['assignment_taken_id', 'timestamp_period']]
			group_by_columns = ['timestamp_period']
			agg_columns = {'assignment_taken_id' : pd.Series.count}

			df = analyze_types_(dataframe, group_by_columns, agg_columns)
			df.rename(columns={'assignment_taken_id' :'assignments_taken'}, inplace=True)

			qce = QueryCourseEnrollments(self.session)
			total_enrollments = qce.count_enrollments(self.course_id)

			df['ratio'] = df['assignments_taken'] / total_enrollments
			return df

	def analyze_question_types(self):
		token = self.dataframe['assignment_taken_id']
		assignment_taken_ids = get_values_of_series_categorical_index_(token).tolist()
		qad = QueryAssignmentDetails(self.session)
		assignment_details_df = qad.get_submission_given_assignment_taken_id(assignment_taken_ids)
		assignment_details_df['question_type'] = \
				assignment_details_df['submission'].apply(lambda x: get_question_type(x))
		df = self.dataframe[['timestamp_period', 'assignment_taken_id']]
		new_df = assignment_details_df.merge(df, how='left')
		return new_df

def get_question_type(submission_value):
	try:
		value = ast.literal_eval(submission_value)
		if value == "<FILE_UPLOADED>":
			return 'file upload'
		elif isinstance(value, dict):
			return 'order/matching'
		elif isinstance(value, list):
			return 'multiple choice multiple answer'
		elif isinstance(value, int):
			return 'multiple choice'
		else:
			count_space = value.count(' ')
			if count_space > 25:
				return 'essay'
			else:
				return 'free response'
	except ValueError:
		return 'null'

class SelfAssessmentViewsTimeseries(object):
	"""
	analyze the number of self assessments views given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True,
				 period='daily', with_context_name=True,
				 with_enrollment_type=True):

		self.session = session
		self.period = period
		qsav = self.query_self_assessment_view = QuerySelfAssessmentViews(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qsav.filter_by_course_id_and_period_of_time(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qsav.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['self_assessment_view_id', 'user_id']
			if with_resource_type:
				new_df = qsav.add_resource_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('resource_type')

			if with_device_type:
				new_df = qsav.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)

			if with_context_name:
				new_df = qsav.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qsav.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('enrollment_type')

			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		"""
		return a dataframe contains:
		 - the number of self assessments views,
		 - the number of unique user viewing self assessments
		 - ratio of self assessments views over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_per_course_sections(self):
		"""
		return a dataframe contains:
		 - the number of self assessments views,
		 - the number of unique user viewing self assessments
		 - ratio of self assessments views over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_group_by_device_type(self):
		"""
		return a dataframe contains:
		 - the number of self assessments views,
		 - the number of unique user viewing self assessments
		 - ratio of self assessments views over unique users
		grouped by device type on each available date
		"""
		if 'device_type' in self.dataframe.columns:
			group_by_columns = ['timestamp_period', 'device_type']
			df = self.build_dataframe(group_by_columns)
			return df

	def analyze_events_group_by_enrollment_type(self):
		"""
		return a dataframe contains:
		 - the number of self assessments views,
		 - the number of unique user viewing self assessments
		 - ratio of self assessments views over unique users
		grouped by enrollment type on each available date
		"""
		if 'device_type' in self.dataframe.columns:
			group_by_columns = ['timestamp_period', 'enrollment_type']
			df = self.build_dataframe(group_by_columns)
			return df

	def analyze_events_group_by_resource_type(self):
		"""
		return a dataframe contains:
		 - the number of self assessments views,
		 - the number of unique user viewing self assessments
		 - ratio of self assessments views over unique users
		grouped by device type on each available date
		"""
		if 'resource_type' in self.dataframe.columns:
			group_by_columns = ['timestamp_period', 'resource_type']
			df = self.build_dataframe(group_by_columns)
			return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'self_assessment_view_id'	: pd.Series.count,
						'user_id'					: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'self_assessment_view_id'	:'number_self_assessments_viewed',
								'user_id'					:'number_of_unique_users'},
					  inplace=True)
			df['ratio'] = df['number_self_assessments_viewed'] / df['number_of_unique_users']
		return df

class SelfAssessmentsTakenTimeseries(object):
	"""
	analyze the number of self assessments taken given time period and list of course id
	"""

	def __init__(self, session, start_date, end_date, course_id=None,
				 with_resource_type=True, with_device_type=True,
				 period='daily', with_context_name=True,
				 with_enrollment_type=True):

		self.session = session
		self.period = period
		self.course_id = course_id
		qsat = self.query_self_assessments_taken = QuerySelfAssessmentsTaken(self.session)
		if isinstance (course_id, (tuple, list)):
			self.dataframe = qsat.filter_by_course_id_and_period_of_time(start_date,
																		 end_date,
																		 course_id)
		else:
			self.dataframe = qsat.filter_by_period_of_time(start_date, end_date)

		if not self.dataframe.empty:
			categorical_columns = ['self_assessment_id', 'user_id']

			if with_device_type:
				new_df = qsat.add_device_type(self.dataframe)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('device_type')

			if with_context_name:
				new_df = qsat.add_context_name(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('context_name')

			if with_enrollment_type:
				new_df = qsat.add_enrollment_type(self.dataframe, course_id)
				if new_df is not None:
					self.dataframe = new_df
					categorical_columns.append('enrollment_type')

			self.dataframe = add_timestamp_period_(self.dataframe, time_period=period)
			self.dataframe = cast_columns_as_category_(self.dataframe, categorical_columns)

	def analyze_events(self):
		"""
		return a dataframe contains:
		 - the number of self assessments taken
		 - the number of unique user taking self assessments
		 - ratio of self assessments taken over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_per_course_sections(self):
		"""
		return a dataframe contains:
		 - the number of self assessments taken
		 - the number of unique user taking self assessments
		 - ratio of self assessments taken over unique users
		on each available date
		"""
		group_by_columns = ['timestamp_period', 'course_id', 'context_name']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_group_by_device_type(self):
		"""
		return a dataframe contains:
		 - the number of self assessments taken
		 - the number of unique user taking self assessments
		 - ratio of self assessments taken over unique users
		grouped by device type on each available date
		"""
		group_by_columns = ['timestamp_period', 'device_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def analyze_events_group_by_enrollment_type(self):
		"""
		return a dataframe contains:
		 - the number of self assessments taken
		 - the number of unique user taking self assessments
		 - ratio of self assessments taken over unique users
		grouped by enrollment type on each available date
		"""
		group_by_columns = ['timestamp_period', 'enrollment_type']
		df = self.build_dataframe(group_by_columns)
		return df

	def build_dataframe(self, group_by_columns):
		agg_columns = {	'self_assessment_id'	: pd.Series.count,
						'user_id'				: pd.Series.nunique }
		df = analyze_types_(self.dataframe, group_by_columns, agg_columns)
		if df is not None:
			df.rename(columns={	'self_assessment_id'	:'number_self_assessments_taken',
								'user_id'				:'number_of_unique_users'},
						inplace=True)
			df['ratio'] = df['number_self_assessments_taken'] / df['number_of_unique_users']
		return df

	def analyze_self_assessments_taken_over_total_enrollments_ts(self):
		if not self.dataframe.empty:
			dataframe = self.dataframe[['self_assessment_id', 'timestamp_period']]
			group_by_columns = ['timestamp_period']
			agg_columns = {'self_assessment_id' : pd.Series.count}

			df = analyze_types_(dataframe, group_by_columns, agg_columns)
			df.rename(columns={'self_assessment_id' :'self_assessment_taken'}, inplace=True)

			qce = QueryCourseEnrollments(self.session)
			total_enrollments = qce.count_enrollments(self.course_id)

			df['ratio'] = df['self_assessment_taken'] / total_enrollments
			return df
