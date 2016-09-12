#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import numpy as np

from nti.analytics_database.resource_tags import NoteLikes
from nti.analytics_database.resource_tags import NotesViewed
from nti.analytics_database.resource_tags import NotesCreated
from nti.analytics_database.resource_tags import NoteFavorites

from .mixins import TableQueryMixin

from .common import add_device_type_
from .common import add_context_name_
from .common import add_resource_type_

from .enrollments import add_enrollment_type_

from . import orm_dataframe

class QueryNotesCreated(TableQueryMixin):

	table = NotesCreated

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		nc = self.table
		query = self.session.query(nc.note_id,
								   nc.timestamp,
								   nc.course_id,
								   nc.resource_id,
								   nc.user_id,
								   nc.parent_id,
								   nc.parent_user_id,
								   nc.session_id,
								   nc.sharing,
								   nc.favorite_count,
								   nc.like_count,
								   nc.note_length,
								   nc.is_flagged,
								   nc.deleted).filter(nc.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		nc = self.table
		query = self.session.query(nc.note_id,
								   nc.timestamp,
								   nc.resource_id,
								   nc.user_id,
								   nc.parent_id,
								   nc.parent_user_id,
								   nc.session_id,
								   nc.sharing,
								   nc.favorite_count,
								   nc.like_count,
								   nc.note_length,
								   nc.is_flagged,
								   nc.deleted,
								   nc.course_id).filter(nc.timestamp.between(start_date, end_date)).filter(nc.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_resource_type(self, dataframe):
		new_df = add_resource_type_(self.session, dataframe)
		return new_df

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

	def add_context_name(self, dataframe, course_id):
		new_df = add_context_name_(self.session, dataframe, course_id)
		return new_df

	def add_enrollment_type(self, dataframe, course_id):
		new_df = add_enrollment_type_(self.session, dataframe, course_id)
		return new_df

	def get_author_id_filter_by_note_id(self, notes_id):
		nc = self.table
		query = self.query(nc.note_id,
							nc.user_id).filter(nc.note_id.in_(notes_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def get_sharing_type_filter_by_note_id(self, notes_id):
		nc = self.table
		query = self.query(nc.note_id, nc.sharing).filter(nc.note_id.in_(notes_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def get_resource_id_filter_by_note_id(self, notes_id):
		nc = self.table
		query = self.query(nc.note_id, nc.resource_id).filter(nc.note_id.in_(notes_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

class QueryNotesViewed(TableQueryMixin):

	table = NotesViewed

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		nv = self.table
		query = self.session.query(nv.note_id,
								   nv.timestamp,
								   nv.course_id,
								   nv.user_id,
								   nv.session_id,
								   nv.resource_id,
								   nv.context_path).filter(nv.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		nv = self.table
		query = self.session.query(nv.note_id,
								   nv.timestamp,
								   nv.user_id,
								   nv.session_id,
								   nv.resource_id,
								   nv.context_path,
								   nv.course_id).filter(nv.timestamp.between(start_date, end_date)).filter(nv.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_resource_type(self, dataframe):
		new_df = add_resource_type_(self.session, dataframe)
		return new_df

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

	def add_sharing_type(self, dataframe):
		new_df = add_sharing_type_(self.session, dataframe)
		return new_df

	def add_context_name(self, dataframe, course_id):
		new_df = add_context_name_(self.session, dataframe, course_id)
		return new_df

	def add_enrollment_type(self, dataframe, course_id):
		new_df = add_enrollment_type_(self.session, dataframe, course_id)
		return new_df

class QueryNoteFavorites(TableQueryMixin):

	table = NoteFavorites

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		nf = self.table
		query = self.session.query(nf.note_id,
								   nf.timestamp,
								   nf.course_id,
								   nf.user_id,
								   nf.session_id,
								   nf.creator_id).filter(nf.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		nf = self.table
		query = self.session.query(nf.note_id,
								   nf.timestamp,
								   nf.user_id,
								   nf.session_id,
								   nf.creator_id,
								   nf.course_id).filter(nf.timestamp.between(start_date, end_date)).filter(nf.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_resource_type(self, dataframe):
		if 'note_id' in dataframe:
			notes_id = np.unique(dataframe['note_id'].values.ravel())
			if len(notes_id) == 1 and notes_id[0] is None:
				return
			notes_id = notes_id[~np.isnan(notes_id)].tolist()
			qnc = QueryNotesCreated(self.session)
			resource_df = qnc.get_resource_id_filter_by_note_id(notes_id)
			dataframe = dataframe.merge(resource_df, how='left')
			new_df = add_resource_type_(self.session, dataframe)
			return new_df

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

	def add_context_name(self, dataframe, course_id):
		new_df = add_context_name_(self.session, dataframe, course_id)
		return new_df

	def add_enrollment_type(self, dataframe, course_id):
		new_df = add_enrollment_type_(self.session, dataframe, course_id)
		return new_df

class QueryNoteLikes(TableQueryMixin):

	table = NoteLikes

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		nl = self.table
		query = self.session.query(nl.note_id,
								   nl.timestamp,
								   nl.course_id,
								   nl.user_id,
								   nl.session_id,
								   nl.creator_id).filter(nl.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_period_of_time_and_course_id(self, start_date=None, end_date=None, course_id=()):
		nl = self.table
		query = self.session.query(nl.note_id,
								   nl.timestamp,
								   nl.user_id,
								   nl.session_id,
								   nl.creator_id,
								   nl.course_id).filter(nl.timestamp.between(start_date, end_date)).filter(nl.course_id.in_(course_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_resource_type(self, dataframe):
		if 'note_id' in dataframe:
			notes_id = np.unique(dataframe['note_id'].values.ravel())
			if len(notes_id) == 1 and notes_id[0] is None:
				return
			notes_id = notes_id[~np.isnan(notes_id)].tolist()
			qnc = QueryNotesCreated(self.session)
			resource_df = qnc.get_resource_id_filter_by_note_id(notes_id)
			dataframe = dataframe.merge(resource_df, how='left')
			new_df = add_resource_type_(self.session, dataframe)
			return new_df

	def add_device_type(self, dataframe):
		new_df = add_device_type_(self.session, dataframe)
		return new_df

	def add_context_name(self, dataframe, course_id):
		new_df = add_context_name_(self.session, dataframe, course_id)
		return new_df

	def add_enrollment_type(self, dataframe, course_id):
		new_df = add_enrollment_type_(self.session, dataframe, course_id)
		return new_df

def add_sharing_type_(session, dataframe):
	if 'note_id' in dataframe:
		notes_id = np.unique(dataframe['note_id'].values.ravel())
		if len(notes_id) == 1 and notes_id[0] is None:
			return
		notes_id = notes_id[~np.isnan(notes_id)].tolist()
		qnc = QueryNotesCreated(session)
		notes_df = qnc.get_sharing_type_filter_by_note_id(notes_id)
		new_df = dataframe.merge(notes_df, how='left')
		return new_df
