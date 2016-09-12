#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics_database.profile_views import EntityProfileViews
from nti.analytics_database.profile_views import EntityProfileActivityViews
from nti.analytics_database.profile_views import EntityProfileMembershipViews

from .mixins import TableQueryMixin

from .common import add_application_type_

from . import orm_dataframe

class QueryEntityProfileViews(TableQueryMixin):

	table = EntityProfileViews

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		epv = self.table
		query = self.session.query(epv.timestamp,
								   epv.context_path,
								   epv.time_length,
								   epv.target_id,
								   epv.session_id,
								   epv.user_id).filter(epv.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df

class QueryEntityProfileActivityViews(TableQueryMixin):

	table = EntityProfileActivityViews

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		epav = self.table
		query = self.session.query(epav.timestamp,
								   epav.context_path,
								   epav.time_length,
								   epav.target_id,
								   epav.session_id,
								   epav.user_id).filter(epav.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df

class QueryEntityProfileMembershipViews(TableQueryMixin):

	table = EntityProfileMembershipViews

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		epmv = self.table
		query = self.session.query(epmv.timestamp,
								   epmv.context_path,
								   epmv.time_length,
								   epmv.target_id,
								   epmv.session_id,
								   epmv.user_id).filter(epmv.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df
