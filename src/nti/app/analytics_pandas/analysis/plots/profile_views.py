#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: profile_views.py 78747 2015-12-10 15:54:52Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

import pandas as pd

from .commons import generate_three_plots
from .commons import generate_three_group_by_plots
from .commons import histogram_plot_x_axis_discrete

class EntityProfileViewEventsTimeseriesPlot(object):
	def __init__(self, epvet):
		"""
		epvet = EntityProfileViewEventsTimeseries
		"""
		self.epvet = epvet
		self.period = epvet.period

	def combine_events(self, period_breaks=None, minor_period_breaks=None,
					   theme_seaborn_=True):
		epvet = self.epvet
		df = epvet.combine_events()
		if df.empty:
			return()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'event_type'
		event_title = _('Number of profile view events per type')
		user_title = _("Number of unique users creating profile view events per type")
		ratio_title = _("Ratio of profile view events over unique user per event type")

		event_type = 'profile_view_events'
		event_y_axis_field = 'total_events'
		event_y_axis_label = _('Number of profile view events')

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

class EntityProfileViewsTimeseriesPlot(object):

	def __init__(self, epvt):
		"""
		epvt = EntityProfileViewsTimeseries
		"""
		self.epvt = epvt
		self.period = epvt.period

	def explore_events(self, period_breaks=None, minor_period_breaks=None,
					   theme_seaborn_=True):
		epvt = self.epvt
		df = epvt.analyze_events()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of profile views')
		user_title = _("Number of unique users viewing profiles")
		ratio_title = _("Ratio of profile views over unique user")

		event_type = 'profile_views'
		event_y_axis_field = 'number_of_profile_views'
		event_y_axis_label = _('Number of profile views')

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

	def analyze_application_types(self,
								  period_breaks=None,
								  minor_period_breaks=None,
					   			  theme_seaborn_=True):
		epvt = self.epvt
		df = epvt.analyze_application_types()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'application_type'
		event_title = _('Number of profile views per application type')
		user_title = _("Number of unique users viewing profiles per application type")
		ratio_title = _("Ratio of profile views over unique user per application type")

		event_type = 'profile_views_per_application_type'
		event_y_axis_field = 'number_of_profile_views'
		event_y_axis_label = _('Number of profile views')

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

	def analyze_views_by_owner_or_by_others(self,
											period_breaks=None,
											minor_period_breaks=None,
							   				theme_seaborn_=True):
		epvt = self.epvt
		df = epvt.analyze_views_by_owner_or_by_others()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'viewers'
		event_title = _('Number of profile views per viewer type')
		user_title = _('Number of unique users viewing profiles per viewer type')
		ratio_title = _('Ratio of profile views over unique user per viewer type')

		event_type = 'profile_views_per_viewer_type'
		event_y_axis_field = 'number_of_profile_views'
		event_y_axis_label = _('Number of profile views')

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
		epvt = self.epvt
		users_df = epvt.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(
											df=users_df,
											x_axis_field='username' ,
											y_axis_field='number_of_profile_views',
											x_axis_label=_('Username'),
											y_axis_label=_('Number of profile views'),
											title=_('The most active users viewing profiles'),
											stat='identity',
											plot_name='most_active_user_viewing_profiles')
		return (plot_users,)

	def plot_the_most_viewed_profiles(self, max_rank_number=10):
		epvt = self.epvt
		df = epvt.get_the_most_viewed_profiles(max_rank_number)
		if df is None:
			return ()

		plot_profiles = histogram_plot_x_axis_discrete(
											df=df,
											x_axis_field='profile' ,
											y_axis_field='number_of_profile_viewed',
											x_axis_label=_('Profile'),
											y_axis_label=_('Number of profile viewed'),
											title=_('The most viewed profiles'),
											stat='identity',
											plot_name='most_viewed_profiles')
		return (plot_profiles,)

class EntityProfileActivityViewsTimeseriesPlot(object):

	def __init__(self, epavt):
		"""
		epavt = EntityProfileActivityViewsTimeseries
		"""
		self.epavt = epavt
		self.period = epavt.period

	def explore_events(self, period_breaks=None, minor_period_breaks=None,
					   theme_seaborn_=True):
		epavt = self.epavt
		df = epavt.analyze_events()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of profile activity views')
		user_title = _("Number of unique users viewing profile activities")
		ratio_title = _("Ratio of profile activity views over unique user")

		event_type = 'profile_activity_views'
		event_y_axis_field = 'number_of_profile_activity_views'
		event_y_axis_label = _('Number of profile activity views')

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

	def analyze_application_types(self,
								  period_breaks=None,
								  minor_period_breaks=None,
					   			  theme_seaborn_=True):
		epavt = self.epavt
		df = epavt.analyze_application_types()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'application_type'
		event_title = _('Number of profile activity views per application type')
		user_title = _("Number of unique users viewing profile activities per application type")
		ratio_title = _("Ratio of profile activity views over unique user per application type")

		event_type = 'profile_activity_views_per_application_type'
		event_y_axis_field = 'number_of_profile_activity_views'
		event_y_axis_label = _('Number of profile activity views')

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

	def analyze_views_by_owner_or_by_others(self,
									 		period_breaks=None,
									  		minor_period_breaks=None,
									   		theme_seaborn_=True):
		epavt = self.epavt
		df = epavt.analyze_views_by_owner_or_by_others()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'viewers'
		event_title = _('Number of profile activity views per viewer type')
		user_title = _("Number of unique users viewing profile activities per viewer type")
		ratio_title = _("Ratio of profile activity views over unique user per per viewer type")

		event_type = 'profile_activity_views_per_viewer_type'
		event_y_axis_field = 'number_of_profile_activity_views'
		event_y_axis_label = _('Number of profile activity views')

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
		epavt = self.epavt
		users_df = epavt.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(
											df=users_df,
											x_axis_field='username' ,
											y_axis_field='number_of_profile_activity_views',
											x_axis_label=_('Username'),
											y_axis_label=_('Number of profile activity views'),
											title=_('The most active users viewing profile activities'),
											stat='identity',
											plot_name='most_active_user_viewing_profile_activities')
		return (plot_users,)

	def plot_the_most_viewed_profile_activities(self, max_rank_number=10):
		epavt = self.epavt
		df = epavt.get_the_most_viewed_profile_activities(max_rank_number)
		if df is None:
			return ()

		plot_profiles = histogram_plot_x_axis_discrete(
											df=df,
											x_axis_field='profile' ,
											y_axis_field='number_of_profile_activity_viewed',
											x_axis_label=_('Profile'),
											y_axis_label=_('Number of profile activity viewed'),
											title=_('The most viewed profile activities'),
											stat='identity',
											plot_name='most_viewed_profile_activities')
		return (plot_profiles,)

class EntityProfileMembershipViewsTimeseriesPlot(object):

	def __init__(self, epmvt):
		"""
		epmvt = EntityProfileMembershipViewsTimeseries
		"""
		self.epmvt = epmvt
		self.period = epmvt.period

	def explore_events(self, period_breaks=None, minor_period_breaks=None,
					   theme_seaborn_=True):
		epmvt = self.epmvt
		df = epmvt.analyze_events()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of profile membership views')
		user_title = _("Number of unique users viewing profile memberships")
		ratio_title = _("Ratio of profile membership views over unique user")

		event_type = 'profile_membership_views'
		event_y_axis_field = 'number_of_profile_membership_views'
		event_y_axis_label = _('Number of profile membership views')

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

	def analyze_application_types(self,
								  period_breaks=None,
								  minor_period_breaks=None,
					   			  theme_seaborn_=True):
		epmvt = self.epmvt
		df = epmvt.analyze_application_types()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'application_type'
		event_title = _('Number of profile membership views per application type')
		user_title = _("Number of unique users viewing profile memberships per application type")
		ratio_title = _("Ratio of profile membership views over unique user per application type")

		event_type = 'profile_membership_views_per_application_type'
		event_y_axis_field = 'number_of_profile_membership_views'
		event_y_axis_label = _('Number of profile membership views')

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

	def analyze_views_by_owner_or_by_others(self,
											period_breaks=None,
											minor_period_breaks=None,
							   				theme_seaborn_=True):
		epmvt = self.epmvt
		df = epmvt.analyze_views_by_owner_or_by_others()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'viewers'
		event_title = _('Number of profile membership views per viewer type')
		user_title = _("Number of unique users viewing profile memberships per viewer type")
		ratio_title = _("Ratio of profile membership views over unique user per viewer type")

		event_type = 'profile_membership_views_per_viewer_type'
		event_y_axis_field = 'number_of_profile_membership_views'
		event_y_axis_label = _('Number of profile membership views')

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
		epmvt = self.epmvt
		users_df = epmvt.get_the_most_active_users(max_rank_number)
		if users_df is None:
			return ()

		plot_users = histogram_plot_x_axis_discrete(
											df=users_df,
											x_axis_field='username' ,
											y_axis_field='number_of_profile_membership_views',
											x_axis_label=_('Username'),
											y_axis_label=_('Number of profile membership views'),
											title=_('The most active users viewing profile membership'),
											stat='identity',
											plot_name='most_active_user_viewing_profile_memberships')
		return (plot_users,)

	def plot_the_most_viewed_profile_memberships(self, max_rank_number=10):
		epmvt = self.epmvt
		df = epmvt.get_the_most_viewed_profile_memberships(max_rank_number)
		if df is None:
			return ()

		plot_profiles = histogram_plot_x_axis_discrete(
											df=df,
											x_axis_field='profile' ,
											y_axis_field='number_of_profile_membership_viewed',
											x_axis_label=_('Profile'),
											y_axis_label=_('Number of profile membership viewed'),
											title=_('The most viewed profile memberships'),
											stat='identity',
											plot_name='most_viewed_profile_memberships')
		return (plot_profiles,)
