#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from nti.analytics_pandas.queries.users import QueryUsers

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestCourses(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestCourses, self).setUp()

	def test_filter_by_user_id(self):
		qu = QueryUsers(self.session)
		users_id = [1, 2, 3, 4, 5]
		qu.filter_by_user_id(users_id)
