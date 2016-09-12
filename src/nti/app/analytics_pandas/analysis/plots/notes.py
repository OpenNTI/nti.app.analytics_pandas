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

from .commons import bar_plot_with_fill
from .commons import generate_three_plots
from .commons import group_line_plot_x_axis_date
from .commons import generate_three_group_by_plots
from .commons import histogram_plot_x_axis_discrete

class NotesEventsTimeseriesPlot(object):

	def __init__(self, net):
		"""
		net = NotesEventsTimeseries
		"""
		self.net = net
		self.period = net.period

	def explore_all_events(self, period_breaks='1 week', minor_period_breaks='1 day',
							theme_seaborn_=True):
		net = self.net
		df = net.combine_all_events()
		if len(df.index) <= 0:
			return ()

		group_by = 'event_type'
		event_title = _('Number of notes events grouped by event type during period of time')
		user_title = _('Number of unique users creating notes events during period of time')
		ratio_title = _('Ratio of notes events over unique user on each available date')
		event_type = 'note_events'
		event_y_axis_field = 'total_events'
		event_y_axis_label = _('Number of notes events')
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

class NotesCreationTimeseriesPlot(object):

	def __init__(self, nct):
		"""
		nct = NotesCreationTimeseries
		"""
		self.nct = nct
		self.period = nct.period

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day',
						theme_seaborn_=True):
		nct = self.nct
		df = nct.analyze_events()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of notes created')
		user_title = _('Number of unique users creating notes')
		ratio_title = _('Ratio of notes created over unique user')
		event_type = 'notes_created'
		plots = self.generate_plots(df,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_,
									event_type)
		return (plots)

	def analyze_events_per_course_sections(self, period_breaks='1 week',
										   minor_period_breaks='1 day',
										   theme_seaborn_=True):
		nct = self.nct
		df = nct.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = {}
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of notes created per course sections')
			user_title = _('Number of unique users creating notes per course sections')
			ratio_title = _('Ratio of notes created over unique user per course sections')
			event_type = 'notes_created_per_course_sections'
			all_section_plots = self.generate_group_by_plot(df,
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
			event_title = translate(_("Number of notes created in ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users creating notes in ${title}",
									  mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of notes created over unique user in ${title}",
									  mapping={'title': context_name}))
			event_type = 'notes_created_in_%s' % (context_name.replace(' ', '_'))
			section_plots = self.generate_plots(new_df,
												event_title,
												user_title,
												ratio_title,
												period_breaks,
												minor_period_breaks,
												theme_seaborn_,
												event_type)
			key = 'section_plots_%s' % course_id
			section_plots_dict[key] = section_plots
		plots['section_plots'] = section_plots_dict
		return plots

	def generate_plots(self, df, event_title, user_title, ratio_title,
					   period_breaks, minor_period_breaks, theme_seaborn_,
					   event_type=None):

		event_y_axis_field = 'number_of_notes_created'
		event_y_axis_label = _('Number of notes created')
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

	def analyze_device_types(self, period_breaks='1 week', minor_period_breaks='1 day',
							theme_seaborn_=True):

		nct = self.nct
		dataframe = nct.dataframe
		df = nct.analyze_device_types(dataframe)

		group_by = 'device_type'
		event_title = _('Number of notes created grouped by device types')
		user_title = _('Number of unique users creating notes grouped by device types')
		ratio_title = _('Ratio of notes created grouped by device types over unique user')
		event_type = 'notes_created_per_device_types'
		device_plots = self.generate_group_by_plot(df,
												   group_by,
												   event_title,
												   user_title,
												   ratio_title,
												   period_breaks,
												   minor_period_breaks,
												   theme_seaborn_,
												   event_type)
		return device_plots

	def analyze_enrollment_types(self, period_breaks='1 week', minor_period_breaks='1 day',
							theme_seaborn_=True):

		nct = self.nct
		dataframe = nct.dataframe
		df = nct.analyze_enrollment_types(dataframe)

		group_by = 'enrollment_type'
		event_title = _('Number of notes created grouped by enrollment types')
		user_title = _('Number of unique users creating notes grouped by enrollment types')
		ratio_title = _('Ratio of notes created grouped by enrollment types over unique user')
		event_type = 'notes_created_per_enrollment_types'
		enrollment_plots = self.generate_group_by_plot(
												df,
												group_by,
												event_title,
												user_title,
												ratio_title,
												period_breaks,
												minor_period_breaks,
												theme_seaborn_,
												event_type)
		return enrollment_plots

	def analyze_resource_types(self, period_breaks='1 week',
							   minor_period_breaks='1 day',
							   theme_seaborn_=True):
		nct = self.nct
		df = nct.analyze_resource_types()

		event_title = _('Number of notes created grouped by resource types')
		user_title = _('Number of unique users creating notes grouped by resource types')
		ratio_title = _('Ratio of notes created grouped by resource types over unique user')
		group_by = 'resource_type'
		event_type = 'notes_created_per_resource_types'
		resource_plots = self.generate_group_by_plot(df,
													 group_by,
													 event_title,
													 user_title,
													 ratio_title,
													 period_breaks,
													 minor_period_breaks,
													 theme_seaborn_,
													 event_type)

		return resource_plots

	def plot_the_most_active_users(self, max_rank_number=10):
		nct = self.nct
		users_df = nct.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()
		event_type = 'most_active_users_creating_notes'
		plot_users = histogram_plot_x_axis_discrete(
								df=users_df,
								x_axis_field='username' ,
								y_axis_field='number_of_notes_created',
								x_axis_label=_('Username'),
								y_axis_label=_('Number of notes created'),
								title=_('The most active users creating notes'),
								stat='identity',
								plot_name=event_type)
		return (plot_users,)

	def analyze_sharing_types(self, period_breaks='1 week',
							  minor_period_breaks='1 day',
							  theme_seaborn_=True):
		nct = self.nct
		dataframe = nct.dataframe
		df = nct.analyze_sharing_types(dataframe)

		event_title = _('Number of notes created grouped by sharing types')
		user_title = _('Number of unique users creating notes grouped by sharing types')
		ratio_title = _('Ratio of notes created grouped by sharing types over unique user')
		event_type = 'notes_created_per_sharing_types'
		group_by = 'sharing'
		sharing_plots = self.generate_group_by_plot(df,
													group_by,
													event_title,
													user_title,
													ratio_title,
													period_breaks,
													minor_period_breaks,
													theme_seaborn_,
													event_type)

		return sharing_plots

	def generate_group_by_plot(self, df, group_by, event_title, user_title, ratio_title,
							   period_breaks, minor_period_breaks, theme_seaborn_,
							   event_type=None):
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_y_axis_field = 'number_of_notes_created'
		event_y_axis_label = _('Number of notes created')

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

	def analyze_notes_created_on_videos(self, period_breaks='1 week',
										minor_period_breaks='1 day',
										theme_seaborn_=True):

		nct = self.nct
		df = nct.analyze_notes_created_on_videos()
		if df is None:
			return ()
		(sharing_df, device_df) = df

		plots = {}
		# generate sharing types plots
		group_by = 'sharing'
		event_title = _('Number of notes created on videos grouped by sharing types')
		user_title = _('Number of unique users creating notes on videos grouped by sharing types')
		ratio_title = _('Ratio of notes created on videos grouped by sharing types over unique user')
		event_type = 'notes_created_on_videos_per_sharing_types'
		sharing_plots = self.generate_group_by_plot(sharing_df,
													group_by,
													event_title,
													user_title,
													ratio_title,
													period_breaks,
													minor_period_breaks,
													theme_seaborn_,
													event_type)
		plots['sharing'] = sharing_plots
		# generate device types plots
		group_by = 'device_type'
		event_title = _('Number of notes created on videos grouped by device types')
		user_title = _('Number of unique users creating notes on videos grouped by device types')
		ratio_title = _('Ratio of notes created on videos grouped by device types over unique user')
		event_type = 'notes_created_on_video_per_device_types'
		device_plots = self.generate_group_by_plot(device_df,
												   group_by,
												   event_title,
												   user_title,
												   ratio_title,
												   period_breaks,
												   minor_period_breaks,
												   theme_seaborn_,
												   event_type)
		plots['user_agent'] = device_plots
		return plots

class NotesViewTimeseriesPlot(object):

	def __init__(self, nvt):
		"""
		nvt = NotesViewTimeseries
		"""
		self.nvt = nvt
		self.period = nvt.period

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day',
						theme_seaborn_=True):
		nvt = self.nvt
		df = nvt.analyze_total_events()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_type = 'note_views'
		event_title = _('Number of notes viewed during period of time')
		user_title = _('Number of unique users viewing notes during period of time')
		ratio_title = _('Ratio of notes viewed over unique user on each available date')

		plots = self.generate_plots(
							df,
							event_title,
							user_title,
							ratio_title,
							period_breaks,
							minor_period_breaks,
							theme_seaborn_,
							event_type)
		return (plots)

	def analyze_total_events_per_course_sections(self, period_breaks='1 week',
												 minor_period_breaks='1 day',
												 theme_seaborn_=True):
		nvt = self.nvt
		df = nvt.analyze_total_events_per_course_sections()
		if df is None:
			return()

		plots = {}
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of notes viewed per course sections')
			user_title = _('Number of unique users viewing notes per course sections')
			ratio_title = _('Ratio of notes viewed over unique user per course sections')
			event_type = 'note_views_per_course_sections'
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
			event_title = translate(_("Number of notes viewed in ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users viewing notes in ${title}",
									  mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of notes viewed over unique user in ${title}",
									  mapping={'title': context_name}))
			event_type = 'note_views_in_%s' % (context_name.replace(' ', '_'))
			section_plots = self.generate_plots(new_df,
												event_title,
												user_title,
												ratio_title,
												period_breaks,
												minor_period_breaks,
												theme_seaborn_,
												event_type)
			key = 'section_plots_%s' % course_id
			section_plots_dict[key] = section_plots
		plots['section_plots'] = section_plots_dict
		return plots

	def generate_plots(self, df, event_title, user_title,
					   ratio_title, period_breaks, minor_period_breaks,
					   theme_seaborn_, event_type):
		event_y_axis_field = 'number_of_note_views'
		event_y_axis_label = _('Number of note views')
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

	def generate_group_by_plots(self, df, group_by, event_title, user_title, ratio_title,
							   period_breaks, minor_period_breaks,
							   theme_seaborn_, event_type):
		event_y_axis_field = 'number_of_note_views'
		event_y_axis_label = _('Number of note views')
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

	def analyze_total_events_based_on_sharing_type(self, period_breaks='1 week',
												   minor_period_breaks='1 day',
												   theme_seaborn_=True):
		nvt = self.nvt
		df = nvt.analyze_total_events_based_on_sharing_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'sharing'
		event_title = _('Number of notes viewed grouped by sharing types')
		user_title = _('Number of unique users viewing notes grouped by sharing types')
		ratio_title = _('Ratio of notes viewed grouped by sharing types over unique user')
		event_type = 'note_views_per_sharing_types'
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

	def plot_the_most_active_users(self, max_rank_number=10):
		nvt = self.nvt
		users_df = nvt.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(df=users_df,
													x_axis_field='username' ,
													y_axis_field='number_of_note_views',
													x_axis_label=_('Username'),
													y_axis_label=_('Number of notes viewed'),
													title=_('The most active users viewing notes'),
													stat='identity',
													plot_name='most_active_user_viewing_notes')
		return (plot_users,)

	def analyze_total_events_based_on_device_type(self, period_breaks='1 week',
												  minor_period_breaks='1 day',
												  theme_seaborn_=True):
		nvt = self.nvt
		df = nvt.analyze_total_events_based_on_device_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of note views grouped by device types')
		user_title = _('Number of unique users viewing notes grouped by device types')
		ratio_title = _('Ratio of note views grouped by device types over unique user')
		event_type = 'note_views_per_device_types'
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

	def analyze_total_events_based_on_enrollment_type(self, period_breaks='1 week',
												  minor_period_breaks='1 day',
												  theme_seaborn_=True):
		nvt = self.nvt
		df = nvt.analyze_total_events_based_on_enrollment_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'enrollment_type'
		event_title = _('Number of note views grouped by enrollment types')
		user_title = _('Number of unique users viewing notes grouped by enrollment types')
		ratio_title = _('Ratio of note views grouped by enrollment types over unique user')
		event_type = 'note_views_per_enrollment_types'
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

	def analyze_total_events_based_on_resource_type(self, period_breaks='1 week',
													minor_period_breaks='1 day',
													theme_seaborn_=True):
		nvt = self.nvt
		df = nvt.analyze_total_events_based_on_resource_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'resource_type'
		event_title = _('Number of notes viewed grouped by resource types')
		user_title = _('Number of unique users viewing notes grouped by resource types')
		ratio_title = _('Ratio of notes viewed grouped by resource types over unique user')
		event_type = 'note_views_per_resource_types'
		plots = self.generate_group_by_plots(df,
											 group_by,
											 event_title,
											 user_title,
											 ratio_title,
											 period_breaks,
											 minor_period_breaks,
											 theme_seaborn_,
											 event_type)
		return (plots)

	def analyze_unique_events_based_on_sharing_type(self, period_breaks='1 week',
													minor_period_breaks='1 day',
													theme_seaborn_=True):
		nvt = self.nvt
		df = nvt.analyze_unique_events_based_on_sharing_type()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		title = _('Number of notes viewed grouped by sharing types during period of time')
		plot_unique_notes_viewed = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_unique_notes_viewed',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of notes viewed'),
										title=title,
										period_breaks=period_breaks,
										group_by='sharing',
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_,
										plot_name='unique_note_views_per_sharing_types')
		return (plot_unique_notes_viewed,)

	def plot_the_most_viewed_notes_and_its_author(self):
		nvt = self.nvt
		df = nvt.get_the_most_viewed_notes_and_its_author()
		if df is None:
			return ()
		df['note_id'] = df['note_id'].astype('category')
		plot_authors = bar_plot_with_fill(df=df,
										  x_axis_field='author_name' ,
										  y_axis_field='number_of_views',
										  x_axis_label=_("Author's name"),
										  y_axis_label=_('Number of notes viewed'),
										  title=_('The authors of most viewed notes'),
										  stat='bar',
										  fill='note_id',
										  plot_name='most_viewed_notes_author')
		return (plot_authors,)

class NoteLikesTimeseriesPlot(object):

	def __init__(self, nlt):
		"""
		nlt = NoteLikesTimeseries
		"""
		self.nlt = nlt
		self.period = nlt.period

	def explore_events(self, period_breaks='1 week',
					   minor_period_breaks='1 day',
					   theme_seaborn_=True):

		nlt = self.nlt
		df = nlt.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of note likes during period of time')
		user_title = _('Number of unique users liking notes during period of time')
		ratio_title = _('Ratio of note likes over unique user on each available date')
		event_type = 'note_likes'
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
		nlt = self.nlt
		df = nlt.analyze_events_per_course_sections()
		if df is None:
			return()

		plots = []
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of note likes per course sections')
			user_title = _('Number of unique users liking notes per course sections')
			ratio_title = _('Ratio of note likes over unique user per course sections')
			event_type = 'note_likes_per_course_sections'
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks,
															 theme_seaborn_,
															 event_type)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = translate(_("Number of notes likes in ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users liking notes in ${title}",
									  mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of notes likes over unique user in ${title}",
									  mapping={'title': context_name}))

			event_type = 'note_likes_in_%s' % (context_name)
			section_plots = self.generate_plots(new_df,
												event_title,
												user_title,
												ratio_title,
												period_breaks,
												minor_period_breaks,
												theme_seaborn_)
			plots.append(section_plots)
		return plots

	def analyze_events_per_device_types(self, period_breaks='1 week',
										minor_period_breaks='1 day',
										theme_seaborn_=True):

		nlt = self.nlt
		df = nlt.analyze_events_per_device_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'device_type'
		event_title = _('Number of note likes grouped by device types')
		user_title = _('Number of unique users liking notes grouped by device types')
		ratio_title = _('Ratio of note likes over unique user grouped by device types')
		event_type = 'note_likes_per_device_types'
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

	def analyze_events_per_enrollment_types(self, period_breaks='1 week',
										minor_period_breaks='1 day',
										theme_seaborn_=True):

		nlt = self.nlt
		df = nlt.analyze_events_per_enrollment_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'enrollment_type'
		event_title = _('Number of note likes grouped by enrollment types')
		user_title = _('Number of unique users liking notes grouped by enrollment types')
		ratio_title = _('Ratio of note likes over unique user grouped by enrollment types')
		event_type = 'note_likes_per_enrollment_types'
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

	def analyze_events_per_resource_types(self, period_breaks='1 week',
										  minor_period_breaks='1 day',
										  theme_seaborn_=True):

		nlt = self.nlt
		df = nlt.analyze_events_per_resource_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'resource_type'
		event_title = _('Number of note likes grouped by resource types')
		user_title = _('Number of unique users liking notes grouped by resource types')
		ratio_title = _('Ratio of note likes over unique user grouped by resource types')
		event_type = 'note_likes_per_resource_types'
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

	def generate_plots(self, df, event_title, user_title, ratio_title, period_breaks,
					   minor_period_breaks, theme_seaborn_, event_type=None):
		event_y_axis_field = 'number_of_note_likes'
		event_y_axis_label = _('Number of note likes')
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

	def generate_group_by_plots(self, df, group_by, event_title, user_title, ratio_title,
								period_breaks, minor_period_breaks, theme_seaborn_,
								event_type=None):
		event_y_axis_field = 'number_of_note_likes'
		event_y_axis_label = _('Number of note likes')
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

class NoteFavoritesTimeseriesPlot(object):

	def __init__(self, nft):
		"""
		nft = NoteFavoritesTimeseries
		"""
		self.nft = nft
		self.period = nft.period

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day',
						theme_seaborn_=True):
		nft = self.nft
		df = nft.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of note favorites during period of time')
		user_title = _('Number of unique users voting notes as favorite during period of time')
		ratio_title = _('Ratio of note favorites over unique user on each available date')
		event_type = 'note_favorites'
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
		nft = self.nft
		df = nft.analyze_events_per_course_sections()
		if df is None:
			return()

		plots = []
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of note favorites per course sections')
			user_title = _('Number of unique users voting notes as favorites per course sections')
			ratio_title = _('Ratio of note favorites over unique user per course sections')
			event_type = 'note_favorites_per_course_sections'
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 event_title,
															 user_title,
															 ratio_title,
															 period_breaks,
															 minor_period_breaks,
															 theme_seaborn_,
															 event_type)
			plots.append(all_section_plots)

		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = translate(_("Number of note favorites in  ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users voting notes as favorites in ${title}",
									  mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of note favorites over unique user in ${title}",
									  mapping={'title': context_name}))
			event_type = 'note_favorites_in_%s' % (context_name)
			section_plots = self.generate_plots(new_df,
												event_title,
												user_title,
												ratio_title,
												period_breaks,
												minor_period_breaks,
												theme_seaborn_,
												event_type)
			plots.append(section_plots)

		return plots

	def analyze_events_per_device_types(self, period_breaks='1 week',
										minor_period_breaks='1 day',
										theme_seaborn_=True):
		nft = self.nft
		df = nft.analyze_events_per_device_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'device_type'
		event_title = _('Number of note favorites grouped by device types')
		user_title = _('Number of unique users voting notes as favorite grouped by device types')
		ratio_title = _('Ratio of note favorites over unique user grouped by device types')
		event_type = 'note_favorites_per_device_types'
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

	def analyze_events_per_enrollment_types(self, period_breaks='1 week',
										minor_period_breaks='1 day',
										theme_seaborn_=True):
		nft = self.nft
		df = nft.analyze_events_per_enrollment_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'enrollment_type'
		event_title = _('Number of note favorites grouped by enrollment types')
		user_title = _('Number of unique users voting notes as favorite grouped by enrollment types')
		ratio_title = _('Ratio of note favorites over unique user grouped by enrollment types')
		event_type = 'note_favorites_per_enrollment_types'
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


	def analyze_events_per_resource_types(self, period_breaks='1 week',
										  minor_period_breaks='1 day',
										  theme_seaborn_=True):
		nft = self.nft
		df = nft.analyze_events_per_resource_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'resource_type'
		event_title = _('Number of note favorites grouped by resource types')
		user_title = _('Number of unique users voting notes as favorite grouped by resource types')
		ratio_title = _('Ratio of note favorites over unique user grouped by resource types')
		event_type = 'note_favorites_per_resource_types'
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

	def generate_plots(self, df, event_title, user_title, ratio_title,
					   period_breaks, minor_period_breaks, theme_seaborn_,
					   event_type=None):
		event_y_axis_field = 'number_of_note_favorites'
		event_y_axis_label = _('Number of note favorites')
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

	def generate_group_by_plots(self, df, group_by, event_title, user_title, ratio_title,
								period_breaks, minor_period_breaks, theme_seaborn_,
								event_type=None):
		event_y_axis_field = 'number_of_note_favorites'
		event_y_axis_label = _('Number of note favorites')
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
