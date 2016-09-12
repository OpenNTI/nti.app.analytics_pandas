#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.queries.notes import QueryNoteLikes
from nti.analytics_pandas.queries.notes import QueryNotesViewed
from nti.analytics_pandas.queries.notes import QueryNotesCreated
from nti.analytics_pandas.queries.notes import QueryNoteFavorites

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestNotes(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestNotes, self).setUp()

	def test_query_notes_created_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qnc = QueryNotesCreated(self.session)
		dataframe = qnc.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(688))

	def test_query_notes_created_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qnc = QueryNotesCreated(self.session)
		dataframe = qnc.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(34))

	def test_query_notes_created_add_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qnc = QueryNotesCreated(self.session)
		dataframe = qnc.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(34))
		new_df = qnc.add_device_type(dataframe)
		assert_that(len(dataframe.index), equal_to(len(new_df.index)))
		assert_that(new_df.columns, has_item('device_type'))

	def test_query_notes_created_add_resource_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qnc = QueryNotesCreated(self.session)
		dataframe = qnc.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(34))
		new_df = qnc.add_resource_type(dataframe)
		assert_that(len(dataframe.index), equal_to(len(new_df.index)))
		assert_that(new_df.columns, has_item('resource_type'))

	def test_query_notes_viewed_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qnv = QueryNotesViewed(self.session)
		dataframe = qnv.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(7471))

	def test_query_notes_viewed_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qnv = QueryNotesViewed(self.session)
		dataframe = qnv.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(157))

	def test_query_notes_viewed_add_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qnv = QueryNotesViewed(self.session)
		dataframe = qnv.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(157))
		new_df = qnv.add_device_type(dataframe)
		assert_that(len(dataframe.index), equal_to(len(new_df.index)))
		assert_that(new_df.columns, has_item('device_type'))

	def test_query_notes_viewed_add_resource_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qnv = QueryNotesViewed(self.session)
		dataframe = qnv.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(157))
		new_df = qnv.add_resource_type(dataframe)
		assert_that(len(dataframe.index), equal_to(len(new_df.index)))
		assert_that(new_df.columns, has_item('resource_type'))

	def test_query_notes_viewed_add_sharing_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qnv = QueryNotesViewed(self.session)
		dataframe = qnv.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(157))
		new_df = qnv.add_sharing_type(dataframe)
		assert_that(len(dataframe.index), equal_to(len(new_df.index)))
		assert_that(new_df.columns, has_item('sharing'))

	def test_query_note_favorites_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qnf = QueryNoteFavorites(self.session)
		dataframe = qnf.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(5))

	def test_query_note_favorites_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qnf = QueryNoteFavorites(self.session)
		dataframe = qnf.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(0))

	def test_query_note_favorites_add_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qnf = QueryNoteFavorites(self.session)
		dataframe = qnf.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(0))
		new_df = qnf.add_device_type(dataframe)
		assert_that(new_df, equal_to(None))

	def test_query_note_favorites_add_resource_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qnf = QueryNoteFavorites(self.session)
		dataframe = qnf.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(0))
		new_df = qnf.add_resource_type(dataframe)
		assert_that(new_df, equal_to(None))

	def test_query_note_likes_by_period_of_time(self):
		start_date = u'2015-03-01'
		end_date = u'2015-05-31'
		qnl = QueryNoteLikes(self.session)
		dataframe = qnl.filter_by_period_of_time(start_date, end_date)
		assert_that(len(dataframe.index), equal_to(18))

	def test_query_note_likes_by_period_of_time_and_course_id(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qnl = QueryNoteLikes(self.session)
		dataframe = qnl.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(0))

	def test_query_note_likes_add_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qnl = QueryNoteLikes(self.session)
		dataframe = qnl.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(0))
		new_df = qnl.add_device_type(dataframe)
		assert_that(new_df, equal_to(None))

	def test_query_note_likes_add_resource_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		course_id = ['388']
		qnl = QueryNoteLikes(self.session)
		dataframe = qnl.filter_by_period_of_time_and_course_id(start_date, end_date, course_id)
		assert_that(len(dataframe.index), equal_to(0))
		new_df = qnl.add_resource_type(dataframe)
		assert_that(new_df, equal_to(None))
