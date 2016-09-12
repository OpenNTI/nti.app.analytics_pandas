#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics_database.social import ContactsAdded
from nti.analytics_database.social import ContactsRemoved
from nti.analytics_database.social import FriendsListsCreated
from nti.analytics_database.social import FriendsListsMemberAdded
from nti.analytics_database.social import FriendsListsMemberRemoved
from nti.analytics_database.social import DynamicFriendsListsCreated
from nti.analytics_database.social import DynamicFriendsListsMemberAdded
from nti.analytics_database.social import DynamicFriendsListsMemberRemoved

from .mixins import TableQueryMixin

from .common import add_application_type_

from . import orm_dataframe

class QueryContactsAdded(TableQueryMixin):

	table = ContactsAdded

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		ca = self.table
		query = self.session.query(ca.timestamp,
								   ca.session_id,
								   ca.user_id,
								   ca.target_id).filter(ca.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df

class QueryContactsRemoved(TableQueryMixin):

	table = ContactsRemoved

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		cr = self.table
		query = self.session.query(cr.timestamp,
								   cr.session_id,
								   cr.user_id,
								   cr.target_id).filter(cr.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df

class QueryDynamicFriendsListsCreated(TableQueryMixin):

	table = DynamicFriendsListsCreated

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		dflc = self.table
		query = self.session.query(dflc.timestamp,
								   dflc.deleted,
								   dflc.dfl_ds_id,
								   dflc.dfl_id,
								   dflc.session_id,
								   dflc.user_id).filter(dflc.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df

class QueryDynamicFriendsListsMemberAdded(TableQueryMixin):

	table = DynamicFriendsListsMemberAdded

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		dflma = self.table
		query = self.session.query(dflma.timestamp,
								   dflma.session_id,
								   dflma.user_id,
								   dflma.dfl_id,
								   dflma.target_id).filter(dflma.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df

class QueryDynamicFriendsListsMemberRemoved(TableQueryMixin):

	table = DynamicFriendsListsMemberRemoved

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		dflmr = self.table
		query = self.session.query(dflmr.timestamp,
								   dflmr.session_id,
								   dflmr.user_id,
								   dflmr.dfl_id,
								   dflmr.target_id
								   ).filter(dflmr.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df

class QueryFriendsListsCreated(TableQueryMixin):

	table = FriendsListsCreated

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		flc = self.table
		query = self.session.query(flc.timestamp,
								   flc.deleted,
								   flc.friends_list_ds_id,
								   flc.friends_list_id,
								   flc.session_id,
								   flc.user_id).filter(flc.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df

class QueryFriendsListsMemberAdded(TableQueryMixin):

	table = FriendsListsMemberAdded

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		flma = self.table
		query = self.session.query(flma.timestamp,
								   flma.session_id,
								   flma.user_id,
								   flma.friends_list_id,
								   flma.target_id).filter(flma.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df

class QueryFriendsListsMemberRemoved(TableQueryMixin):

	table = FriendsListsMemberRemoved

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		flmr = self.table
		query = self.session.query(flmr.timestamp,
								   flmr.session_id,
								   flmr.user_id,
								   flmr.friends_list_id,
								   flmr.target_id).filter(flmr.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df
