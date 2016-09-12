#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics_database.resource_views import VideoEvents

from .mixins import TableQueryMixin

from .common import add_device_type_
from .common import add_context_name_
from .common import add_resource_type_

from .enrollments import add_enrollment_type_

from . import orm_dataframe

class QueryVideoEvents(TableQueryMixin):

	table = VideoEvents

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		ve = self.table
		query = self.session.query(ve.video_view_id,
								   ve.timestamp,
								   ve.course_id,
								   ve.resource_id,
								   ve.context_path,
								   ve.time_length,
								   ve.video_event_type,
								   ve.video_start_time,
								   ve.video_end_time,
								   ve.with_transcript,
								   ve.session_id,
								   ve.user_id,
								   ve.play_speed).filter(ve.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		ve = self.table
		query = self.session.query(ve.video_view_id,
								   ve.timestamp,
								   ve.resource_id,
								   ve.context_path,
								   ve.time_length,
								   ve.video_event_type,
								   ve.video_start_time,
								   ve.video_end_time,
								   ve.with_transcript,
								   ve.session_id,
								   ve.user_id,
								   ve.play_speed,
								   ve.course_id).filter(ve.timestamp.between(start_date, end_date)).filter(ve.course_id.in_(course_id))
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
