#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics_database.assessments import AssignmentViews
from nti.analytics_database.assessments import AssignmentsTaken
from nti.analytics_database.assessments import AssignmentDetails

from nti.analytics_database.assessments import SelfAssessmentViews
from nti.analytics_database.assessments import SelfAssessmentsTaken
from nti.analytics_database.assessments import SelfAssessmentDetails

from .mixins import TableQueryMixin

from .common import add_device_type_
from .common import add_context_name_
from .common import add_resource_type_

from .enrollments import add_enrollment_type_

from . import orm_dataframe

class QueryAssignmentViews(TableQueryMixin):

	table = AssignmentViews

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		av = self.table
		query = self.session.query(	av.timestamp,
									av.context_path,
									av.course_id,
									av.time_length,
									av.assignment_view_id,
									av.resource_id,
									av.session_id,
									av.user_id,
									av.assignment_id,
									av.entity_root_context_id).filter(av.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_course_id_and_period_of_time(self, start_date=None, end_date=None, course_id=()):
		av = self.table
		query = self.session.query(	av.timestamp,
									av.context_path,
									av.time_length,
									av.assignment_view_id,
									av.resource_id,
									av.session_id,
									av.user_id,
									av.assignment_id,
									av.entity_root_context_id,
									av.course_id).filter(av.timestamp.between(start_date, end_date)).filter(av.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

	def add_resource_type(self, dataframe):
		new_df = add_resource_type_(self.session, dataframe)
		return new_df

	def add_context_name(self, dataframe, course_id):
		new_df = add_context_name_(self.session, dataframe, course_id)
		return new_df

	def add_enrollment_type(self, dataframe, course_id):
		new_df = add_enrollment_type_(self.session, dataframe, course_id)
		return new_df

class QueryAssignmentsTaken(TableQueryMixin):

	table = AssignmentsTaken

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		at = self.table
		query = self.session.query(	at.timestamp,
									at.course_id,
									at.time_length,
									at.submission_id,
									at.assignment_taken_id,
									at.assignment_id,
									at.session_id,
									at.user_id,
									at.is_late).filter(at.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_course_id_and_period_of_time(self, start_date=None, end_date=None, course_id=()):
		at = self.table
		query = self.session.query(	at.timestamp,
									at.time_length,
									at.submission_id,
									at.assignment_taken_id,
									at.assignment_id,
									at.session_id,
									at.user_id,
									at.is_late,
									at.course_id).filter(at.timestamp.between(start_date, end_date)).filter(at.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

	def add_assignment_title(self, dataframe):
		index = dataframe['assignment_id']
		dataframe['assignment_title'] = index.apply(lambda x: self._label_assignment_title(x))
		return dataframe

	@classmethod
	def _label_assignment_title(cls, assignment_id):
		idx = assignment_id.rfind(':') + 1
		title = assignment_id[idx:]
		return title

	def add_context_name(self, dataframe, course_id):
		new_df = add_context_name_(self.session, dataframe, course_id)
		return new_df

	def add_enrollment_type(self, dataframe, course_id):
		new_df = add_enrollment_type_(self.session, dataframe, course_id)
		return new_df

class QueryAssignmentDetails(TableQueryMixin):

	table = AssignmentDetails

	def get_submission_given_assignment_taken_id (self, assignment_taken_ids ):
		ad = self.table
		query = self.session.query(ad.submission,
								   ad.assignment_taken_id).filter(ad.assignment_taken_id.in_(assignment_taken_ids))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe


class QuerySelfAssessmentViews(TableQueryMixin):

	table = SelfAssessmentViews

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		sav = self.table
		query = self.session.query(	sav.timestamp,
									sav.context_path,
									sav.course_id,
									sav.time_length,
									sav.self_assessment_view_id,
									sav.resource_id,
									sav.session_id,
									sav.user_id,
									sav.assignment_id,
									sav.entity_root_context_id).filter(sav.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_course_id_and_period_of_time(self, start_date=None, end_date=None, course_id=()):
		sav = self.table
		query = self.session.query(	sav.timestamp,
									sav.context_path,
									sav.time_length,
									sav.self_assessment_view_id,
									sav.resource_id,
									sav.session_id,
									sav.user_id,
									sav.assignment_id,
									sav.entity_root_context_id,
									sav.course_id).filter(sav.timestamp.between(start_date, end_date)).filter(sav.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

	def add_resource_type(self, dataframe):
		new_df = add_resource_type_(self.session, dataframe)
		return new_df

	def add_context_name(self, dataframe, course_id):
		new_df = add_context_name_(self.session, dataframe, course_id)
		return new_df

	def add_enrollment_type(self, dataframe, course_id):
		new_df = add_enrollment_type_(self.session, dataframe, course_id)
		return new_df

class QuerySelfAssessmentsTaken(TableQueryMixin):

	table = SelfAssessmentsTaken

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		sat = self.table
		query = self.session.query(	sat.timestamp,
									sat.time_length,
									sat.course_id,
									sat.submission_id,
									sat.self_assessment_id,
									sat.assignment_id,
									sat.session_id,
									sat.user_id).filter(sat.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_course_id_and_period_of_time(self, start_date=None, end_date=None, course_id=()):
		sat = self.table
		query = self.session.query(	sat.timestamp,
									sat.time_length,
									sat.submission_id,
									sat.self_assessment_id,
									sat.assignment_id,
									sat.session_id,
									sat.user_id,
									sat.course_id).filter(sat.timestamp.between(start_date, end_date)).filter(sat.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

	def add_context_name(self, dataframe, course_id):
		new_df = add_context_name_(self.session, dataframe, course_id)
		return new_df

	def add_enrollment_type(self, dataframe, course_id):
		new_df = add_enrollment_type_(self.session, dataframe, course_id)
		return new_df

class QuerySelfAssessmentDetails(TableQueryMixin):

	table = SelfAssessmentDetails

	def get_submission_given_self_assessment_id(self, self_assessment_ids ):
		sad = self.table
		query = self.session.query(sad.submission,
								   sad.self_assessment_id).filter(sad.self_assessment_id.in_(self_assessment_ids))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe
