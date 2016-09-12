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

class TopicsEventsTimeseriesPlot(object):

	def __init__(self, tet):
		"""
		tet = TopicsEventsTimeseries
		"""
		self.tet = tet
		self.period = tet.period

	def explore_all_events(self, period_breaks='1 week', minor_period_breaks='1 day',
						   theme_seaborn_=True):
		tet = self.tet
		df = tet.combine_all_events_per_date()
		if len(df.index) <= 0:
			return ()

		group_by = 'event_type'
		event_title = _('Number of topics events grouped by event type during period of time')
		user_title = _('Number of unique users creating topics events during period of time')
		ratio_title = _('Ratio of topics events over unique user on each available date')
		event_type = 'forum_comment_favorites_per_device_types'
		event_y_axis_field = 'total_events'
		event_y_axis_label = _('Number of topics events')
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

class TopicsCreationTimeseriesPlot(object):

	def __init__(self, tct):
		"""
		tct = TopicsCreationTimeseries
		"""
		self.tct = tct
		self.period = tct.period

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day',
					   theme_seaborn_=True):
		"""
		return plots of topics created during period of time
		it consists of:
			- number of topics created
			- number of unique users
			- ratio of topics created over unique users
		"""
		tct = self.tct
		df = tct.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of topics created during period of time')
		user_title = _('Number of unique users creating topics during period of time')
		ratio_title = _('Ratio of topics created over unique user on each available date')
		event_type = 'topics_created'
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
		tct = self.tct
		df = tct.analyze_events_per_course_sections()
		if df is None:
			return ()

		plots = {}
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of topics created per course sections')
			user_title = _('Number of unique users creating topics per course sections')
			ratio_title = _('Ratio of topics created over unique user per course sections')
			event_type = 'topics_created_per_course_sections'
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
			event_title = 'Number of topics created in %s' % (context_name)
			user_title = 'Number of unique users creating topics in %s' % (context_name)
			ratio_title = 'Ratio of topics created over unique user in %s' % (context_name)
			event_type = 'topics_created_in_%s' % (context_name.replace(' ', '_'))
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

	def analyze_events_per_device_types(self, period_breaks='1 week',
										minor_period_breaks='1 day',
										theme_seaborn_=True):
		tct = self.tct
		df = tct.analyze_events_per_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'device_type'
		event_title = _('Number of topics created per device types')
		user_title = _('Number of unique users creating topics per device types')
		ratio_title = _('Ratio of topics created over unique user per device types')
		event_type = 'topics_created_per_device_types'
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

	def analyze_events_per_enrollment_types(self, period_breaks='1 week',
											minor_period_breaks='1 day',
											theme_seaborn_=True):
		tct = self.tct
		df = tct.analyze_events_per_enrollment_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		group_by = 'enrollment_type'
		event_title = _('Number of topics created per enrollment types')
		user_title = _('Number of unique users creating topics per enrollment types')
		ratio_title = _('Ratio of topics created over unique user per enrollment types')
		event_type = 'topics_created_per_enrollment_types'
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
		event_y_axis_field = 'number_of_topics_created'
		event_y_axis_label = _('Number of topics created')
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
		event_y_axis_field = 'number_of_topics_created'
		event_y_axis_label = _('Number of topics created')
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

class TopicViewsTimeseriesPlot(object):

	def __init__(self, tvt):
		"""
		tvt = TopicViewsTimeseries
		"""
		self.tvt = tvt
		self.period = tvt.period

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day',
					   theme_seaborn_=True):
		"""
		return plots of topics viewed during period of time
		it consists of:
			- number of topics viewed
			- number of unique users
			- ratio of topics viewed over unique users
		"""
		tvt = self.tvt
		df = tvt.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of topics viewed during period of time')
		user_title = _('Number of unique users viewing topics during period of time')
		ratio_title = _('Ratio of topics viewed over unique user on each available date')
		event_type = 'topic_views'
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

		tvt = self.tvt
		df = tvt.analyze_events_per_course_sections()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())
		plots = {}
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of topics viewed per course sections')
			user_title = _('Number of unique users viewing topics per course sections')
			ratio_title = _('Ratio of topics viewed over unique user per course sections')
			event_type = 'topic_views_per_course_sections'
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
			event_title = translate(_("Number of topics viewed in ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users viewing topics in ${title}",
									  mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of topics viewed over unique user in ${title}",
									  mapping={'title': context_name}))

			event_type = 'topic_views_in_%s' % (context_name.replace(' ', '_'))
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

	def analyze_device_types(self, period_breaks='1 day', minor_period_breaks=None,
							 theme_seaborn_=True):
		"""
		return plots of topics viewed grouped by device type during period of time
		it consists of:
			- number of topics viewed
			- number of unique users
			- ratio of topics viewed over unique users
		"""
		tvt = self.tvt
		df = tvt.analyze_device_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of topics viewed grouped by device types')
		user_title = _('Number of unique users viewing topics grouped by device types')
		ratio_title = _('Ratio of topics viewed over unique user grouped by device types')
		event_type = 'topic_views_per_device_types'
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

	def analyze_enrollment_types(self, period_breaks='1 day', minor_period_breaks=None,
							theme_seaborn_=True):
		"""
		return plots of topics viewed grouped by enrollment type during period of time
		it consists of:
			- number of topics viewed
			- number of unique users
			- ratio of topics viewed over unique users
		"""
		tvt = self.tvt
		df = tvt.analyze_enrollment_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'enrollment_type'
		event_title = _('Number of topics viewed grouped by enrollment types')
		user_title = _('Number of unique users viewing topics grouped by enrollment types')
		ratio_title = _('Ratio of topics viewed over unique user grouped by enrollment types')
		event_type = 'topic_views_per_enrollment_types'
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
		event_y_axis_field = 'number_of_topics_viewed'
		event_y_axis_label = _('Number of topics viewed')
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
		event_y_axis_field = 'number_of_topics_viewed'
		event_y_axis_label = _('Number of topics viewed')
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

	def plot_the_most_active_users(self, max_rank_number=10):

		tvt = self.tvt
		users_df = tvt.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(
									df=users_df,
									x_axis_field='username' ,
									y_axis_field='number_of_topics_viewed',
									x_axis_label=_('Username'),
									y_axis_label=_('Number of topics viewed'),
									title=_('The most active users viewing topics'),
									stat='identity',
									plot_name='most_active_users_viewing_topics')

		return (plot_users,)

class TopicLikesTimeseriesPlot(object):

	def __init__(self, tlt):
		"""
		tlt = TopicLikesTimeseries
		"""
		self.tlt = tlt
		self.period = tlt.period

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day',
					   theme_seaborn_=True):
		"""
		return plots of topic likes during period of time
		it consists of:
			- number of topic likes
			- number of unique users
			- ratio of topic likes over unique users
		"""
		tlt = self.tlt
		df = tlt.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of topic likes during period of time')
		user_title = _('Number of unique users liking topics during period of time')
		ratio_title = _('Ratio of topic likes over unique user on each available date')
		event_type = 'topic_likes'
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
		tlt = self.tlt
		df = tlt.analyze_events_per_course_sections()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())
		plots = []
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of topic likes per course sections')
			user_title = _('Number of unique users liking topics per course sections')
			ratio_title = _('Ratio of topic likes over unique user per course sections')
			event_type = 'topic_likes_per_course_sections'
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
			event_title = translate(_("Number of topics likes in ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users liking topics in ${title}",
									  mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of topics likes over unique user in ${title}",
									  mapping={'title': context_name}))

			event_type = 'topic_likes_in_%s' % (context_name.replace(' ', '_'))
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

	def analyze_events_per_device_types(self, period_breaks='1 day',
										minor_period_breaks=None,
										theme_seaborn_=True):
		"""
		return plots of topic likes grouped by device  types
		it consists of:
			- number of topic likes
			- number of unique users
			- ratio of topic likes over unique users
		"""
		tlt = self.tlt
		df = tlt.analyze_events_per_device_types(tlt.dataframe)
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of topics likes grouped by device types')
		user_title = _('Number of unique users liking topics grouped by device types')
		ratio_title = _('Ratio of topic likes over unique user grouped by device types')
		event_type = 'topic_likes_per_device_types'
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

	def analyze_events_per_enrollment_types(self, period_breaks='1 day',
											minor_period_breaks=None,
											theme_seaborn_=True):
		"""
		return plots of topic likes grouped by enrollment  types
		it consists of:
			- number of topic likes
			- number of unique users
			- ratio of topic likes over unique users
		"""
		tlt = self.tlt
		df = tlt.analyze_events_per_enrollment_types(tlt.dataframe)
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'enrollment_type'
		event_title = _('Number of topics likes grouped by enrollment types')
		user_title = _('Number of unique users liking topics grouped by enrollment types')
		ratio_title = _('Ratio of topic likes over unique user grouped by enrollment types')
		event_type = 'topic_likes_per_enrollment_types'
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
		event_y_axis_field = 'number_of_topic_likes'
		event_y_axis_label = _('Number of topic likes')
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
		event_y_axis_field = 'number_of_topic_likes'
		event_y_axis_label = _('Number of topic likes')
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

class TopicFavoritesTimeseriesPlot(object):

	def __init__(self, tft):
		"""
		tft = TopicFavoritesTimeseries
		"""
		self.tft = tft
		self.period = tft.period

	def explore_events(self, period_breaks='1 week', minor_period_breaks='1 day',
					   theme_seaborn_=True):
		"""
		return plots of topic favorites during period of time
		it consists of:
			- number of topic favorites
			- number of unique users
			- ratio of topic favorites over unique users
		"""
		tft = self.tft
		df = tft.analyze_events()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of topic favorites during period of time')
		user_title = _('Number of unique users choosing topics as favorites during period of time')
		ratio_title = _('Ratio of topic favorites over unique user on each available date')
		event_type = 'topic_favorites'
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
		tft = self.tft
		df = tft.analyze_events_per_course_sections()
		if df is None:
			return ()

		plots = []
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of topic favorites per course sections')
			user_title = _('Number of unique users choosing topics as favorite per course sections')
			ratio_title = _('Ratio of topic favorites over unique user per course sections')
			event_type = 'topic_favorites_per_course_sections'
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
			event_title = translate(_("Number of topics favorites in ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users choosing topics as favorites in ${title}",
									  mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of topics favorites over unique user in ${title}",
									  mapping={'title': context_name}))
			event_type = 'topic_favorites_in_%s' % (context_name.replace(' ', '_'))
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

	def analyze_events_per_device_types(self, period_breaks='1 day',
										minor_period_breaks=None,
										theme_seaborn_=True):
		"""
		return plots of topic favorites grouped by device  types
		it consists of:
			- number of topic favorites
			- number of unique users
			- ratio of topic likes over unique users
		"""
		tft = self.tft
		df = tft.analyze_events_per_device_types(tft.dataframe)
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of topics favorites grouped by device types')
		user_title = _('Number of unique users choosing topics as favorite grouped by device types')
		ratio_title = _('Ratio of topic favorites over unique user grouped by device types')
		event_type = 'topic_favorites_per_device_types'
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

	def analyze_events_per_enrollment_types(self, period_breaks='1 day',
											minor_period_breaks=None,
											theme_seaborn_=True):
		"""
		return plots of topic favorites grouped by enrollment  types
		it consists of:
			- number of topic favorites
			- number of unique users
			- ratio of topic likes over unique users
		"""
		tft = self.tft
		df = tft.analyze_events_per_enrollment_types(tft.dataframe)
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'enrollment_type'
		event_title = _('Number of topics favorites grouped by enrollment types')
		user_title = _('Number of unique users choosing topics as favorite grouped by enrollment types')
		ratio_title = _('Ratio of topic favorites over unique user grouped by enrollment types')
		event_type = 'topic_favorites_per_enrollment_types'
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
		event_y_axis_field = 'number_of_topic_favorites'
		event_y_axis_label = _('Number of topic favorites')
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
		event_y_axis_field = 'number_of_topic_favorites'
		event_y_axis_label = _('Number of topic favorites')
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
