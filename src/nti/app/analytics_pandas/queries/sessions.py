#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .. import MessageFactory as _

from user_agents import parse

from nti.analytics_database.sessions import Sessions
from nti.analytics_database.sessions import UserAgents

from .mixins import TableQueryMixin

from . import orm_dataframe

class QuerySessions(TableQueryMixin):

	table = Sessions

	def get_sessions_by_id(self, sessions_id):
		s = self.table
		query = self.session.query(s.session_id,
								   s.user_id,
								   s.ip_addr,
								   s.user_agent_id,
								   s.start_time,
								   s.end_time).filter(s.session_id.in_(sessions_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def get_sessions_user_agent_id(self, sessions_id):
		s = self.table
		query = self.session.query(s.session_id,
									s.user_agent_id).filter(s.session_id.in_(sessions_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

class QueryUserAgents(TableQueryMixin):

	table = UserAgents

	def get_user_agents_by_id(self, user_agents_id):
		ua = self.table
		query = self.session.query(ua.user_agent_id,
									ua.user_agent).filter(ua.user_agent_id.in_(user_agents_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	@classmethod
	def _label_user_agents(cls, ua_string):
		if 'iPad' in ua_string:
			return _('iPad App')
		else:
			user_agent = parse(ua_string)
			if user_agent.is_mobile :
				return _('Mobile App')
			elif user_agent.is_tablet :
				if 'mobile' in user_agent.browser.family.lower():
					return _('Mobile App')
				else:
					return _('Web App')
			elif user_agent.is_pc :
				return _('Web App')
			else :
				if 'mobile' in user_agent.browser.family.lower():
					return _('Mobile App')
				else:
					return _('Web App')

	def add_device_type(self, ua_dataframe):
		index = ua_dataframe['user_agent']
		ua_dataframe['device_type'] = index.apply(lambda x : self._label_user_agents(x))
		return ua_dataframe

	def add_application_type(self, ua_dataframe):
		index = ua_dataframe['user_agent']
		ua_dataframe['application_type'] = index.apply(lambda x : self._label_user_agents(x))
		return ua_dataframe
