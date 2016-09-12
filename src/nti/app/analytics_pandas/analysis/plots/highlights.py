#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .. import MessageFactory as _

import pandas as pd

import numpy as np

from zope.i18n import translate

from .commons import generate_three_plots
from .commons import generate_three_group_by_plots
from .commons import histogram_plot_x_axis_discrete

class HighlightsCreationTimeseriesPlot(object):

	def __init__(self, hct):
		"""
		hct = HighlightsCreationTimeseries
		"""
		self.hct = hct
		self.period = hct.period

	def explore_events(self, period_breaks='1 week',
					   minor_period_breaks='1 day',
					   theme_seaborn_=True):
		hct = self.hct
		df = hct.analyze_events()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of highlights created during period of time')
		user_title = _('Number of unique users creating highlights during period of time')
		ratio_title = _('Ratio of highlights created over unique users during period of time')
		event_type = 'highlights_created'
		plots = self.generate_plots(df,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_,
									event_type)
		return plots

	def analyze_events_per_course_sections(self, period_breaks='1 week',
										   minor_period_breaks='1 day',
										   theme_seaborn_=True):
		hct = self.hct
		df = hct.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = {}
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of highlights created per course sections')
			user_title = _('Number of unique users creating highlights per course sections')
			ratio_title = _('Ratio of highlights created over unique user per course sections')
			event_type = 'highlights_created_per_course_sections'
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks,
															 theme_seaborn_,
															 event_type)
			plots['all_section_plots'] = all_section_plots

		section_plots_dict = {}
		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = translate(_("Number of highlights created in ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users creating highlights in ${title}",
									  mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of highlights created over unique user in ${title}",
									  mapping={'title': context_name}))
			event_type = 'highlights_created_in_%s' % (context_name.replace(' ', '_'))
			section_plots = self.generate_plots(new_df,
												event_title,
												user_title,
												ratio_title,
												period_breaks,
												minor_period_breaks,
												theme_seaborn_,
												event_type)
			key = 'section_%s' % (course_id)
			section_plots_dict[key] = section_plots
		plots['section_plots'] = section_plots_dict
		return plots

	def analyze_device_types(self, period_breaks='1 week',
							 minor_period_breaks='1 day',
							 theme_seaborn_=True):
		hct = self.hct
		df = hct.analyze_device_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of highlights created grouped by device types')
		user_title = _('Number of unique users created highlights grouped by device types')
		ratio_title = _('Ratio of highlights created over unique users grouped by device types')
		event_type = 'highlights_created_per_device_types'
		plots = self.generate_group_by_plots(df,
											 group_by,
											 event_title,
											 user_title,
											 ratio_title,
											 period_breaks,
											 minor_period_breaks,
											 theme_seaborn_,
											 event_type)
		return plots

	def analyze_enrollment_types(self, period_breaks='1 week',
							 	 minor_period_breaks='1 day',
							 	 theme_seaborn_=True):
		hct = self.hct
		df = hct.analyze_enrollment_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'enrollment_type'
		event_title = _('Number of highlights created grouped by enrollment types')
		user_title = _('Number of unique users created highlights grouped by enrollment types')
		ratio_title = _('Ratio of highlights created over unique users grouped by enrollment types')
		event_type = 'highlights_created_per_enrollment_types'
		plots = self.generate_group_by_plots(df,
											 group_by,
											 event_title,
											 user_title,
											 ratio_title,
											 period_breaks,
											 minor_period_breaks,
											 theme_seaborn_,
											 event_type)
		return plots

	def generate_plots(self,
					   df,
					   event_title,
					   user_title,
					   ratio_title,
					   period_breaks,
					   minor_period_breaks,
					   theme_seaborn_,
					   event_type=None):
		event_y_axis_field = 'number_of_highlights_created'
		event_y_axis_label = _('Number of highlights created')
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
		return plots

	def generate_group_by_plots(self,
								df,
								group_by,
								event_title,
								user_title,
								ratio_title,
								period_breaks,
								minor_period_breaks,
								theme_seaborn_,
								event_type=None):
		event_y_axis_field = 'number_of_highlights_created'
		event_y_axis_label = _('Number of highlights created')
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
		return plots

	def analyze_resource_types(self,
							   period_breaks='1 week',
							   minor_period_breaks='1 day',
							   theme_seaborn_=True):
		hct = self.hct
		df = hct.analyze_resource_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'resource_type'
		event_title = _('Number of highlights created grouped by resource types')
		user_title = _('Number of unique users created highlights grouped by resource types')
		ratio_title = _('Ratio of highlights created over unique users grouped by resource types')
		event_type = 'highlights_created_per_resource_types'
		plots = self.generate_group_by_plots(
									df,
									group_by,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_,
									event_type)

		return plots

	def plot_the_most_active_users(self, max_rank_number=10):
		hct = self.hct
		users_df = hct.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(
											df=users_df,
											x_axis_field='username' ,
											y_axis_field='number_of_highlights_created',
											x_axis_label=_('Username'),
											y_axis_label=_('Number of highlights created'),
											title=_('The most active users creating highlights'),
											stat='identity',
											plot_name='most_active_users_creating_highlights')
		return (plot_users,)
