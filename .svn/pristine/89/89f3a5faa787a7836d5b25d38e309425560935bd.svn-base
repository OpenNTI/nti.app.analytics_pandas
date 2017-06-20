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

from nti.analytics_pandas.analysis import BookmarksTimeseriesPlot
from nti.analytics_pandas.analysis import BookmarkCreationTimeseries

from .commons import get_course_names
from .commons import build_plot_images_dictionary
from .commons import build_images_dict_from_plot_dict

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class BookmarksTimeseriesContext(object):

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

Context = BookmarksTimeseriesContext

class BookmarksTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Bookmarks Report')

	def _build_data(self, data=_('sample bookmarks related events report')):
		keys = self.options.keys()
		if 'has_bookmark_data' not in keys:
			self.options['has_bookmark_data'] = False

		if 'has_bookmark_data_per_device_types' not in keys:
			self.options['has_bookmark_data_per_device_types'] = False

		if 'has_bookmark_data_per_resource_types' not in keys:
			self.options['has_bookmark_data_per_resource_types'] = False

		if 'has_bookmark_created_users' not in keys:
			self.options['has_bookmark_created_users'] = False

		if 'has_bookmark_data_per_course_sections' not in keys:
			self.options['has_bookmark_data_per_course_sections'] = False

		if 'has_bookmark_data_per_enrollment_types' not in keys:
			self.options['has_bookmark_data_per_enrollment_types'] = False

		self.options['data'] = data
		return self.options

	def __call__(self):
		self.bct = BookmarkCreationTimeseries(self.context.session,
										   	  self.context.start_date,
										   	  self.context.end_date,
											  self.context.courses,
											  period=self.context.period)
		if self.bct.dataframe.empty:
			self.options['has_bookmark_data'] = False
			return self.options
		else:
			self.options['has_bookmark_data'] = True

		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ", ".join(map(str, course_names))

		data = {}
		data = self.generate_bookmarks_created_plots(data)
		self._build_data(data)
		return self.options

	def generate_bookmarks_created_plots(self, data):
		self.bctp = BookmarksTimeseriesPlot(self.bct)
		data = self.get_bookmarks_created_plots(data)
		data = self.get_bookmarks_created_plots_per_device_types(data)
		data = self.get_bookmarks_created_plots_per_enrollment_types(data)
		data = self.get_bookmarks_created_plots_per_resource_types(data)
		data = self.get_the_most_active_users_plot(data)
		if len(self.context.courses) > 1:
			data = self.get_bookmarks_created_plots_per_course_sections(data)
		else:
			self.options['has_bookmark_data_per_course_sections'] = False
		return data

	def get_bookmarks_created_plots(self, data):
		plots = self.bctp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['bookmarks_created'] = build_plot_images_dictionary(plots)
		return data

	def get_bookmarks_created_plots_per_device_types(self, data):
		plots = self.bctp.analyze_device_types(self.context.period_breaks,
										 	   self.context.minor_period_breaks,
										 	   self.context.theme_bw_)
		if plots:
			data['bookmarks_created_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_bookmark_data_per_device_types'] = True
		return data

	def get_bookmarks_created_plots_per_enrollment_types(self, data):
		plots = self.bctp.analyze_enrollment_types(self.context.period_breaks,
										 	   self.context.minor_period_breaks,
										 	   self.context.theme_bw_)
		if plots:
			data['bookmarks_created_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_bookmark_data_per_enrollment_types'] = True
		return data

	def get_bookmarks_created_plots_per_resource_types(self, data):
		plots = self.bctp.analyze_resource_types(self.context.period_breaks,
										 	   	 self.context.minor_period_breaks,
										 	   	 self.context.theme_bw_)
		if plots:
			data['bookmarks_created_per_resource_types'] = build_images_dict_from_plot_dict(plots)
			self.options['has_bookmark_data_per_resource_types'] = True
		return data

	def get_the_most_active_users_plot(self, data):
		plot = self.bctp.plot_the_most_active_users(self.context.number_of_most_active_user)
		if plot:
			data['bookmark_created_users'] = build_plot_images_dictionary(plot)
			self.options['has_bookmark_created_users'] = True
		return data

	def get_bookmarks_created_plots_per_course_sections(self, data):
		plots = self.bctp.analyze_events_per_course_sections(self.context.period_breaks,
										 	   	 			 self.context.minor_period_breaks,
										 	   	 			 self.context.theme_bw_)
		if plots:
			data['bookmarks_created_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_bookmark_data_per_course_sections'] = True
		return data

View = BookmarksTimeseriesReport = BookmarksTimeseriesReportView
