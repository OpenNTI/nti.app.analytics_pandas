#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import numpy as np

from nti.analytics_database.enrollments import CourseDrops
from nti.analytics_database.enrollments import EnrollmentTypes
from nti.analytics_database.enrollments import CourseEnrollments
from nti.analytics_database.enrollments import CourseCatalogViews

from .mixins import TableQueryMixin

from .common import add_device_type_

from . import orm_dataframe

class QueryCourseCatalogViews(TableQueryMixin):

	table = CourseCatalogViews

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		ccv = self.table
		query = self.session.query(ccv.timestamp,
								   ccv.course_id,
								   ccv.time_length,
								   ccv.session_id,
								   ccv.user_id,
								   ccv.context_path).filter(ccv.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		ccv = self.table
		query = self.session.query(ccv.timestamp,
								   ccv.time_length,
								   ccv.session_id,
								   ccv.user_id,
								   ccv.context_path).filter(ccv.timestamp.between(start_date, end_date)).filter(ccv.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

class QueryCourseEnrollments(TableQueryMixin):

	table = CourseEnrollments

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		ce = self.table
		query = self.session.query(ce.timestamp,
								   ce.course_id,
								   ce.type_id,
								   ce.session_id,
								   ce.user_id).filter(ce.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		ce = self.table
		query = self.session.query(ce.timestamp,
								   ce.type_id,
								   ce.session_id,
								   ce.user_id,
								   ce.course_id).filter(ce.timestamp.between(start_date, end_date)).filter(ce.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

	def filter_by_user_id(self, courses_id):
		ce = self.table
		query = self.session.query(ce.user_id, ce.type_id).filter(ce.course_id.in_(courses_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_course_id_user_id(self, courses_id, users_id):
		ce = self.table
		query = self.session.query(ce.user_id, ce.type_id).filter(ce.course_id.in_(courses_id)).filter(ce.user_id.in_(users_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def count_enrollments(self, courses_id):
		"""
		given course_id, return the number of users enrolled on those courses
		"""
		ce = self.table
		query = self.session.query(ce.user_id).filter(ce.course_id.in_(courses_id))
		dataframe = orm_dataframe(query, self.columns)
		enrollments_number = dataframe['user_id'].count()
		return enrollments_number

class QueryEnrollmentTypes(TableQueryMixin):

	table = EnrollmentTypes

	def get_enrollment_types(self):
		et = self.table
		query = self.session.query(et.type_id,
								   et.type_name)
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def get_enrollment_types_given_type_id(self, types_id):
		et = self.table
		query = self.session.query(et.type_id,
								   et.type_name).filter(et.type_id.in_(types_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

class QueryCourseDrops(TableQueryMixin):

	table = CourseDrops

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		cd = self.table
		query = self.session.query(cd.timestamp,
								   cd.course_id,
								   cd.session_id,
								   cd.user_id).filter(cd.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		cd = self.table
		query = self.session.query(cd.timestamp,
								   cd.course_id,
								   cd.session_id,
								   cd.user_id).filter(cd.timestamp.between(start_date, end_date)).filter(cd.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

def add_enrollment_type_(session, dataframe, course_ids):
	if 'user_id' not in dataframe.columns:
		return
	users_id = np.unique(dataframe['user_id'].values.ravel())
	if len(users_id) == 1 and users_id[0] is None:
		return
	users_id = users_id[~np.isnan(users_id)].tolist()

	qce = QueryCourseEnrollments(session)
	enrollments_df = qce.filter_by_course_id_user_id(course_ids, users_id)

	types_id = np.unique(enrollments_df['type_id'].values.ravel())
	if len(types_id) == 1 and types_id[0] is None:
		return
	types_id = types_id[~np.isnan(types_id)].tolist()

	qet = QueryEnrollmentTypes(session)
	enrollment_types_df = qet.get_enrollment_types_given_type_id(types_id)
	enrollment_types_df.rename(columns={'type_name':'enrollment_type'}, inplace=True)

	new_df = dataframe.merge(enrollments_df, how='left').merge(enrollment_types_df, how='left')
	return new_df
