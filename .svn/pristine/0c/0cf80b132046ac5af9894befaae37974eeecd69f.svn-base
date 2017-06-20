#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.analytics_pandas.analysis import VideoEventsTimeseries
from nti.analytics_pandas.analysis import VideoEventsTimeseriesPlot

from nti.app.analytics_pandas import MessageFactory as _

from nti.app.analytics_pandas.views.commons import get_course_names
from nti.app.analytics_pandas.views.commons import build_plot_images_dictionary
from nti.app.analytics_pandas.views.commons import build_images_dict_from_plot_dict

from nti.app.analytics_pandas.views.mixins import AbstractReportView

@interface.implementer(interface.Interface)
class VideosTimeseriesContext(object):

	def __init__(self, session=None, start_date=None, end_date=None, courses=None,
				 period_breaks=None, minor_period_breaks=None, theme_bw_=True,
				 number_of_most_active_user=10, period='daily'):
		self.period = period
		self.session = session
		self.courses = courses
		self.end_date = end_date
		self.start_date = start_date
		self.period_breaks = period_breaks
		self.theme_bw_ = theme_bw_
		self.minor_period_breaks = minor_period_breaks
		self.number_of_most_active_user = number_of_most_active_user

Context = VideosTimeseriesContext

class VideosTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Videos Related Events')

	def _build_data(self, data=_('sample Videos related events report')):
		keys = self.options.keys()
		if 'has_video_data' not in keys:
			self.options['has_video_data'] = False

		if 'has_video_watched_data' not in keys:
			self.options['has_video_watched_data'] = False

		if 'has_video_watched_data_per_device_types' not in keys:
			self.options['has_video_watched_data_per_device_types'] = False

		if 'has_video_watched_data_per_enrollment_types' not in keys:
			self.options['has_video_watched_data_per_enrollment_types'] = False

		if 'has_video_skipped_data' not in keys:
			self.options['has_video_skipped_data'] = False

		if 'has_video_skipped_data_per_device_types' not in keys:
			self.options['has_video_skipped_data_per_device_types'] = False

		if 'has_video_skipped_data_per_enrollment_types' not in keys:
			self.options['has_video_skipped_data_per_enrollment_types'] = False

		self.options['data'] = data
		return self.options

	def __call__(self):
		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ", ".join(map(str, course_names))
		data = {}
		self.vet = VideoEventsTimeseries(self.context.session,
										 self.context.start_date,
										 self.context.end_date,
										 self.context.courses,
										 period=self.context.period)
		if self.vet.dataframe.empty:
			self.options['has_video_data'] = False
		else:
			self.options['has_video_data'] = True
			data = self.generate_video_events_plots(data)

		self._build_data(data)
		return self.options

	def generate_video_events_plots(self, data):
		self.vetp = VideoEventsTimeseriesPlot(self.vet)
		data = self.get_video_event_plots(data)
		data = self.get_video_watched_plots(data)
		data = self.get_video_watched_plots_per_device_types(data)
		data = self.get_video_watched_plots_per_enrollment_types(data)
		data = self.get_video_skipped_plots(data)
		data = self.get_video_skipped_plots_per_device_types(data)
		data = self.get_video_skipped_plots_per_enrollment_types(data)
		if len(self.context.courses) > 1 :
			data = self.get_video_watched_plots_per_course_sections(data)
			data = self.get_video_skipped_plots_per_course_sections(data)
		return data

	def get_video_event_plots(self, data):
		plots = self.vetp.analyze_video_events_types(self.context.period_breaks,
													 self.context.minor_period_breaks,
													 self.context.theme_bw_)
		if plots:
			data['video_events'] = build_plot_images_dictionary(plots)
		return data

	def get_video_watched_plots(self, data):
		plots = self.vetp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_,
										 video_event_type='watch')
		if plots:
			data['videos_watched'] = build_plot_images_dictionary(plots)
			self.options['has_video_watched_data'] = True
		return data

	def get_video_watched_plots_per_device_types(self, data):
		plots = self.vetp.analyze_video_events_device_types(self.context.period_breaks,
										 					self.context.minor_period_breaks,
										 					video_event_type='watch',
											 				theme_bw_=self.context.theme_bw_)
		if plots:
			data['videos_watched_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_video_watched_data_per_device_types'] = True
		return data

	def get_video_watched_plots_per_enrollment_types(self, data):
		plots = self.vetp.analyze_video_events_enrollment_types(self.context.period_breaks,
										 					self.context.minor_period_breaks,
										 					video_event_type='watch',
											 				theme_bw_=self.context.theme_bw_)
		if plots:
			data['videos_watched_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_video_watched_data_per_enrollment_types'] = True
		return data

	def get_video_watched_plots_per_course_sections(self, data):
		plots = self.vetp.analyze_video_events_per_course_sections(self.context.period_breaks,
												 				   self.context.minor_period_breaks,
												 				   video_event_type='watch',
													 			   theme_bw_=self.context.theme_bw_)
		self.options['has_video_watched_data_per_course_sections'] = False
		if plots:
			data['videos_watched_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_video_watched_data_per_course_sections'] = True
		return data

	def get_video_skipped_plots(self, data):
		plots = self.vetp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_,
										 video_event_type='skip')
		if plots:
			data['videos_skipped'] = build_plot_images_dictionary(plots)
			self.options['has_video_skipped_data'] = True
		return data

	def get_video_skipped_plots_per_device_types(self, data):
		plots = self.vetp.analyze_video_events_device_types(self.context.period_breaks,
										 					self.context.minor_period_breaks,
										 					video_event_type='skip',
											 				theme_bw_=self.context.theme_bw_)
		if plots:
			data['videos_skipped_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_video_skipped_data_per_device_types'] = True
		return data

	def get_video_skipped_plots_per_enrollment_types(self, data):
		plots = self.vetp.analyze_video_events_enrollment_types(self.context.period_breaks,
										 						self.context.minor_period_breaks,
										 						video_event_type='skip',
											 					theme_bw_=self.context.theme_bw_)
		if plots:
			data['videos_skipped_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_video_skipped_data_per_enrollment_types'] = True
		return data

	def get_video_skipped_plots_per_course_sections(self, data):
		plots = self.vetp.analyze_video_events_per_course_sections(self.context.period_breaks,
												 				   self.context.minor_period_breaks,
												 				   video_event_type='skip',
													 			   theme_bw_=self.context.theme_bw_)
		self.options['has_video_skipped_data_per_course_sections'] = False
		if plots:
			data['videos_skipped_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_video_skipped_data_per_course_sections'] = True
		return data

View = VideosTimeseriesReport = VideosTimeseriesReportView
