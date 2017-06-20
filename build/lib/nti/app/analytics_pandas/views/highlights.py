#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: highlights.py 115516 2017-06-19 16:50:24Z austin.graham $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from zope import interface

from nti.analytics_pandas.analysis import HighlightsCreationTimeseries
from nti.analytics_pandas.analysis import HighlightsCreationTimeseriesPlot

from .commons import get_course_names
from .commons import build_plot_images_dictionary
from .commons import build_images_dict_from_plot_dict

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class HighlightsTimeseriesContext(object):

	def __init__(self, session=None, start_date=None, end_date=None, courses=None,
				 period_breaks=None, minor_period_breaks=None, theme_bw_=True,
				 number_of_most_active_user=10, period='daily'):
		self.session = session
		self.courses = courses
		self.end_date = end_date
		self.start_date = start_date
		self.period_breaks = period_breaks
		self.theme_bw_ = theme_bw_
		self.minor_period_breaks = minor_period_breaks
		self.number_of_most_active_user = number_of_most_active_user
		self.period = period

Context = HighlightsTimeseriesContext

class HighlightsTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Highlight Events Report')

	def _build_data(self, data=_('sample highlights created events report')):
		keys = self.options.keys()
		if 'has_highlight_data' not in keys:
			self.options['has_highlight_data'] = False

		if 'has_highlight_data_per_device_types' not in keys:
			self.options['has_highlight_data_per_device_types'] = False

		if 'has_highlight_data_per_resource_types' not in keys:
			self.options['has_highlight_data_per_resource_types'] = False

		if 'has_highlight_created_users' not in keys:
			self.options['has_highlight_created_users'] = False

		if 'has_highlight_data_per_course_sections' not in keys:
			self.options['has_highlight_data_per_course_sections'] = False

		if 'has_highlight_data_per_enrollment_types' not in keys:
			self.options['has_highlight_data_per_enrollment_types'] = False

		self.options['data'] = data
		return self.options

	def __call__(self):
		self.hct = HighlightsCreationTimeseries(self.context.session,
										   		self.context.start_date,
										   		self.context.end_date,
										   		self.context.courses,
										   		period=self.context.period)
		if self.hct.dataframe.empty:
			self.options['has_highlight_data'] = False
			return self.options

		self.options['has_highlight_data'] = True

		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ", ".join(map(str, course_names))
		data = {}
		data = self.generate_highlights_created_plots(data)
		self._build_data(data)
		return self.options

	def generate_highlights_created_plots(self, data):
		self.hctp = HighlightsCreationTimeseriesPlot(self.hct)
		data = self.get_highlights_created_plots(data)
		data = self.get_highlights_created_plots_per_device_types(data)
		data = self.get_highlights_created_plots_per_resource_types(data)
		data = self.get_the_most_active_users_plot(data)
		if len(self.context.courses) > 1:
			data = self.get_highlights_created_plots_per_course_sections(data)
			self.options['has_highlight_data_per_course_sections'] = True
		return data

	def get_highlights_created_plots(self, data):
		plots = self.hctp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['highlights_created'] = build_plot_images_dictionary(plots)
		return data

	def get_highlights_created_plots_per_device_types(self, data):
		plots = self.hctp.analyze_device_types(self.context.period_breaks,
										 	   self.context.minor_period_breaks,
										 	   self.context.theme_bw_)
		if plots:
			data['highlights_created_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_highlight_data_per_device_types'] = True
		return data

	def get_highlights_created_plots_per_enrollment_types(self, data):
		plots = self.hctp.analyze_enrollment_types(self.context.period_breaks,
										 	   self.context.minor_period_breaks,
										 	   self.context.theme_bw_)
		if plots:
			data['highlights_created_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_highlight_data_per_enrollment_types'] = True
		return data

	def get_highlights_created_plots_per_resource_types(self, data):
		plots = self.hctp.analyze_resource_types(self.context.period_breaks,
										 		 self.context.minor_period_breaks,
										 		 self.context.theme_bw_)
		if plots:
			data['highlights_created_per_resource_types'] = build_plot_images_dictionary(plots)
			self.options['has_highlight_data_per_resource_types'] = True
		return data

	def get_the_most_active_users_plot(self, data):
		plot = self.hctp.plot_the_most_active_users(self.context.number_of_most_active_user)
		if plot:
			data['highlight_created_users'] = build_plot_images_dictionary(plot)
			self.options['has_highlight_created_users'] = True
		return data

	def get_highlights_created_plots_per_course_sections(self, data):
		plots = self.hctp.analyze_events_per_course_sections(self.context.period_breaks,
										 		 			 self.context.minor_period_breaks,
										 		 			 self.context.theme_bw_)
		if plots:
			data['highlights_created_per_course_sections'] = build_images_dict_from_plot_dict(plots)
		return data

View = HighlightsTimeseriesReport = HighlightsTimeseriesReportView
