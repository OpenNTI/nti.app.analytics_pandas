#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: enrollments.py 115516 2017-06-19 16:50:24Z austin.graham $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from zope import interface

from nti.analytics_pandas.analysis import CourseDropsTimeseries
from nti.analytics_pandas.analysis import CourseDropsTimeseriesPlot

from nti.analytics_pandas.analysis import CourseCatalogViewsTimeseries
from nti.analytics_pandas.analysis import CourseCatalogViewsTimeseriesPlot

from nti.analytics_pandas.analysis import CourseEnrollmentsTimeseries
from nti.analytics_pandas.analysis import CourseEnrollmentsTimeseriesPlot

from nti.analytics_pandas.analysis import CourseEnrollmentsEventsTimeseries
from nti.analytics_pandas.analysis import CourseEnrollmentsEventsTimeseriesPlot

from nti.app.analytics_pandas.reports.report import PandasReportContext

from .commons import get_course_names
from .commons import build_plot_images_dictionary

from .mixins import AbstractReportView

class EnrollmentTimeseriesContext(PandasReportContext):

	def __init__(self, session=None, start_date=None, end_date=None, courses=None,
				 period_breaks='1 week', minor_period_breaks='1 day',
				 theme_bw_=True, number_of_most_active_user=10,
				 period='daily'):
		super(EnrollmentTimeseriesContext, self).__init__(session, start_date, 
														 end_date, courses, 
														 period_breaks, minor_period_breaks,
														 theme_bw_, number_of_most_active_user,
														 period)

Context = EnrollmentTimeseriesContext

class EnrollmentTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Enrollment Related Events')

	def _build_data(self, data=_('sample enrollment related events report')):
		keys = self.options.keys()
		if 'has_course_catalog_view_data' not in keys:
			self.options['has_course_catalog_view_data'] = False

		if 'has_course_enrollment_data' not in keys:
			self.options['has_course_enrollment_data'] = False

		if 'has_course_drop_data' not in keys:
			self.options['has_course_drop_data'] = False

		if 'has_enrollment_event_data' not in keys:
			self.options['has_enrollment_event_data'] = False

		self.options['data'] = data
		return self.options

	def __call__(self):
		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ", ".join(map(str, course_names))
		data = {}

		self.ccvt = CourseCatalogViewsTimeseries(self.context.session,
											   	 self.context.start_date,
											   	 self.context.end_date,
												 self.context.courses,
												 period=self.context.period)
		if self.ccvt.dataframe.empty:
			self.options['has_course_catalog_view_data'] = False
		else:
			self.options['has_course_catalog_view_data'] = True
			data = self.generate_course_catalog_view_plots(data)

		self.cet = CourseEnrollmentsTimeseries(self.context.session,
										   	   self.context.start_date,
										   	   self.context.end_date,
											   self.context.courses,
											   period=self.context.period)
		if self.cet.dataframe.empty:
			self.options['has_course_enrollment_data'] = False
		else:
			self.options['has_course_enrollment_data'] = True
			data = self.generate_course_enrollment_plots(data)

		self.cdt = CourseDropsTimeseries(self.context.session,
								   		 self.context.start_date,
								   		 self.context.end_date,
										 self.context.courses,
										 period=self.context.period)
		if self.cdt.dataframe.empty:
			self.options['has_course_drop_data'] = False
		else:
			self.options['has_course_drop_data'] = True
			data = self.generate_course_drop_plots(data)

		self.ceet = CourseEnrollmentsEventsTimeseries(cet=self.cet, cdt=self.cdt, ccvt=self.ccvt)
		if not self.ccvt.dataframe.empty or not self.cet.dataframe.empty or not self.cdt.dataframe.empty:
			self.options['has_enrollment_event_data'] = True
			data = self.generate_combined_enrollment_event_plots(data)
		else:
			self.options['has_enrollment_event_data'] = False

		self._build_data(data)
		return self.options

	def generate_course_catalog_view_plots(self, data):
		self.ccvtp = CourseCatalogViewsTimeseriesPlot(self.ccvt)
		data = self.get_course_catalog_view_plots(data)
		data = self.get_course_catalog_view_plots_per_device_types(data)
		return data

	def get_course_catalog_view_plots(self, data):
		plots = self.ccvtp.explore_events(self.context.period_breaks,
										  self.context.minor_period_breaks,
										  self.context.theme_bw_)
		if plots:
			data['course_catalog_views'] = build_plot_images_dictionary(plots)
		return data

	def get_course_catalog_view_plots_per_device_types(self, data):
		plots = self.ccvtp.analyze_device_types(self.context.period_breaks,
												self.context.minor_period_breaks,
												self.context.theme_bw_)
		self.options['has_course_catalog_views_per_device_types'] = False
		if plots:
			data['course_catalog_views_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_course_catalog_views_per_device_types'] = True
		return data

	def generate_course_enrollment_plots(self, data):
		self.cetp = CourseEnrollmentsTimeseriesPlot(self.cet)
		data = self.get_course_enrollment_plots(data)
		data = self.get_course_enrollment_plots_per_types(data)
		return data

	def get_course_enrollment_plots(self, data):
		plots = self.cetp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['course_enrollments'] = build_plot_images_dictionary(plots)
		return data

	def get_course_enrollment_plots_per_types(self, data):
		plots = self.cetp.analyze_device_enrollment_types(self.context.period_breaks,
														  self.context.minor_period_breaks,
														  self.context.theme_bw_)
		self.options['has_course_enrollments_per_types'] = False
		if plots:
			data['course_enrollments_per_types'] = build_plot_images_dictionary(plots)
			self.options['has_course_enrollments_per_types'] = True
		return data

	def generate_course_drop_plots(self, data):
		self.cdtp = CourseDropsTimeseriesPlot(self.cdt)
		data = self.get_course_drop_plots(data)
		if 'device_type' in self.cdt.dataframe.columns:
			data = self.get_course_drop_plots_per_device_types(data)
		else:
			self.options['has_course_drops_per_device_types'] = False

		if 'type_name' in self.cdt.dataframe.columns:
			data = self.get_course_drop_plots_per_enrollment_types(data)
		else:
			self.options['has_course_drops_per_enrollment_types'] = False

		return data

	def get_course_drop_plots(self, data):
		plots = self.cdtp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['course_drops'] = build_plot_images_dictionary(plots)
		return data

	def get_course_drop_plots_per_device_types(self, data):
		plots = self.cdtp.analyze_device_types(self.context.period_breaks,
											   self.context.minor_period_breaks,
											   self.context.theme_bw_)
		self.options['has_course_drops_per_device_types'] = False
		if plots:
			data['course_drops_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_course_drops_per_device_types'] = True
		return data

	def get_course_drop_plots_per_enrollment_types(self, data):
		plots = self.cdtp.analyze_enrollment_types(self.context.period_breaks,
												   self.context.minor_period_breaks,
												   self.context.theme_bw_)
		self.options['has_course_drops_per_enrollment_types'] = False
		if plots:
			data['course_drops_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_course_drops_per_enrollment_types'] = True
		return data

	def generate_combined_enrollment_event_plots(self, data):
		self.ceetp = CourseEnrollmentsEventsTimeseriesPlot(self.ceet)
		data = self.get_course_enrollments_vs_drops_plots(data)
		data = self.get_course_enrollments_vs_catalog_views_plots(data)
		return data

	def get_course_enrollments_vs_drops_plots(self, data):
		plots = self.ceetp.explore_course_enrollments_vs_drops(self.context.period_breaks,
															   self.context.minor_period_breaks,
															   self.context.theme_bw_)
		self.options['has_course_enrollments_vs_drops'] = False
		if plots:
			data['course_enrollments_vs_drops'] = build_plot_images_dictionary(plots)
			self.options['has_course_enrollments_vs_drops'] = True
		return data

	def get_course_enrollments_vs_catalog_views_plots(self, data):
		plots = self.ceetp.explore_course_catalog_views_vs_enrollments(self.context.period_breaks,
																	   self.context.minor_period_breaks,
																	   self.context.theme_bw_)
		self.options['has_course_enrollments_vs_catalog_views'] = False
		if plots:
			data['course_enrollments_vs_catalog_views'] = build_plot_images_dictionary(plots)
			self.options['has_course_enrollments_vs_catalog_views'] = True
		return data

View = EnrollmentTimeseriesReport = EnrollmentTimeseriesReportView
