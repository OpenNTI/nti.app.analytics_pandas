#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import assert_that
from hamcrest import greater_than

from nti.analytics_pandas.queries.chats import QueryChatsInitiated
from nti.analytics_pandas.queries.chats import QueryChatsJoined

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestChats(AnalyticsPandasTestBase):

	def test_query_chats_initiated_period_of_time(self):
		start_date = u'2015-10-05'
		end_date = u'2015-10-19'
		qci = QueryChatsInitiated(self.session)
		dataframe = qci.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), greater_than(0))

	def test_query_chats_joined_period_of_time(self):
		start_date = u'2015-10-05'
		end_date = u'2015-10-19'
		qcj = QueryChatsJoined(self.session)
		dataframe = qcj.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), greater_than(0))
