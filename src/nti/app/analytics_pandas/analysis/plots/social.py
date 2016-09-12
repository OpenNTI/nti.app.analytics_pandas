#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pandas as pd

from . import MessageFactory as _

from .commons import generate_three_plots
from .commons import line_plot_x_axis_date
from .commons import generate_three_group_by_plots
from .commons import histogram_plot_x_axis_discrete

class ContactsEventsTimeseriesPlot(object):

	def __init__(self, cet):
		"""
		cet = ContactsEventsTimeseries
		"""
		self.cet = cet

	def combine_events(self,
					   period_breaks=None,
					   minor_period_breaks=None,
					   theme_seaborn_=True):
		cet = self.cet
		df = cet.combine_events()
		group_by = 'event_type'
		event_title = _('Number of contact related events grouped by event type during period of time')
		user_title = _('Number of unique users creating contact events during period of time')
		ratio_title = _('Ratio of contact related events over unique user on each available date')
		event_type = 'combine_contact_events'
		event_y_axis_field = 'total_events'
		event_y_axis_label = _('Number of contact related events')
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
											  period=cet.period)
		return plots

class ContactsAddedTimeseriesPlot(object):

	def __init__(self, cat):
		"""
		cat = ContactsAddedTimeseries
		"""
		self.cat = cat
		self.period = cat.period

	def analyze_events(self,
					   period_breaks=None,
					   minor_period_breaks=None,
					   theme_seaborn_=True):
		cat = self.cat
		df = cat.analyze_events()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of contacts added during period of time')
		user_title = _('Number of unique users adding contacts during period of time')
		ratio_title = _('Ratio of contacts added over unique users during period of time')
		event_type = 'contacts_added'
		event_y_axis_field = 'number_of_contacts_added'
		event_y_axis_label = _('Number of contacts added')

		plots = generate_three_plots(
								 df,
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

	def analyze_application_types(self,
								  period_breaks=None,
								  minor_period_breaks=None,
								  theme_seaborn_=True):
		cat = self.cat
		df = cat.analyze_application_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'application_type'
		event_title = _('Number of contacts added per application type')
		user_title = _('Number of unique users adding contacts per application type')
		ratio_title = _('Ratio of contacts added over unique users per application type')
		event_type = 'contacts_added_per_application_type'
		event_y_axis_field = 'number_of_contacts_added'
		event_y_axis_label = _('Number of contacts added')

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
		cat = self.cat
		users_df = cat.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(
											df=users_df,
											x_axis_field='username' ,
											y_axis_field='number_of_contacts_added',
											x_axis_label=_('Username'),
											y_axis_label=_('Number of contacts added'),
											title=_('The most active users adding contacts'),
											stat='identity',
											plot_name='most_active_users_adding_contacts')
		return (plot_users,)

class ContactsRemovedTimeseriesPlot(object):

	def __init__(self, crt):
		"""
		crt = ContactsRemovedTimeseries
		"""
		self.crt = crt
		self.period = crt.period

	def analyze_events(self,
					   period_breaks=None,
					   minor_period_breaks=None,
					   theme_seaborn_=True):
		crt = self.crt
		df = crt.analyze_events()
		if df is None:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of contacts removed during period of time')
		user_title = _('Number of unique users removing contacts during period of time')
		ratio_title = _('Ratio of contacts removed over unique users during period of time')
		event_type = 'contacts_removed'
		event_y_axis_field = 'number_of_contacts_removed'
		event_y_axis_label = _('Number of contacts removed')

		plots = generate_three_plots(
								 df,
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

	def analyze_application_types(self,
								  period_breaks=None,
								  minor_period_breaks=None,
								  theme_seaborn_=True):
		crt = self.crt
		df = crt.analyze_application_types()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'application_type'
		event_title = _('Number of contacts removed per application type')
		user_title = _('Number of unique users removing contacts per application type')
		ratio_title = _('Ratio of contacts removed over unique users per application type')
		event_type = 'contacts_removed_per_application_type'
		event_y_axis_field = 'number_of_contacts_removed'
		event_y_axis_label = _('Number of contacts removed')

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
		crt = self.crt
		users_df = crt.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(
											df=users_df,
											x_axis_field='username' ,
											y_axis_field='number_of_contacts_removed',
											x_axis_label=_('Username'),
											y_axis_label=_('Number of contacts removed'),
											title=_('The most active users removing contacts'),
											stat='identity',
											plot_name='most_active_users_removing_contacts')
		return (plot_users,)

class FriendsListsMemberAddedTimeseriesPlot(object):

	def __init__(self, flmat):
		"""
		flmat = FriendsListsMemberAddedTimeseries
		"""
		self.flmat = flmat
		self.period = flmat.period

	def analyze_number_of_friend_list_members_added(self,
					   								period_breaks=None,
					   								minor_period_breaks=None,
					  	 							theme_seaborn_=True):
		flmat = self.flmat
		df = flmat.analyze_number_of_friend_list_members_added()
		if df is None:
			return ()
		plot_average_number_of_friend_list_members_added = line_plot_x_axis_date(
															df=df,
															x_axis_field='timestamp_period',
															y_axis_field='average_number_of_friend_list_members_added',
															x_axis_label='Date',
															y_axis_label='Average number of friend list members added',
															title='Average number of friend list members added during time period',
															period_breaks=period_breaks,
															minor_breaks=minor_period_breaks,
															theme_seaborn_=theme_seaborn_,
															plot_name='average_number_of_friend_list_members_added')

		plot_total_number_of_friend_list_members_added = line_plot_x_axis_date(
															df=df,
															x_axis_field='timestamp_period',
															y_axis_field='total_number_of_friend_list_members_added',
															x_axis_label='Date',
															y_axis_label='Total number of friend list members added',
															title='Total number of friend list members added during time period',
															period_breaks=period_breaks,
															minor_breaks=minor_period_breaks,
															theme_seaborn_=theme_seaborn_,
															plot_name='total_number_of_friend_list_members_added')

		plot_number_of_friend_lists = line_plot_x_axis_date(
													  df=df,
													  x_axis_field='timestamp_period',
													  y_axis_field='number_of_friend_lists',
													  x_axis_label='Date',
													  y_axis_label='Number of friend lists',
													  title='Number of friend lists during time period',
													  period_breaks=period_breaks,
													  minor_breaks=minor_period_breaks,
													  theme_seaborn_=theme_seaborn_,
													  plot_name='number_of_friend_lists')

		return (plot_average_number_of_friend_list_members_added,
				plot_total_number_of_friend_list_members_added,
				plot_number_of_friend_lists)
