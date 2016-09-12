#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from sqlalchemy import and_

from nti.analytics_database.root_context import Courses

from .mixins import TableQueryMixin

from . import orm_dataframe

class QueryCourses(TableQueryMixin):

	table = Courses

	def filter_by_context_name(self, context_name):
		c = self.table
		query = self.session.query( c.context_id,
									c.context_ds_id,
									c.context_name,
									c.context_long_name,
									c.start_date,
									c.end_date,
									c.duration,
									c.term,
									c.crn).filter(c.context_name.like(context_name)).all()
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def filter_by_context_ids(self, context_ids):
		c = self.table
		query = self.session.query( c.context_id,
									c.context_ds_id,
									c.context_name,
									c.context_long_name,
									c.start_date,
									c.end_date,
									c.duration,
									c.term,
									c.crn).filter(c.context_id.in_(context_ids))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def get_context_name(self, context_ids):
		c = self.table
		query = self.session.query(c.context_id, c.context_name).filter(c.context_id.in_(context_ids))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def get_course_id(self, context_name, start_date=None, end_date=None):
		c = self.table
		query = self.session.query(c.context_id).filter(c.context_name.like(context_name))
		if start_date is not None and end_date is not None:
			query = query.filter(and_(c.start_date >= start_date, c.end_date <= end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe
