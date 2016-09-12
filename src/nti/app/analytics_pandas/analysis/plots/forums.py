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
from .commons import line_plot_x_axis_date
from .commons import group_line_plot_x_axis_date
from .commons import generate_three_group_by_plots
from .commons import histogram_plot_x_axis_discrete

class ForumsEventsTimeseriesPlot(object):

	def __init__(self, fet):
		"""
		fet = ForumsEventsTimeseries
		"""
		self.fet = fet
		self.period = fet.period

	def explore_all_events(self, period_breaks='1 week',
						   minor_period_breaks='1 day',
						   theme_seaborn_=True):

		fet = self.fet
		df = fet.combine_all_events_per_date()
		if len(df.index) <= 0:
			return ()

		group_by = 'event_type'
		event_title = _('Number of forums events grouped by event type during period of time')
		user_title = _('Number of unique users creating forums events during period of time')
		ratio_title = _('Ratio of forums events over unique user on each available date')
		event_type = 'forum_events'
		event_y_axis_field = 'total_events'
		event_y_axis_label = _('Number of forums events')
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

class ForumsCreatedTimeseriesPlot(object):

	def __init__(self, fct):
		"""
		fct = ForumsCreatedTimeseries
		"""
		self.fct = fct
		self.period = fct.period

	def explore_events(self, period_breaks='1 week',
					   minor_period_breaks='1 day',
					   theme_seaborn_=True):
		"""
		return scatter plots of forums creation during period of time
		it consists of:
			- number of forums creation
			- number of unique users
			- ratio of forums creation over unique users
		"""
		fct = self.fct
		df = fct.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of forums created during period of time')
		user_title = _('Number of unique users creating forums during period of time')
		ratio_title = _('Ratio of forums created over unique user on each available date')
		event_type = 'forums_created'
		event_y_axis_field = 'number_of_forums_created'
		event_y_axis_label = _('Number of forums created')
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

	def analyze_device_types(self, period_breaks='1 week',
							 minor_period_breaks='1 day',
							 theme_seaborn_=True):
		"""
		return scatter plots of forums creation grouped by device type during period of time
		it consists of:
			- number of forums creation
			- number of unique users
			- ratio of forums creation over unique users
		"""

		fct = self.fct
		df = fct.analyze_events_per_device_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		df['ratio'] = df['number_of_forums_created'] / df['number_of_unique_users']

		group_by = 'device_type'
		event_title = _('Number of forums created grouped by device types')
		user_title = _('Number of unique users creating forums grouped by device types')
		ratio_title = _('Ratio of forums created over unique user grouped by device types')
		event_type = 'forums_created_per_device_types'
		event_y_axis_field = 'number_of_forums_created'
		event_y_axis_label = _('Number of forums created per device type')

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

class ForumsCommentsCreatedTimeseriesPlot(object):

	def __init__(self, fcct):
		"""
		fcct = ForumsCommentsCreatedTimeseries
		"""
		self.fcct = fcct
		self.period = fcct.period

	def explore_events(self, period_breaks='1 week',
					   minor_period_breaks='1 day',
					   theme_seaborn_=True):
		"""
		return scatter plots of forum comments creation during period of time
		it consists of:
			- number of forums comment creation
			- number of unique users
			- ratio of forum comment creation over unique users
		"""
		fcct = self.fcct
		df = fcct.analyze_events()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		title_event = _('Number of forums comments created during period of time')
		title_users = _('Number of unique users creating forum comments during period of time')
		title_ratio = _('Ratio of forums comments created over unique user on each available date')
		title_avg_length = _('Average forums comments length on each available date')
		event_type = 'forum_comments_created'
		plots = self.generate_plots(df,
									period_breaks,
									minor_period_breaks,
									title_event,
									title_users,
									title_ratio,
									title_avg_length,
									theme_seaborn_,
									event_type)
		return plots

	def analyze_comments_per_section(self, period_breaks='1 week',
									 minor_period_breaks='1 day',
									 theme_seaborn_=True):
		"""
		return scatter plots of forum comments creation grouped by course section during period of time
		it consists of:
			- number of forums comment creation
			- number of unique users
			- ratio of forum comment creation over unique users
			- average comment length
		"""
		fcct = self.fcct
		df = fcct.analyze_comments_per_section()
		if df is None:
			return()

		plots = {}
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		if len(course_ids) > 1:
			title_event = _('Number of forum comments created')
			title_users = _('Number of unique users creating forum comments')
			title_ratio = _('Ratio of forums comments created over unique user')
			title_avg_length = _('Average forums comments length on each available date')
			group_by = 'context_name'
			event_type = 'forum_comments_created_per_course_sections'
			all_section_plots = self.generate_group_by_plots(df,
															 group_by,
															 period_breaks,
															 minor_period_breaks,
															 title_event,
															 title_users,
															 title_ratio,
															 title_avg_length,
															 theme_seaborn_,
															 event_type)
			plots['all_section_plots'] = all_section_plots

		section_plots_dict = {}
		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']

			title_event = translate(_("Number of forum comments created in ${title}",
									  mapping={'title': context_name}))

			title_users = translate(_("Number of unique users creating forum comments in ${title}",
									  mapping={'title': context_name}))

			title_ratio = translate(_("Ratio of forums comments created over unique user in ${title}",
									  mapping={'title': context_name}))

			title_avg_length = translate(_("Average forums comments length on each available date in ${title}",
									  	 mapping={'title': context_name}))

			event_type = 'forum_comments_created_in_%s' % (context_name.replace(' ', '_'))
			section_plots = self.generate_plots(new_df,
												period_breaks,
												minor_period_breaks,
												title_event,
												title_users,
												title_ratio,
												title_avg_length,
												theme_seaborn_,
												event_type)
			key = 'section_%s' % (course_id)
			section_plots_dict[key] = section_plots
		plots['section_plots'] = section_plots_dict

		return plots

	def generate_plots(self,
					   df,
					   period_breaks,
					   minor_period_breaks,
					   event_title,
					   user_title,
					   ratio_title,
					   title_avg_length,
					   theme_seaborn_,
					   event_type=None):
		event_y_axis_field = 'number_of_comment_created'
		event_y_axis_label = _('Number of forum comments created')
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

		avg_event_name = 'average_comment_%s' % event_type
		plot_average_comment_length = line_plot_x_axis_date(
				df=df,
				x_axis_field='timestamp_period',
				y_axis_field='average_comment_length',
				x_axis_label=_('Date'),
				y_axis_label=_('Average comments length'),
				title=title_avg_length,
				period_breaks=period_breaks,
				minor_breaks=minor_period_breaks,
				theme_seaborn_=theme_seaborn_,
				plot_name=avg_event_name,
				period=self.period)

		plots = plots + (plot_average_comment_length,)
		return plots

	def generate_group_by_plots(self,
								df,
								group_by,
								period_breaks,
								minor_period_breaks,
								event_title,
								user_title,
								ratio_title,
								title_avg_length,
								theme_seaborn_,
								event_type=None):
		event_y_axis_field = 'number_of_comment_created'
		event_y_axis_label = _('Number of forum comments created')
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

		avg_event_name = u'average_comment_%s' % event_type
		if 'device_type' in group_by:
			group_by = 'application_type'
			title_avg_length = title_avg_length.replace('device', 'application')
		plot_average_comment_length = group_line_plot_x_axis_date(
				df=df,
				x_axis_field='timestamp_period',
				y_axis_field='average_comment_length',
				x_axis_label=_('Date'),
				y_axis_label=_('Average comments length'),
				title=title_avg_length,
				period_breaks=period_breaks,
				group_by=group_by,
				minor_breaks=minor_period_breaks,
				theme_seaborn_=theme_seaborn_,
				plot_name=avg_event_name,
				period=self.period)

		plots = plots + (plot_average_comment_length,)
		return plots

	def analyze_device_types(self,
							 period_breaks='1 week',
							 minor_period_breaks='1 day',
							 theme_seaborn_=True):
		"""
		return scatter plots of forum comments creation grouped by device_type during
		period of time it consists of:
			- number of forums comment creation
			- number of unique users
			- ratio of forum comment creation over unique users
			- average comment length
		"""
		fcct = self.fcct
		df = fcct.analyze_device_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		title_event = _('Number of forum comments created grouped by device types')
		title_users = _('Number of unique users creating forum comments grouped by device types')
		title_ratio = _('Ratio of forums comments created over unique user on each available date')
		title_avg_length = _('Average forums comments length on each available date')
		event_type = 'forum_comments_created_per_device_types'
		plots = self.generate_group_by_plots(df,
											 group_by,
											 period_breaks,
											 minor_period_breaks,
											 title_event,
											 title_users,
											 title_ratio,
											 title_avg_length,
											 theme_seaborn_,
											 event_type)
		return plots

	def analyze_enrollment_types(self,
							 	 period_breaks='1 week',
							 	 minor_period_breaks='1 day',
							 	 theme_seaborn_=True):
		"""
		return plots of forum comments creation grouped by enrollment_type during period of time
		it consists of:
			- number of forums comment creation
			- number of unique users
			- ratio of forum comment creation over unique users
			- average comment length
		"""
		fcct = self.fcct
		df = fcct.analyze_enrollment_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'enrollment_type'
		title_event = _('Number of forum comments created grouped by enrollment types')
		title_users = _('Number of unique users creating forum comments grouped by enrollment types')
		title_ratio = _('Ratio of forums comments created over unique user on each available date')
		title_avg_length = _('Average forums comments length on each available date')
		event_type = 'forum_comments_created_per_enrollment_types'
		plots = self.generate_group_by_plots(df,
											 group_by,
											 period_breaks,
											 minor_period_breaks,
											 title_event,
											 title_users,
											 title_ratio,
											 title_avg_length,
											 theme_seaborn_,
											 event_type)
		return plots

	def plot_the_most_active_users(self, max_rank_number=10):
		fcct = self.fcct
		users_df = fcct.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(
						df=users_df,
						x_axis_field='username' ,
						y_axis_field='number_of_comments_created',
						x_axis_label=_('Username'),
						y_axis_label=_('Number of comments'),
						title=_('The most active users by forum comment count'),
						stat='identity',
						plot_name='most_active_users_creating_forum_comments')
		return (plot_users,)

class ForumCommentLikesTimeseriesPlot(object):

	def __init__(self, fclt):
		"""
		fclt = ForumCommentLikesTimeseries
		"""
		self.fclt = fclt
		self.period = fclt.period

	def analyze_events(self, period_breaks='1 week', minor_period_breaks='1 day',
						theme_seaborn_=True):
		"""
		return plots of forum comment likes during period of time
		it consists of:
			- number of forums comment likes
			- number of unique users
			- ratio of forum comment likes over unique users
		"""
		fclt = self.fclt
		df = fclt.analyze_events()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of forums comment likes during period of time')
		user_title = _('Number of unique users liking forum comments during period of time')
		ratio_title = _('Ratio of forum comments liked over unique user on each available date')
		event_type = 'forum_comment_likes'
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
		fclt = self.fclt
		df = fclt.analyze_events_per_course_sections()
		if df is None:
			return()

		plots = {}
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of forum comment likes per course sections')
			user_title = _('Number of unique users liking forum comments per course sections')
			ratio_title = _('Ratio of forum comment likes over unique user per course sections')
			event_type = 'forum_comment_likes_per_course_sections'
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
			event_title = 'Number of forum comment likes in %s' % (context_name)
			user_title = 'Number of unique users liking forum comments in %s' % (context_name)
			ratio_title = 'Ratio of forum comments likes over unique user in %s' % (context_name)
			event_type = 'forum_comment_likes_in_%s' % (context_name.replace(' ', '_'))
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
		"""
		plot the number of comments liked on each available date during time period.
		It also shows the number of unique users liking comments
		"""
		fclt = self.fclt
		df = fclt.analyze_device_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of forum comments likes grouped by device types')
		user_title = _('Number of unique users liking forum comments grouped by device types')
		ratio_title = _('Ratio of forum comments liked over unique user grouped by device types')
		event_type = 'forum_comment_likes_per_device_types'
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
		"""
		plot the number of comments liked per enrollment types on each available date during time period.
		It also shows the number of unique users liking comments
		"""
		fclt = self.fclt
		df = fclt.analyze_enrollment_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'enrollment_type'
		event_title = _('Number of forum comments likes grouped by enrollment types')
		user_title = _('Number of unique users liking forum comments grouped by enrollment types')
		ratio_title = _('Ratio of forum comments liked over unique user grouped by enrollment types')
		event_type = 'forum_comment_likes_per_enrollment_types'
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

		event_y_axis_field = 'number_of_likes'
		event_y_axis_label = _('Number of forum comment likes')
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
		event_y_axis_field = 'number_of_likes'
		event_y_axis_label = _('Number of forum comment likes')
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

class ForumCommentFavoritesTimeseriesPlot(object):

	def __init__(self, fcft):
		"""
		fcft = ForumCommentFavoritesTimeseries
		"""
		self.fcft = fcft
		self.period = fcft.period

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day',
						theme_seaborn_=True):
		"""
		return plots of forum comment favorites during period of time
		it consists of:
			- number of forums comment favorites
			- number of unique users
			- ratio of forum comment favorites over unique users
		"""
		fcft = self.fcft
		df = fcft.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of forum comment favorites during time period')
		user_title = _('Number of unique users voting forum comments as favorites during time period')
		ratio_title = _('Ratio of forum comment favorites over unique users during time period')
		event_type = 'forum_comment_favorites'
		plots = self.generate_plots(df,
									event_title,
									user_title,
									ratio_title,
									period_breaks,
									minor_period_breaks,
									theme_seaborn_,
									event_type)
		return plots

	def analyze_events_per_course_sections(self,
										   period_breaks='1 week',
										   minor_period_breaks='1 day',
										   theme_seaborn_=True):
		fcft = self.fcft
		df = fcft.analyze_events_per_course_sections()
		if df is None:
			return()

		plots = {}
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of forum comment favorites per course sections')
			user_title = _('Number of unique users voting forum comments as favorites per course sections')
			ratio_title = _('Ratio of forum comment favorites over unique user per course sections')
			event_type = 'forum_comment_favorites_per_course_sections'
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
			event_title = translate(_("Number of forum comments favorites in ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users voting forum comments as favorites in ${title}",
									 mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of forums comments favorites over unique user in ${title}",
									  mapping={'title': context_name}))

			event_type = 'forum_comment_favorites_in_%s' % (context_name.replace(' ', '_'))
			section_plots = self.generate_plots(new_df,
												event_title,
												user_title,
												ratio_title,
												period_breaks,
												minor_period_breaks,
												theme_seaborn_)
			key = 'section_%s' % (course_id)
			section_plots_dict[key] = section_plots
		plots['section_plots'] = section_plots_dict
		return plots

	def analyze_device_types(self, period_breaks='1 week',
							 minor_period_breaks='1 day',
							 theme_seaborn_=True):
		"""
		plot the number of comment favorites on each available date during time period.
		It also shows the number of unique users adding favorites
		"""
		fcft = self.fcft
		df = fcft.analyze_device_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of forum comment favorites grouped by device types')
		user_title = _('Number of unique users voting forum comments as favorites grouped by device types')
		ratio_title = _('Ratio of forum comment favorites over unique users grouped by device types')
		event_type = 'forum_comment_favorites_per_device_types'
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
		"""
		plot the number of comment favorites per enrollment types on each available date during time period.
		It also shows the number of unique users adding favorites
		"""
		fcft = self.fcft
		df = fcft.analyze_enrollment_types()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'enrollment_type'
		event_title = _('Number of forum comment favorites grouped by enrollment types')
		user_title = _('Number of unique users voting forum comments as favorites grouped by enrollment types')
		ratio_title = _('Ratio of forum comment favorites over unique users grouped by enrollment types')
		event_type = 'forum_comment_favorites_per_enrollment_types'
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
		event_y_axis_field = 'number_of_favorites'
		event_y_axis_label = _('Number of forum comment favorites')
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
		event_y_axis_field = 'number_of_favorites'
		event_y_axis_label = _('Number of forum comment favorites')
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
