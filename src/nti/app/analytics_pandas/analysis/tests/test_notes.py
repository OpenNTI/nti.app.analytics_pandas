#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

import numpy as np

from nti.analytics_pandas.analysis.notes import NoteLikesTimeseries
from nti.analytics_pandas.analysis.notes import NotesViewTimeseries
from nti.analytics_pandas.analysis.notes import NotesEventsTimeseries
from nti.analytics_pandas.analysis.notes import NotesCreationTimeseries
from nti.analytics_pandas.analysis.notes import NoteFavoritesTimeseries

from nti.analytics_pandas.utils import get_values_of_series_categorical_index_

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestNotesEDA(AnalyticsPandasTestBase):

	def test_notes_creation_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(nct.dataframe.index), equal_to(34))
		assert_that(nct.dataframe.columns, has_item('device_type'))
		assert_that(nct.dataframe.columns, has_item('resource_type'))

		dataframe = nct.dataframe
		assert_that(dataframe.columns, has_item('context_name'))
		assert_that(dataframe.columns, has_item('enrollment_type'))

		df = nct.analyze_device_types(dataframe)
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_notes_created'))
		assert_that(df.columns, has_item('ratio'))

		df = nct.analyze_resource_types()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_notes_created'))
		assert_that(df.columns, has_item('ratio'))

		df = nct.analyze_resource_device_types()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_notes_created'))
		assert_that(df.columns, has_item('ratio'))

		df = nct.get_the_most_active_users()
		assert_that(len(df.index), equal_to(10))

		df = nct.analyze_sharing_types(dataframe)
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_notes_created'))
		assert_that(df.columns, has_item('ratio'))

		sharing_df, device_df = nct.analyze_notes_created_on_videos()
		assert_that(sharing_df.columns, has_item('number_of_unique_users'))
		assert_that(sharing_df.columns, has_item('number_of_notes_created'))
		assert_that(sharing_df.columns, has_item('ratio'))

		assert_that(device_df.columns, has_item('number_of_unique_users'))
		assert_that(device_df.columns, has_item('number_of_notes_created'))
		assert_that(device_df.columns, has_item('ratio'))

		df = nct.analyze_events_per_course_sections()
		assert_that(sharing_df.columns, has_item('number_of_unique_users'))
		assert_that(sharing_df.columns, has_item('number_of_notes_created'))
		assert_that(sharing_df.columns, has_item('ratio'))

	def test_notes_view_based_on_timestamp_date(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(nvt.dataframe.index), equal_to(157))
		assert_that(nvt.dataframe.columns, has_item('device_type'))
		assert_that(nvt.dataframe.columns, has_item('resource_type'))
		assert_that(nvt.dataframe.columns, has_item('context_name'))
		assert_that(nvt.dataframe.columns, has_item('enrollment_type'))

		events_df = nvt.analyze_total_events()

		df = nvt.analyze_unique_events_based_on_device_type()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_unique_notes_viewed'))

		df = nvt.analyze_total_events_based_on_device_type()
		assert_that(df.columns, has_item('number_of_note_views'))
		assert_that(len(events_df.index), equal_to(len(df.sum(level='timestamp_period'))))

		most_viewed_notes = nvt.get_the_most_viewed_notes()
		assert_that(len(most_viewed_notes), equal_to(10))
		index_values = get_values_of_series_categorical_index_(most_viewed_notes)
		assert_that(type(index_values), equal_to(np.ndarray))

		most_viewed_notes_author_df = nvt.get_the_most_viewed_notes_and_its_author()
		assert_that(len(most_viewed_notes), equal_to(len(most_viewed_notes_author_df.index)))

		most_active_users_df = nvt.get_the_most_active_users()
		assert_that(len(most_active_users_df.index), equal_to(10))

		df = nvt.analyze_unique_events_based_on_resource_type()
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('number_of_unique_notes_viewed'))

		df = nvt.analyze_total_events_based_on_resource_type()
		assert_that(df.columns, has_item('number_of_note_views'))
		assert_that(len(events_df.index), equal_to(len(df.sum(level='timestamp_period'))))

		df = nvt.analyze_total_events_based_on_sharing_type()
		assert_that(df.columns, has_item('number_of_note_views'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))
		assert_that(len(events_df.index), equal_to(len(df.sum(level='timestamp_period'))))

		df = nvt.analyze_total_events_per_course_sections()
		assert_that(df.columns, has_item('number_of_note_views'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))
		assert_that(len(events_df.index), equal_to(len(df.sum(level='timestamp_period'))))

	def test_note_likes_based_on_timestamp_date(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(nlt.dataframe.index), equal_to(41))

		dataframe = nlt.dataframe
		assert_that(dataframe.columns, has_item('context_name'))
		assert_that(dataframe.columns, has_item('enrollment_type'))

		events_df = nlt.analyze_events()
		assert_that(len(events_df.index), equal_to(13))
		assert_that(events_df.columns, has_item('number_of_note_likes'))
		assert_that(events_df.columns, has_item('number_of_unique_users'))
		assert_that(events_df.columns, has_item('ratio'))

	def test_note_favorites_based_on_timestamp_date(self):
		start_date = '2015-10-05'
		end_date = '2015-10-20'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)
		assert_that(len(nft.dataframe.index), equal_to(2))

		dataframe = nft.dataframe
		assert_that(dataframe.columns, has_item('context_name'))
		assert_that(dataframe.columns, has_item('enrollment_type'))

		events_df = nft.analyze_events()
		assert_that(len(events_df.index), equal_to(1))
		assert_that(events_df.columns, has_item('number_of_note_favorites'))
		assert_that(events_df.columns, has_item('number_of_unique_users'))
		assert_that(events_df.columns, has_item('ratio'))

	def test_notes_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)

		net = NotesEventsTimeseries(nct, nvt, nlt, nft)
		df = net.combine_all_events()
		assert_that(len(df.columns), equal_to(5))
		assert_that(len(df.index), equal_to(62))
