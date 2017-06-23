#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

import json

from pyramid.view import view_config

from zope import interface

from nti.analytics_pandas.analysis import ResourceViewsTimeseries
from nti.analytics_pandas.analysis import ResourceViewsTimeseriesPlot

from nti.app.analytics_pandas.reports.report import PandasReportContext

from nti.app.analytics_pandas.views.interfaces import IResourceViewsTimeseriesContext

from .commons import get_course_names
from .commons import build_plot_images_dictionary

from .mixins import AbstractReportView

@interface.implementer(IResourceViewsTimeseriesContext)
class ResourceViewsTimeseriesContext(PandasReportContext):

	def __init__(self, *args, **kwargs):
		super(ResourceViewsTimeseriesContext, self).__init__(*args, **kwargs)

@view_config(name="ResourceViews",
			 renderer="../templates/resource_views.rml")
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
		json_data = json.loads(self.request.json)
		self.context = self._build_context(ResourceViewsTimeseriesContext, json_data)
		
		self.rvt = ResourceViewsTimeseries(self.db.session,
										   self.context.start_date,
										   self.context.end_date,
										   self.context.courses,
										   period=self.context.period)
		if self.rvt.dataframe.empty:
			self.options['has_resource_view_events'] = False
			return self.options

		self.options['has_resource_view_events'] = True

		course_names = get_course_names(self.db.session, self.context.courses)
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
