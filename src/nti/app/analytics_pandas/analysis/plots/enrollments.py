#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

import pandas as pd

from .commons import generate_three_plots
from .commons import line_plot_x_axis_date
from .commons import group_line_plot_x_axis_date
from .commons import generate_three_group_by_plots

class CourseCatalogViewsTimeseriesPlot(object):

	def __init__(self, ccvt):
		"""
		ccvt = CourseCatalogViewsTimeseries
		"""
		self.ccvt = ccvt
		self.period = ccvt.period

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day', theme_seaborn_=True):
		"""
		return scatter plots of course catalog views during period of time
		it consists of:
			- number of course catalog views
			- number of unique users
			- ratio of course catalog views over unique users
		"""
		ccvt = self.ccvt
		df = ccvt.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		event_title = _('Course catalog views during time period')
		user_title = _('Number of unique users viewing course catalog')
		ratio_title = _('Ratio of course catalog views over unique user')
		event_type = 'course_catalog_views'
		event_y_axis_field = 'number_of_course_catalog_views'
		event_y_axis_label = 'Number of course catalog views'
		plots = generate_three_plots(df,
									 event_title,
									 user_title,
									 ratio_title,
									 event_y_axis_field,
									 event_y_axis_label,
									 period_breaks,
									 minor_period_breaks,
									 theme_seaborn_,
									 event_type,
									 period=self.period)

		plot_average_time_length = line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='average_time_length',
										x_axis_label=_('Date'),
										y_axis_label=_('Average time length'),
										title=_('Average time length viewing course catalog'),
										period_breaks=period_breaks,
										minor_breaks=minor_period_breaks,
										plot_name='average_time_length',
										period=self.period)

		plots = plots + (plot_average_time_length,)
		return plots

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day', theme_seaborn_=True):
		"""
		plot course catalog views based on user agent (device type)
		the plots consists of:
		- average time length users spent on viewing course catalog during time period
		- number of unique users during time period for each type of user agent
		"""
		ccvt = self.ccvt
		df = ccvt.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'device_type'
		event_title = _('Number of course catalog views per device_type')
		user_title = _('Number of unique users viewing course catalog per device_type')
		ratio_title = _('Ratio of course catalog views over unique user per device_type')
		event_type = 'course_catalog_views_per_device_types'
		event_y_axis_field = 'number_of_course_catalog_views'
		event_y_axis_label = 'Number of course catalog views'
		plots = generate_three_group_by_plots(df,
											  group_by,
											  event_title,
											  user_title,
											  ratio_title,
											  event_y_axis_field,
											  event_y_axis_label,
											  period_breaks,
											  minor_period_breaks,
											  theme_seaborn_,
											  event_type,
											  period=self.period)

		plot_average_time_length = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='average_time_length',
										x_axis_label=_('Date'),
										y_axis_label=_('Average time length'),
										title=_('Average time length viewing course catalog per application type'),
										period_breaks=period_breaks,
										group_by='application_type',
										minor_breaks=minor_period_breaks,
										plot_name='average_time_length_per_device_types',
										period=self.period)

		plots = plots + (plot_average_time_length,)
		return plots

class CourseEnrollmentsTimeseriesPlot(object):

	def __init__(self, cet):
		"""
		cevt = CourseEnrollmentsTimeseries
		"""
		self.cet = cet
		self.period = cet.period

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day', theme_seaborn_=True):
		"""
		return scatter plots of course enrollments during period of time
		"""
		cet = self.cet
		df = cet.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_course_enrollments = line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_enrollments',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of enrollments'),
										title=_('Number of enrollments during period of time'),
										period_breaks=period_breaks,
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_,
										plot_name='course_enrollments',
										period=self.period)
		return (plot_course_enrollments,)

	def analyze_device_enrollment_types(self, period_breaks='1 month', minor_period_breaks='1 week', theme_seaborn_=True):
		"""
		return plots of the course enrollments grouped by user agent (device_type) and enrollment type
		"""
		cet = self.cet
		df = cet.analyze_device_enrollment_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df.rename(columns={	'type_name':'enrollment_type'}, inplace=True)

		plot_course_enrollments_by_device = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_enrollments',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of enrollments'),
										title=_('Number of enrollments per device types during period of time'),
										period_breaks=period_breaks,
										group_by='device_type',
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_,
										plot_name='course_enrollments_per_device_types',
										period=self.period)

		plot_course_enrollments_by_type = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_enrollments',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of enrollments'),
										title=_('Number of course enrollments per enrollment types during period of time'),
										period_breaks=period_breaks,
										group_by='enrollment_type',
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_,
										plot_name='course_enrollments_per_enrollment_types',
										period=self.period)

		return (plot_course_enrollments_by_device, plot_course_enrollments_by_type)

class CourseDropsTimeseriesPlot(object):

	def __init__(self, cdt):
		"""
		cdvt = CourseDropsTimeseries
		"""
		self.cdt = cdt
		self.period = cdt.period

	def explore_events(self, period_breaks='1 month', minor_period_breaks='1 week', theme_seaborn_=True):
		"""
		return scatter plots of course enrollments during period of time
		"""
		cdt = self.cdt
		df = cdt.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_course_drops = line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_course_drops',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of drops'),
										title=_('Number of course drops during period of time'),
										period_breaks=period_breaks,
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_,
										plot_name='course_drops',
										period=self.period)
		return (plot_course_drops,)

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day', theme_seaborn_=True):
		"""
		return plots of the course drops grouped by user agent (device_type)
		"""
		cdt = self.cdt
		df = cdt.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot_course_drops_by_device = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_course_drops',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of course drops'),
										title=_('Number of course drops per device types during period of time'),
										period_breaks=period_breaks,
										group_by='device_type',
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_,
										plot_name='course_drops_per_device_types',
										period=self.period)

		return (plot_course_drops_by_device,)

	def analyze_enrollment_types(self, period_breaks='1 week', minor_period_breaks='1 day', theme_seaborn_=True):
		"""
		return plots of the course drops grouped by enrollment types
		"""
		cdt = self.cdt
		df = cdt.analyze_enrollment_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		df.rename(columns={	'type_name':'enrollment_type'}, inplace=True)

		plot_course_drops_by_enrollment_type = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_course_drops',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of course drops'),
										title=_('Number of course course drops per enrollment types during period of time'),
										period_breaks=period_breaks,
										group_by='enrollment_type',
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_,
										plot_name='course_drops_per_enrollment_types',
										period=self.period)

		return (plot_course_drops_by_enrollment_type,)

class CourseEnrollmentsEventsTimeseriesPlot(object):

	def __init__(self, ceet):
		"""
		ceet = CourseEnrollmentsEventsTimeseries
		"""
		self.ceet = ceet
		self.period = ceet.period

	def explore_course_enrollments_vs_drops(self, period_breaks='1 week',
											minor_period_breaks='1 day',
											theme_seaborn_=True):
		ceet = self.ceet
		df = ceet.explore_course_enrollments_vs_drops()
		if len(df.index) <= 0:
			return ()

		plot_enrollments_events = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='total_events',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of events'),
										title=_('Number of course enrollments vs drops during period of time'),
										period_breaks=period_breaks,
										group_by='event_type',
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_,
										plot_name='course_enrollments_vs_drops',
										period=self.period)

		return (plot_enrollments_events,)

	def explore_course_catalog_views_vs_enrollments(self, period_breaks='1 week',
													minor_period_breaks='1 day',
													theme_seaborn_=True):
		ceet = self.ceet
		df = ceet.explore_course_catalog_views_vs_enrollments()
		if len(df.index) <= 0:
			return ()

		plot_enrollments_events = group_line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='total_events',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of events'),
									title=_('Number of course catalog views vs enrollments during period of time'),
									period_breaks=period_breaks,
									group_by='event_type',
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_,
									plot_name='course_enrollments_vs_catalog_views',
									period=self.period)

		return (plot_enrollments_events,)
