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

from ...analysis import ResourceViewsTimeseries
from ...analysis import ResourceViewsTimeseriesPlot

from .commons import get_course_names
from .commons import build_plot_images_dictionary

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class ResourceViewsTimeseriesContext(object):

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

Context = ResourceViewsTimeseriesContext

class ResourceViewsTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Resource Views')

	def _build_data(self, data=_('sample resource views report')):
		keys = self.options.keys()
		if 'has_resource_view_events' not in keys:
			self.options['has_resource_view_events'] = False

		if 'has_resource_views_per_enrollment_types' not in keys:
			self.options['has_resource_views_per_enrollment_types'] = False

		if 'has_resource_views_per_device_types' not in keys:
			self.options['has_resource_views_per_device_types'] = False

		if 'has_resource_views_per_resource_types' not in keys:
			self.options['has_resource_views_per_resource_types'] = False

		if 'has_resource_view_users' not in keys:
			self.options['has_resource_view_users'] = False

		self.options['data'] = data
		return self.options

	def __call__(self):
		self.rvt = ResourceViewsTimeseries(self.context.session,
										   self.context.start_date,
										   self.context.end_date,
										   self.context.courses,
										   period=self.context.period)
		if self.rvt.dataframe.empty:
			self.options['has_resource_view_events'] = False
			return self.options

		self.options['has_resource_view_events'] = True

		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ",".join(map(str, course_names))

		self.rvtp = ResourceViewsTimeseriesPlot(self.rvt)
		data = {}
		data = self.get_resource_view_events(data)
		data = self.get_resource_views_per_device_types(data)
		data = self.get_resource_views_per_resource_types(data)
		data = self.get_the_most_active_users(data)
		self._build_data(data)
		return self.options

	def get_resource_view_events(self, data):
		plots = self.rvtp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['resource_view_events'] = build_plot_images_dictionary(plots)
		return data

	def get_resource_views_per_device_types(self, data):
		plots = self.rvtp.analyze_device_type(self.context.period_breaks,
											  self.context.minor_period_breaks,
											  self.context.theme_bw_)
		if plots:
			data['resource_views_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_resource_views_per_device_types'] = True
		return data

	def get_resource_views_per_enrollment_types(self, data):
		plots = self.rvtp.analyze_enrollment_type(self.context.period_breaks,
											  self.context.minor_period_breaks,
											  self.context.theme_bw_)
		if plots:
			data['resource_views_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_resource_views_per_enrollment_types'] = True
		return data

	def get_resource_views_per_resource_types(self, data):
		plots = self.rvtp.analyze_resource_type(self.context.period_breaks,
												self.context.minor_period_breaks,
												self.context.theme_bw_)
		if plots:
			data['resource_views_per_resource_types'] = build_plot_images_dictionary(plots)
			self.options['has_resource_views_per_resource_types'] = True
		return data

	def get_the_most_active_users(self, data):
		plots = self.rvtp.plot_most_active_users(self.context.number_of_most_active_user)
		if plots:
			data['resource_view_users'] = build_plot_images_dictionary(plots)
			self.options['has_resource_view_users'] = True
		return data

View = ResourceViewsTimeseriesReport = ResourceViewsTimeseriesReportView
