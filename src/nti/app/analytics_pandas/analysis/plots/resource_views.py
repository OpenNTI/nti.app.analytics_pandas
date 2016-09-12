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

import numpy as np

from zope.i18n import translate

from .commons import generate_three_plots
from .commons import line_plot_x_axis_date
from .commons import group_line_plot_x_axis_date
from .commons import group_scatter_plot_x_axis_date
from .commons import generate_three_group_by_plots
from .commons import histogram_plot_x_axis_discrete
from .commons import generate_plot_names as generate_plot_names_

class  ResourceViewsTimeseriesPlot(object):

	def __init__(self, rvt):
		"""
		rvt = ResourceViewsTimeseries
		"""
		self.rvt = rvt
		self.period = rvt.period

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day',
					   theme_seaborn_=True):
		"""
		return scatter plots of resource views during period of time
		it consists of:
			- number of resource views
			- number of unique users
			- ratio of resource views over unique users
		"""
		rvt = self.rvt
		df = rvt.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of resource views during time period')
		user_title = _('Number of unique users viewing resources during time period')
		ratio_title = _('Ratio of resource views over unique users during time period')
		unique_resource_title = _('Number of unique resources viewed during time period')
		event_type = 'resource_views'
		plots = self.generate_plots(df,
									event_title,
									user_title,
									ratio_title,
									unique_resource_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_,
									event_type)
		return plots

	def analyze_events_per_course_sections(self, period_breaks='1 week',
										   minor_period_breaks='1 day',
										   theme_seaborn_=True):
		rvt = self.rvt
		df = rvt.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of resource views per course sections')
			user_title = _('Number of unique users viewing resources per course sections')
			ratio_title = _('Ratio of resource views over unique users per course sections')
			unique_resource_title = _('Number of unique resources viewed per course sections')
			event_type = 'resource_views_per_course_sections'
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 unique_resource_title,
															 period_breaks,
															 minor_period_breaks,
															 theme_seaborn_,
															 event_type)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = translate(_("Number of resource views in  ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users viewing resources in ${title}",
									  mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of resource views over unique user in ${title}",
									  mapping={'title': context_name}))

			unique_resource_title = translate(_("Number of unique resources viewed in ${title}",
									 		  mapping={'title': context_name}))

			event_type = 'resource_views_in_%s' % (context_name.replace(' ', '_'))
			section_plots = self.generate_plots(new_df,
												event_title,
												user_title,
												ratio_title,
												unique_resource_title,
												period_breaks,
												minor_period_breaks,
												theme_seaborn_,
												event_type)
			plots.append(section_plots)
		return plots

	def generate_plots(self,
					   df,
					   event_title,
					   user_title,
					   ratio_title,
					   unique_resource_title,
					   period_breaks,
					   minor_period_breaks,
					   theme_seaborn_,
					   event_type=None):
		event_y_axis_field = 'number_of_resource_views'
		event_y_axis_label = _('Number of resource views')
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
		unique_event_name = None
		if event_type is not None:
			unique_event_name = 'unique_event_%s' % event_type
		plot_unique_resources = line_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_of_unique_resource',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of unique resources viewed'),
											title=unique_resource_title,
											period_breaks=period_breaks,
											minor_breaks=minor_period_breaks,
											theme_seaborn_=theme_seaborn_,
											plot_name=unique_event_name,
											period=self.period)
		plots = plots + (plot_unique_resources,)
		return plots

	def generate_group_by_plots(self,
								df,
								group_by,
								event_title,
								user_title,
								ratio_title,
								unique_resource_title,
								period_breaks,
								minor_period_breaks,
								theme_seaborn_,
								event_type=None):

		event_y_axis_field = 'number_of_resource_views'
		event_y_axis_label = _('Number of resource views')
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
		unique_event_name = None
		if event_type is not None:
			unique_event_name = 'unique_event_%s' % event_type
		if 'device_type' in group_by:
			group_by = 'application_type'
			unique_resource_title = unique_resource_title.replace('device' , 'application')
		plot_unique_resources = group_line_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_of_unique_resource',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of unique resources viewed'),
											title=unique_resource_title,
											period_breaks=period_breaks,
											group_by=group_by,
											minor_breaks=minor_period_breaks,
											theme_seaborn_=theme_seaborn_,
											plot_name=unique_event_name,
											period=self.period)
		plots = plots + (plot_unique_resources,)
		return plots

	def generate_group_by_scatter_plots(self,
										df,
										group_by,
										event_title,
										user_title,
										ratio_title,
										unique_resource_title,
										period_breaks,
										minor_period_breaks,
										theme_seaborn_,
										event_type=None):

		event_name, user_event_name, ratio_event_name, unique_event_name = self.generate_plot_names(event_type)

		plot_resource_views = group_scatter_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_of_resource_views',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of resource views'),
											title=event_title,
											period_breaks=period_breaks,
											group_by=group_by,
											minor_breaks=minor_period_breaks,
											theme_seaborn_=theme_seaborn_,
											plot_name=event_name)

		plot_unique_users = group_scatter_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_of_unique_users',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of unique users'),
											title=user_title,
											period_breaks=period_breaks,
											group_by=group_by,
											minor_breaks=minor_period_breaks,
											theme_seaborn_=theme_seaborn_,
											plot_name=user_event_name)

		plot_ratio = group_scatter_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='ratio',
											x_axis_label=_('Date'),
											y_axis_label=_('Ratio'),
											title=ratio_title,
											period_breaks=period_breaks,
											group_by=group_by,
											minor_breaks=minor_period_breaks,
											theme_seaborn_=theme_seaborn_,
											plot_name=ratio_event_name)

		plot_unique_resources = group_scatter_plot_x_axis_date(
											df=df,
											x_axis_field='timestamp_period',
											y_axis_field='number_of_unique_resource',
											x_axis_label=_('Date'),
											y_axis_label=_('Number of unique resources viewed'),
											title=unique_resource_title,
											period_breaks=period_breaks,
											group_by=group_by,
											minor_breaks=minor_period_breaks,
											theme_seaborn_=theme_seaborn_,
											plot_name=unique_event_name)

		return (plot_resource_views, plot_unique_users, plot_ratio, plot_unique_resources)

	def analyze_resource_type(self, period_breaks='1 week',
							  minor_period_breaks='1 day',
							  theme_seaborn_=True):
		"""
		plot resource views based on resource type
		"""

		rvt = self.rvt
		df = rvt.analyze_events_based_on_resource_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'resource_type'
		event_title = _('Number of resource views on each resource type')
		user_title = _('Number of unique users viewing each resource type at given time period')
		ratio_title = _('Ratio of resource views over unique users grouped by resource type')
		unique_resource_title = _('Number of unique course resource viewed during time period')
		event_type = 'resource_views_per_resource_types'
		plots = self.generate_group_by_plots(
									df,
									group_by,
									event_title,
									user_title,
									ratio_title,
									unique_resource_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_,
									event_type)
		return plots

	def analyze_resource_type_scatter_plot(self, period_breaks='1 week',
										   minor_period_breaks='1 day',
										   theme_seaborn_=True):
		"""
		plot resource views based on resource type
		"""

		rvt = self.rvt
		df = rvt.analyze_events_based_on_resource_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_resource_views'] / df['number_of_unique_users']

		group_by = 'resource_type'
		event_title = _('Number of resource views on each resource type')
		user_title = _('Number of unique users viewing each resource type at given time period')
		ratio_title = _('Ratio of resource views over unique users grouped by resource type')
		unique_resource_title = _('Number of unique course resource viewed during time period')
		event_type = 'resource_views_per_resource_types_scatter_plot'
		plots = self.generate_group_by_scatter_plots(
											df,
											group_by,
											event_title,
											user_title,
											ratio_title,
											unique_resource_title,
											period_breaks,
											minor_period_breaks,
											theme_seaborn_,
											event_type)
		return plots

	def analyze_device_type(self, period_breaks='1 week', minor_period_breaks='1 day',
							theme_seaborn_=True):
		"""
		plot course resource views based on device type (user agent)
		"""

		rvt = self.rvt
		df = rvt.analyze_events_based_on_device_type()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'device_type'
		event_title = _('Number of resource views per device type')
		user_title = _('Number of unique users viewing resources per device type')
		ratio_title = _('Ratio of resource views over unique users grouped by device type')
		unique_resource_title = _('Number of unique course resource viewed during time period')
		event_type = 'resource_views_per_device_types'
		plots = self.generate_group_by_plots(
									df,
									group_by,
									event_title,
									user_title,
									ratio_title,
									unique_resource_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_,
									event_type)
		return plots

	def analyze_enrollment_type(self, period_breaks='1 week', minor_period_breaks='1 day',
								theme_seaborn_=True):
		"""
		plot course resource views based on enrollment type
		"""

		rvt = self.rvt
		df = rvt.analyze_events_based_on_enrollment_type()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'enrollment_type'
		event_title = _('Number of resource views per enrollment type')
		user_title = _('Number of unique users viewing resource per enrollment type')
		ratio_title = _('Ratio of resource views over unique users per enrollment type')
		unique_resource_title = _('Number of unique course resource viewed during time period')
		event_type = 'resource_views_per_enrollment_types'
		plots = self.generate_group_by_plots(
									df,
									group_by,
									event_title,
									user_title,
									ratio_title,
									unique_resource_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_,
									event_type)
		return plots

	def analyze_device_type_scatter_plot(self, period_breaks='1 week', 
										 minor_period_breaks='1 day',
										 theme_seaborn_=True):
		"""
		plot course resource views based on device type (user agent)
		"""

		rvt = self.rvt
		df = rvt.analyze_events_based_on_device_type()
		if df is None:
			return ()

		df.reset_index(inplace=True, drop=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'device_type'
		event_title = _('Number of resource views on each device type')
		user_title = _('Number of unique users viewing each device type at given time period')
		ratio_title = _('Ratio of resource views over unique users grouped by device type')
		unique_resource_title = _('Number of unique course resource viewed during time period')
		event_type = 'resource_views_per_device_types_scatter_plot'
		plots = self.generate_group_by_scatter_plots(
										df,
										group_by,
										event_title,
										user_title,
										ratio_title,
										unique_resource_title,
										period_breaks,
										minor_period_breaks,
										theme_seaborn_,
										event_type)
		return plots

	def plot_most_active_users(self, max_rank_number=10):
		rvt = self.rvt
		users_df = rvt.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		users_df.rename(columns={'number_of_activities': 'number_of_resource_views'},
						inplace=True)
		event_type = 'most_active_users_viewing_resources'
		plot_users = histogram_plot_x_axis_discrete(
										df=users_df,
										x_axis_field='username' ,
										y_axis_field='number_of_resource_views',
										x_axis_label=_('Username'),
										y_axis_label=_('Number of resource views'),
										title=_('The most active users viewing resource'),
										stat='identity',
										plot_name=event_type)
		return (plot_users,)

	def generate_plot_names(self, event_type):
		event_name, user_event_name, ratio_event_name = generate_plot_names_(event_type)
		if event_type is not None:
			unique_event_name = 'unique_%s' % event_type
		return (event_name, user_event_name, ratio_event_name, unique_event_name)
