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

class VideoEventsTimeseriesPlot(object):

	def __init__(self, vet):
		"""
		vet = VideoEventsTimeseries
		"""
		self.vet = vet
		self.period = vet.period

	def explore_events(self, period_breaks='1 day', minor_period_breaks=None,
					   theme_seaborn_=True, video_event_type='watch'):
		"""
		return plots of video events during period of time
		it consists of:
			- number of video events
			- number of unique users
			- ratio of video events over unique users
		"""
		vet = self.vet
		df = vet.analyze_video_events(video_event_type=video_event_type.upper())
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		if video_event_type == 'skip':
			video_event_type = 'skipp'

		event_title = translate(_("Number of videos ${event}ed during period of time",
								  mapping={'event': video_event_type}))

		user_title = translate(_("Number of unique users ${event}ing videos during period of time",
								  mapping={'event': video_event_type}))

		ratio_title = translate(_("Ratio of videos ${event}ed over unique user on each available date",
								  mapping={'event': video_event_type}))
		event_type = 'video_events'
		plots = self.generate_plots(
							df,
							event_title,
							user_title,
							ratio_title,
							period_breaks,
							minor_period_breaks,
							theme_seaborn_,
							event_type)
		return plots

	def generate_plots(self, df, event_title, user_title, ratio_title,
					   period_breaks, minor_period_breaks, theme_seaborn_,
					   event_type=None):
		event_y_axis_field = 'number_of_video_events'
		event_y_axis_label = _('Number of videos events')
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
		event_y_axis_field = 'number_of_video_events'
		event_y_axis_label = _('Number of videos events')
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

	def analyze_video_events_device_types(self, period_breaks='1 week',
										  minor_period_breaks='1 day',
										  video_event_type='WATCH',
										  theme_seaborn_=True):
		"""
		given a video event type (WATCH or SKIP) return plots of video events during period of time
		it consists of:
			- number of video events
			- number of unique users
			- ratio of video events over unique users
		grouped by device types
		"""
		vet = self.vet
		df = vet.analyze_video_events_device_types(video_event_type.upper())
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of video events grouped by device types')
		user_title = _('Number of unique users creating video events grouped by device types')
		ratio_title = _('Ratio of video events over unique users grouped by device types')
		event_type = 'video_events_%s' % (video_event_type.lower())
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

	def analyze_video_events_enrollment_types(self, period_breaks='1 week',
										 	  minor_period_breaks='1 day',
										  	  video_event_type='WATCH',
										  	  theme_seaborn_=True):
		"""
		given a video event type (WATCH or SKIP) return plots of video events during period of time
		it consists of:
			- number of video events
			- number of unique users
			- ratio of video events over unique users
		grouped by enrollment types
		"""
		vet = self.vet
		df = vet.analyze_video_events_enrollment_types(video_event_type.upper())
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'enrollment_type'
		event_title = _('Number of video events grouped by enrollment types')
		user_title = _('Number of unique users creating video events grouped by enrollment types')
		ratio_title = _('Ratio of video events over unique users grouped by enrollment types')
		event_type = 'video_events_%s' % (video_event_type.lower())
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

	def analyze_video_events_types(self, period_breaks='1 week',
								   minor_period_breaks='1 day',
								   theme_seaborn_=True):
		"""
		plot video events by video_event_type
		"""
		vet = self.vet
		df = vet.analyze_video_events_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'video_event_type'
		event_title = _('Number of video events grouped by event types')
		user_title = _('Number of unique users creating video events grouped by event types')
		ratio_title = _('Ratio of video events over unique users grouped by event types')
		event_type = 'video_events_per_types'
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

	def analyze_video_events_per_course_sections(self,
												 period_breaks='1 week',
												 minor_period_breaks='1 day',
												 video_event_type='WATCH',
												 theme_seaborn_=True):
		vet = self.vet
		df = vet.analyze_video_events_per_course_sections(video_event_type.upper())
		if df is None:
			return()

		plots = {}
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = translate(_("Number of video events (${event}) per course sections",
							 		mapping={'event': video_event_type}))

			user_title = translate(_("Number of unique users per course sections (VIDEO ${event})",
							 	   mapping={'event': video_event_type}))

			ratio_title = translate(_("Ratio of video events over unique user per course sections (VIDEO ${event})",
							  		mapping={'event': video_event_type}))
			event_type = 'video_events_per_course_sections_%s' % (video_event_type)
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
			event_title = translate(_("Number of video events (${event}) in ${context}",
								 	   mapping={'event': video_event_type,
												'context':context_name}))

			user_title = translate(_("Number of unique users on video events (${event}) in ${context}",
								 	  mapping={'event': video_event_type,
											   'context':context_name}))

			ratio_title = translate(_("Ratio of video events (${event}) over unique user in ${context}",
								  	mapping={'event': video_event_type, 'context':context_name}))
			event_type = 'video_events_%s_in_%s' % (video_event_type, context_name.replace(' ', '_'))
			section_plots = self.generate_plots(
											new_df,
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
