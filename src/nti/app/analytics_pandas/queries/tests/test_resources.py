#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

import numpy as np

from nti.analytics_pandas.queries.resources import QueryResources

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestResources(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestResources, self).setUp()

	def test_get_all_resources(self):
		qr = QueryResources(self.session)
		dataframe = qr.get_all_resources()
		assert_that(dataframe['resource_display_name'].iloc[4], equal_to('A Pipe for February (Selections)'))

	def test_get_resources_ds_id_given_id(self):
		qr = QueryResources(self.session)
		resources_id = (3,5,7,9)
		dataframe = qr.get_resources_ds_id_given_id(resources_id)
		assert_that(len(dataframe.index), equal_to(4))
		assert_that(dataframe.resource_id.iloc[3], equal_to(9))

	def test_get_resources_given_id(self):
		qr = QueryResources(self.session)
		resources_id = (10,11,12,13)
		dataframe = qr.get_resources_given_id(resources_id)
		assert_that(len(dataframe.index), equal_to(4))
		assert_that(dataframe.resource_id.iloc[3], equal_to(13))
		assert_that(dataframe['max_time_length'].iloc[0], equal_to(None))

	def test_add_resource_type(self):
		qr = QueryResources(self.session)
		dataframe = qr.get_all_resources()
		dataframe = qr.add_resource_type(dataframe)
		assert_that(dataframe['resource_type'].iloc[3], equal_to(u'self assessment'))

		index = dataframe[dataframe['resource_id'] == np.int(13590)].index.tolist()
		idx = index[0]
		assert_that(dataframe['resource_type'].iloc[idx], equal_to(u'in class discussion'))
