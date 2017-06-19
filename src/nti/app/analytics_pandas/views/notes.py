#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from zope import interface

from nti.analytics_pandas.analysis import NoteLikesTimeseries
from nti.analytics_pandas.analysis import NotesViewTimeseries
from nti.analytics_pandas.analysis import NotesEventsTimeseries
from nti.analytics_pandas.analysis import NoteLikesTimeseriesPlot
from nti.analytics_pandas.analysis import NotesViewTimeseriesPlot
from nti.analytics_pandas.analysis import NotesCreationTimeseries
from nti.analytics_pandas.analysis import NoteFavoritesTimeseries
from nti.analytics_pandas.analysis import NotesEventsTimeseriesPlot
from nti.analytics_pandas.analysis import NotesCreationTimeseriesPlot
from nti.analytics_pandas.analysis import NoteFavoritesTimeseriesPlot

from .commons import get_course_names
from .commons import build_plot_images_dictionary
from .commons import build_images_dict_from_plot_dict

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class NoteEventsTimeseriesContext(object):

	def __init__(self, session=None, start_date=None, end_date=None, courses=None,
				 period_breaks='1 week', minor_period_breaks='1 day',
				 theme_bw_=True, number_of_most_active_user=10, period='daily'):
		self.session = session
		self.courses = courses
		self.end_date = end_date
		self.start_date = start_date
		self.period_breaks = period_breaks
		self.theme_bw_ = theme_bw_
		self.minor_period_breaks = minor_period_breaks
		self.number_of_most_active_user = number_of_most_active_user
		self.period = period

Context = NoteEventsTimeseriesContext

class NoteEventsTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Notes Related Events')

	def _build_data(self, data=_('sample notes related events report')):
		keys = self.options.keys()

		if 'has_notes_created_data' not in keys:
			self.options['has_notes_created_data'] = False

		if 'has_note_events_data' not in keys:
			self.options['has_note_events_data'] = False

		if 'has_note_views_data' not in keys:
			self.options['has_note_views_data'] = False

		if 'has_note_likes_data' not in keys:
			self.options['has_note_likes_data'] = False

		if 'has_note_favorites_data' not in keys:
			self.options['has_note_favorites_data'] = False

		self.options['data'] = data
		return self.options

	def __call__(self):
		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ", ".join(map(str, course_names))
		data = {}

		self.nct = NotesCreationTimeseries(self.context.session,
										   self.context.start_date,
										   self.context.end_date,
										   self.context.courses,
										   period=self.context.period)
		if self.nct.dataframe.empty:
			self.options['has_notes_created_data'] = False
		else:
			self.options['has_notes_created_data'] = True
			data = self.generate_notes_created_plots(data)

		self.nvt = NotesViewTimeseries(self.context.session,
									   self.context.start_date,
									   self.context.end_date,
									   self.context.courses,
									   period=self.context.period)
		if self.nvt.dataframe.empty:
			self.options['has_note_views_data'] = False
		else:
			self.options['has_note_views_data'] = True
			data = self.generate_note_views_plots(data)

		self.nlt = NoteLikesTimeseries(self.context.session,
									   self.context.start_date,
									   self.context.end_date,
									   self.context.courses,
									   period=self.context.period)
		if self.nlt.dataframe.empty:
			self.options['has_note_likes_data'] = False
		else:
			self.options['has_note_likes_data'] = True
			data = self.generate_note_likes_plots(data)

		self.nft = NoteFavoritesTimeseries(self.context.session,
									   	   self.context.start_date,
									   	   self.context.end_date,
									   	   self.context.courses,
									   	   period=self.context.period)
		if self.nlt.dataframe.empty:
			self.options['has_note_favorites_data'] = False
		else:
			self.options['has_note_favorites_data'] = True
			data = self.generate_note_favorites_plots(data)

		self.net = NotesEventsTimeseries(self.nct, self.nvt, self.nlt, self.nft)
		data = self.generate_combined_note_events(data)

		self._build_data(data)
		return self.options

	def generate_notes_created_plots(self, data):
		self.nctp = NotesCreationTimeseriesPlot(self.nct)
		data = self.get_notes_created_plots(data)
		data = self.get_notes_created_per_device_types_plots(data)
		data = self.get_notes_created_per_resource_types_plots(data)
		data = self.get_notes_created_per_sharing_types_plots(data)
		data = self.get_notes_created_the_most_active_users(data)
		data = self.get_notes_created_per_enrollment_types_plots(data)
		data = self.get_notes_created_on_videos(data)
		if len(self.context.courses) > 1:
			data = self.get_notes_created_per_course_sections_plots(data)
		else:
			self.options['has_notes_created_data_per_course_sections'] = False
		return data

	def get_notes_created_plots(self, data):
		plots = self.nctp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['notes_created'] = build_plot_images_dictionary(plots)
		return data

	def get_notes_created_per_device_types_plots(self, data):
		plots = self.nctp.analyze_device_types(self.context.period_breaks,
										 	   self.context.minor_period_breaks,
										 	   self.context.theme_bw_)
		self.options['has_notes_created_data_per_device_types'] = False
		if plots:
			data['notes_created_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_notes_created_data_per_device_types'] = True
		return data

	def get_notes_created_per_enrollment_types_plots(self, data):
		plots = self.nctp.analyze_enrollment_types(self.context.period_breaks,
										 		   self.context.minor_period_breaks,
										 		   self.context.theme_bw_)
		self.options['has_notes_created_data_per_enrollment_types'] = False
		if plots:
			data['notes_created_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_notes_created_data_per_enrollment_types'] = True
		return data

	def get_notes_created_per_resource_types_plots(self, data):
		plots = self.nctp.analyze_resource_types(self.context.period_breaks,
										 		 self.context.minor_period_breaks,
										 		 self.context.theme_bw_)
		self.options['has_notes_created_data_per_resource_types'] = False
		if plots:
			data['notes_created_per_resource_types'] = build_plot_images_dictionary(plots)
			self.options['has_notes_created_data_per_resource_types'] = True
		return data

	def get_notes_created_per_sharing_types_plots(self, data):
		plots = self.nctp.analyze_sharing_types(self.context.period_breaks,
										 		self.context.minor_period_breaks,
										 		self.context.theme_bw_)
		self.options['has_notes_created_data_per_sharing_types'] = False
		if plots:
			data['notes_created_per_sharing_types'] = build_plot_images_dictionary(plots)
			self.options['has_notes_created_data_per_sharing_types'] = True
		return data

	def get_notes_created_on_videos(self, data):
		plots = self.nctp.analyze_notes_created_on_videos(self.context.period_breaks,
												 		  self.context.minor_period_breaks,
												 		  self.context.theme_bw_)
		self.options['has_notes_created_on_videos'] = False
		if plots:
			data['notes_created_on_videos'] = build_images_dict_from_plot_dict(plots)
			self.options['has_notes_created_on_videos'] = True
			if 'sharing' in data['notes_created_on_videos'].keys() :
				self.options['has_notes_created_on_videos_per_sharing_types'] = True
			else:
				self.options['has_notes_created_on_videos_per_sharing_types'] = False

			if 'user_agent' in data['notes_created_on_videos'].keys() :
				self.options['has_notes_created_on_videos_per_device_types'] = True
			else:
				self.options['has_notes_created_on_videos_per_device_types'] = False

		return data

	def get_notes_created_per_course_sections_plots(self, data):
		plots = self.nctp.analyze_events_per_course_sections(self.context.period_breaks,
										 					 self.context.minor_period_breaks,
										 					 self.context.theme_bw_)
		self.options['has_notes_created_data_per_course_sections'] = False
		if plots:
			data['notes_created_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_notes_created_data_per_course_sections'] = True
		return data

	def get_notes_created_the_most_active_users(self, data):
		plots = self.nctp.plot_the_most_active_users(self.context.number_of_most_active_user)
		self.options['has_notes_created_user'] = False
		if plots:
			data['notes_created_users'] = build_plot_images_dictionary(plots)
			self.options['has_notes_created_user'] = True
		return data

	def generate_note_views_plots(self, data):
		self.nvtp = NotesViewTimeseriesPlot(self.nvt)
		data = self.get_note_views_plots(data)
		data = self.get_note_views_plots_per_device_types(data)
		data = self.get_note_views_plots_per_resource_types(data)
		data = self.get_note_views_plots_per_sharing_types(data)
		if len(self.context.courses) > 1:
			data = self.get_note_views_per_course_sections_plots(data)
		else:
			self.options['has_note_views_data_per_course_sections'] = False
		data = self.get_the_most_active_users_viewing_notes(data)
		data = self.get_the_most_viewed_notes_and_its_author(data)
		data = self.get_note_views_plots_per_enrollment_types(data)
		return data

	def get_note_views_plots(self, data):
		plots = self.nvtp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['note_views'] = build_plot_images_dictionary(plots)
		return data

	def get_note_views_plots_per_device_types(self, data):
		plots = self.nvtp.analyze_total_events_based_on_device_type(self.context.period_breaks,
										 				  			self.context.minor_period_breaks,
										 				  			self.context.theme_bw_)
		self.options['has_note_views_data_per_device_types'] = False
		if plots:
			data['note_views_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_note_views_data_per_device_types'] = True
		return data

	def get_note_views_plots_per_enrollment_types(self, data):
		plots = self.nvtp.analyze_total_events_based_on_enrollment_type(self.context.period_breaks,
										 				  			self.context.minor_period_breaks,
										 				  			self.context.theme_bw_)
		self.options['has_note_views_data_per_enrollment_types'] = False
		if plots:
			data['note_views_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_note_views_data_per_enrollment_types'] = True
		return data

	def get_note_views_plots_per_resource_types(self, data):
		plots = self.nvtp.analyze_total_events_based_on_resource_type(self.context.period_breaks,
										 				  			self.context.minor_period_breaks,
										 				  			self.context.theme_bw_)
		self.options['has_note_views_data_per_resource_types'] = False
		if plots:
			data['note_views_per_resource_types'] = build_plot_images_dictionary(plots)
			self.options['has_note_views_data_per_resource_types'] = True
		return data

	def get_note_views_plots_per_sharing_types(self, data):
		plots = self.nvtp.analyze_total_events_based_on_sharing_type(self.context.period_breaks,
										 				  			self.context.minor_period_breaks,
										 				  			self.context.theme_bw_)
		self.options['has_note_views_data_per_sharing_types'] = False
		if plots:
			data['note_views_per_sharing_types'] = build_plot_images_dictionary(plots)
			self.options['has_note_views_data_per_sharing_types'] = True
		return data

	def get_note_views_per_course_sections_plots(self, data):
		plots = self.nvtp.analyze_total_events_per_course_sections(self.context.period_breaks,
										 					 	   self.context.minor_period_breaks,
										 						   self.context.theme_bw_)
		self.options['has_note_views_data_per_course_sections'] = False
		if plots:
			data['note_views_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_note_views_data_per_course_sections'] = True
		return data

	def get_the_most_active_users_viewing_notes(self, data):
		plots = self.nvtp.plot_the_most_active_users(self.context.number_of_most_active_user)
		self.options['has_note_views_users'] = False
		if plots :
			data['note_views_users'] = build_plot_images_dictionary(plots)
			self.options['has_note_views_users'] = True
		return data

	def get_the_most_viewed_notes_and_its_author(self, data):
		plots = self.nvtp.plot_the_most_viewed_notes_and_its_author()
		self.options['has_note_views_author'] = False
		if plots :
			data['note_views_authors'] = build_plot_images_dictionary(plots)
			self.options['has_note_views_author'] = True
		return data

	def generate_note_likes_plots(self, data):
		self.nltp = NoteLikesTimeseriesPlot(self.nlt)
		data = self.get_note_likes_plots(data)
		return data

	def get_note_likes_plots(self, data):
		plots = self.nltp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['note_likes'] = build_plot_images_dictionary(plots)
		return data

	def generate_note_favorites_plots(self, data):
		self.nftp = NoteFavoritesTimeseriesPlot(self.nft)
		data = self.get_note_favorites_plots(data)
		return data

	def get_note_favorites_plots(self, data):
		plots = self.nftp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['note_favorites'] = build_plot_images_dictionary(plots)
		return data

	def generate_combined_note_events(self, data):
		self.netp = NotesEventsTimeseriesPlot(self.net)
		plots = self.netp.explore_all_events(self.context.period_breaks,
										 	 self.context.minor_period_breaks,
										 	 self.context.theme_bw_)
		self.options['has_note_events_data'] = False
		if plots:
			data['note_events'] = build_plot_images_dictionary(plots)
			self.options['has_note_events_data'] = True
		return data

View = NoteEventsTimeseriesReport = NoteEventsTimeseriesReportView
