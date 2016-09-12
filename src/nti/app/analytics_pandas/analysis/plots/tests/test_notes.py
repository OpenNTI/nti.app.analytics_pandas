#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.notes import NoteLikesTimeseries
from nti.analytics_pandas.analysis.notes import NotesViewTimeseries
from nti.analytics_pandas.analysis.notes import NotesEventsTimeseries
from nti.analytics_pandas.analysis.notes import NotesCreationTimeseries
from nti.analytics_pandas.analysis.notes import NoteFavoritesTimeseries

from nti.analytics_pandas.analysis.plots.notes import NoteLikesTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NotesViewTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NotesEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NotesCreationTimeseriesPlot
from nti.analytics_pandas.analysis.plots.notes import NoteFavoritesTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestNotesCreationPlot(AnalyticsPandasTestBase):

	def test_explore_events_notes_creation(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		nctp.explore_events()

	def test_explore_events_notes_creation_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		nctp = NotesCreationTimeseriesPlot(nct)
		nctp.explore_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_device_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		nctp.analyze_device_types()

	def test_analyze_enrollment_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		nctp.analyze_enrollment_types()

	def test_analyze_resource_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		nctp.analyze_resource_types()

	def test_plot_most_active_users(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		nctp.plot_the_most_active_users()

	def test_analyze_sharing_types(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		nctp.analyze_sharing_types()

	def test_analyze_notes_created_on_videos(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		nctp.analyze_notes_created_on_videos(period_breaks='1 day', minor_period_breaks='None')

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		nctp.analyze_events_per_course_sections()

	def test_empty_result(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['123']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nctp = NotesCreationTimeseriesPlot(nct)
		nctp.analyze_events_per_course_sections()
		assert_that(len(_), equal_to(0))
		nctp.analyze_notes_created_on_videos(period_breaks='1 day', minor_period_breaks='None')
		assert_that(len(_), equal_to(0))
		nctp.analyze_sharing_types()
		assert_that(len(_), equal_to(0))
		nctp.plot_the_most_active_users()
		assert_that(len(_), equal_to(0))
		nctp.analyze_resource_types()
		assert_that(len(_), equal_to(0))
		nctp.analyze_device_types()
		assert_that(len(_), equal_to(0))
		nctp.explore_events()
		assert_that(len(_), equal_to(0))
		nctp.analyze_enrollment_types()
		assert_that(len(_), equal_to(0))

class TestNoteViewsPlot(AnalyticsPandasTestBase):

	def test_analyze_total_events_based_on_sharing_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		nvtp.analyze_total_events_based_on_sharing_type(period_breaks='1 week')

	def test_analyze_total_events_based_on_sharing_type_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		nvtp = NotesViewTimeseriesPlot(nvt)
		nvtp.analyze_total_events_based_on_sharing_type(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_total_events_based_on_device_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		nvtp.analyze_total_events_based_on_device_type(period_breaks='1 week')

	def test_analyze_total_events_based_on_enrollment_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		nvtp.analyze_total_events_based_on_enrollment_type(period_breaks='1 week')

	def test_analyze_total_events_based_on_resource_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		nvtp.analyze_total_events_based_on_resource_type(period_breaks='1 week')

	def test_plot_most_active_users(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		nvtp.plot_the_most_active_users()

	def test_explore_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		nvtp.explore_events(period_breaks='1 week')

	def test_analyze_unique_events_based_on_sharing_type(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		nvtp.analyze_unique_events_based_on_sharing_type(period_breaks='1 week')

	def test_analyze_total_events_per_course_sections(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		nvtp.analyze_total_events_per_course_sections()

	def test_plot_the_most_viewed_notes_and_its_author(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		nvtp.plot_the_most_viewed_notes_and_its_author()

	def test_empty_result(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['123']
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nvtp = NotesViewTimeseriesPlot(nvt)
		nvtp.plot_the_most_viewed_notes_and_its_author()
		assert_that(len(_), equal_to(0))
		nvtp.analyze_total_events_per_course_sections()
		assert_that(len(_), equal_to(0))
		nvtp.analyze_unique_events_based_on_sharing_type(period_breaks='1 week')
		assert_that(len(_), equal_to(0))
		nvtp.explore_events(period_breaks='1 week')
		assert_that(len(_), equal_to(0))
		nvtp.plot_the_most_active_users()
		assert_that(len(_), equal_to(0))
		nvtp.analyze_total_events_based_on_resource_type(period_breaks='1 week')
		assert_that(len(_), equal_to(0))
		nvtp.analyze_total_events_based_on_enrollment_type(period_breaks='1 week')
		assert_that(len(_), equal_to(0))
		nvtp.analyze_total_events_based_on_device_type(period_breaks='1 week')
		assert_that(len(_), equal_to(0))
		nvtp.analyze_total_events_based_on_sharing_type(period_breaks='1 week')
		assert_that(len(_), equal_to(0))


class TestNoteLikesPlot(AnalyticsPandasTestBase):

	def test_explore_events(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nltp = NoteLikesTimeseriesPlot(nlt)
		nltp.explore_events(period_breaks='1 day', minor_period_breaks=None)

	def test_explore_events_weekly(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		nltp = NoteLikesTimeseriesPlot(nlt)
		nltp.explore_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_events_per_device_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nltp = NoteLikesTimeseriesPlot(nlt)
		nltp.analyze_events_per_device_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_enrollment_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nltp = NoteLikesTimeseriesPlot(nlt)
		nltp.analyze_events_per_enrollment_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_resource_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nltp = NoteLikesTimeseriesPlot(nlt)
		nltp.analyze_events_per_resource_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nltp = NoteLikesTimeseriesPlot(nlt)
		nltp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks=None)

	def test_empty_result(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['123']
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nltp = NoteLikesTimeseriesPlot(nlt)
		nltp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))
		nltp.analyze_events_per_resource_types(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))
		nltp.analyze_events_per_enrollment_types(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))
		nltp.analyze_events_per_device_types(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))
		nltp.explore_events(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))

class TestNoteFavoritesPlot(AnalyticsPandasTestBase):

	def test_explore_events(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)
		nftp = NoteFavoritesTimeseriesPlot(nft)
		nftp.explore_events(period_breaks='1 day', minor_period_breaks=None)

	def test_explore_events_weekly(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		nftp = NoteFavoritesTimeseriesPlot(nft)
		nftp.explore_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_events_per_device_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)
		nftp = NoteFavoritesTimeseriesPlot(nft)
		nftp.analyze_events_per_device_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_enrollment_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)
		nftp = NoteFavoritesTimeseriesPlot(nft)
		nftp.analyze_events_per_enrollment_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_resource_types(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)
		nftp = NoteFavoritesTimeseriesPlot(nft)
		nftp.analyze_events_per_resource_types(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_course_sections(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['1068', '1096', '1097', '1098', '1099']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)
		nftp = NoteFavoritesTimeseriesPlot(nft)
		nftp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks=None)

	def test_empty_result(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['123']
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)
		nftp = NoteFavoritesTimeseriesPlot(nft)
		nftp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))
		nftp.analyze_events_per_resource_types(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))
		nftp.analyze_events_per_enrollment_types(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))
		nftp.analyze_events_per_device_types(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))
		nftp.explore_events(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))

class TestNotesEventsPlot(AnalyticsPandasTestBase):

	def test_notes_events(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)

		net = NotesEventsTimeseries(nct, nvt, nlt, nft)
		netp = NotesEventsTimeseriesPlot(net)
		netp.explore_all_events()

	def test_notes_events_weekly(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id, period='weekly')
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id, period='weekly')

		net = NotesEventsTimeseries(nct, nvt, nlt, nft)
		netp = NotesEventsTimeseriesPlot(net)
		netp.explore_all_events(period_breaks='1 week', minor_period_breaks=None)

	def test_empty_result(self):
		start_date = '2015-10-05'
		end_date = '2015-12-04'
		course_id = ['123']
		nct = NotesCreationTimeseries(self.session, start_date, end_date, course_id)
		nvt = NotesViewTimeseries(self.session, start_date, end_date, course_id)
		nlt = NoteLikesTimeseries(self.session, start_date, end_date, course_id)
		nft = NoteFavoritesTimeseries(self.session, start_date, end_date, course_id)

		net = NotesEventsTimeseries(nct, nvt, nlt, nft)
		netp = NotesEventsTimeseriesPlot(net)
		netp.explore_all_events()
		assert_that(len(_), equal_to(0))
