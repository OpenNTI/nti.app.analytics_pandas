#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics_database.boards import ForumsCreated
from nti.analytics_database.boards import ForumCommentLikes
from nti.analytics_database.boards import ForumCommentsCreated
from nti.analytics_database.boards import ForumCommentFavorites

from .common import add_device_type_
from .common import add_context_name_

from .enrollments import add_enrollment_type_

from .mixins import TableQueryMixin

from . import orm_dataframe

class QueryForumsCreated(TableQueryMixin):

	table = ForumsCreated

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		tc = self.table
		query = self.session.query(tc.timestamp,
								   tc.course_id,
								   tc.forum_ds_id,
								   tc.user_id,
								   tc.session_id,
								   tc.forum_id,
								   tc.deleted,
								   tc.entity_root_context_id).filter(tc.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		tc = self.table
		query = self.session.query(tc.timestamp,
								   tc.course_id,
								   tc.forum_ds_id,
								   tc.user_id,
								   tc.session_id,
								   tc.forum_id,
								   tc.deleted,
								   tc.entity_root_context_id).filter(tc.timestamp.between(start_date, end_date)).filter(tc.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df


class QueryForumsCommentsCreated(TableQueryMixin):

	table = ForumCommentsCreated

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		fcc = self.table
		query = self.session.query(fcc.timestamp,
								   fcc.course_id,
								   fcc.user_id,
								   fcc.topic_id,
								   fcc.session_id,
								   fcc.favorite_count,
								   fcc.like_count,
								   fcc.comment_length,
								   fcc.comment_id,
								   fcc.forum_id,
								   fcc.parent_id,
								   fcc.parent_user_id,
								   fcc.is_flagged,
								   fcc.deleted).filter(fcc.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		fcc = self.table
		query = self.session.query(fcc.timestamp,
								   fcc.user_id,
								   fcc.topic_id,
								   fcc.session_id,
								   fcc.favorite_count,
								   fcc.like_count,
								   fcc.comment_length,
								   fcc.comment_id,
								   fcc.forum_id,
								   fcc.parent_id,
								   fcc.parent_user_id,
								   fcc.is_flagged,
								   fcc.deleted,
								   fcc.course_id).filter(fcc.timestamp.between(start_date, end_date)).filter(fcc.course_id.in_(course_id))
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

class QueryForumCommentFavorites(TableQueryMixin):

	table = ForumCommentFavorites

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		fcf = self.table
		query = self.session.query(fcf.timestamp,
								   fcf.session_id,
								   fcf.user_id,
								   fcf.comment_id,
								   fcf.creator_id,
								   fcf.course_id).filter(fcf.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		fcf = self.table
		query = self.session.query(fcf.timestamp,
								   fcf.session_id,
								   fcf.user_id,
								   fcf.comment_id,
								   fcf.creator_id).filter(fcf.timestamp.between(start_date, end_date)).filter(fcf.course_id.in_(course_id))
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

class QueryForumCommentLikes(TableQueryMixin):

	table = ForumCommentLikes

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		fcl = ForumCommentLikes
		query = self.session.query(fcl.timestamp,
								   fcl.session_id,
								   fcl.user_id,
								   fcl.comment_id,
								   fcl.creator_id,
								   fcl.course_id).filter(fcl.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		fcl = ForumCommentLikes
		query = self.session.query(fcl.timestamp,
								   fcl.session_id,
								   fcl.user_id,
								   fcl.comment_id,
								   fcl.creator_id,
								   fcl.course_id).filter(fcl.timestamp.between(start_date, end_date)).filter(fcl.course_id.in_(course_id))
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
