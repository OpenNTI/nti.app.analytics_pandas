#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.analytics_database.social import ChatsJoined
from nti.analytics_database.social import ChatsInitiated

from .mixins import TableQueryMixin

from .common import add_application_type_

from . import orm_dataframe

class QueryChatsInitiated(TableQueryMixin):

	table = ChatsInitiated

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		ci = self.table
		query = self.session.query(ci.timestamp,
								   ci.chat_ds_id,
								   ci.chat_id,
								   ci.session_id,
								   ci.user_id).filter(ci.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df

class QueryChatsJoined(TableQueryMixin):

	table = ChatsJoined

	def filter_by_period_of_time(self, start_date=None, end_date=None):
		cj = self.table
		query = self.session.query(cj.timestamp,
								   cj.chat_id,
								   cj.session_id,
								   cj.user_id).filter(cj.timestamp.between(start_date, end_date))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def add_application_type(self, dataframe):
		new_df = add_application_type_(self.session, dataframe)
		return new_df
