#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from zope import interface

from nti.analytics_pandas.analysis import ChatsTimeseriesPlot
from nti.analytics_pandas.analysis import ChatsJoinedTimeseries
from nti.analytics_pandas.analysis import ChatsInitiatedTimeseries

from nti.analytics_pandas.analysis import ContactsAddedTimeseries
from nti.analytics_pandas.analysis import ContactsAddedTimeseriesPlot

from nti.analytics_pandas.analysis import ContactsRemovedTimeseries
from nti.analytics_pandas.analysis import ContactsRemovedTimeseriesPlot

from nti.analytics_pandas.analysis import ContactsEventsTimeseries
from nti.analytics_pandas.analysis import ContactsEventsTimeseriesPlot

from nti.analytics_pandas.analysis import FriendsListsMemberAddedTimeseries
from nti.analytics_pandas.analysis import FriendsListsMemberAddedTimeseriesPlot

from nti.analytics_pandas.analysis import EntityProfileViewsTimeseries
from nti.analytics_pandas.analysis import EntityProfileViewsTimeseriesPlot

from nti.analytics_pandas.analysis import EntityProfileActivityViewsTimeseries
from nti.analytics_pandas.analysis import EntityProfileActivityViewsTimeseriesPlot

from nti.analytics_pandas.analysis import EntityProfileMembershipViewsTimeseries
from nti.analytics_pandas.analysis import EntityProfileMembershipViewsTimeseriesPlot

from nti.analytics_pandas.analysis import EntityProfileViewEventsTimeseries

from nti.app.analytics_pandas.reports.report import PandasReportContext

from .commons import build_plot_images_dictionary

from .mixins import AbstractReportView

class SocialTimeseriesContext(PandasReportContext):

	def __init__(self, *args, **kwargs):
		super(SocialTimeseriesContext, self).__init__(*args, **kwargs)

Context = SocialTimeseriesContext

class SocialTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Social Related Events Report')

	def _build_data(self, data=_('sample social related events report')):
		keys = self.options.keys()
		if 'has_contacts_added_data' not in keys:
			self.options['has_contacts_added_data'] = False
		if 'has_contacts_removed_data' not in keys:
			self.options['has_contacts_removed_data'] = False
		if 'has_combined_contact_event_data' not in keys:
			self.options['has_combined_contact_event_data'] = False
		if 'has_friendlist_members_added_data' not in keys:
			self.options['has_friendlist_members_added_data'] = False
		if 'has_chats_data' not in keys:
			self.options['has_chats_data'] = False
		if 'has_profile_view_events' not in keys:
			self.options['has_profile_view_events'] = False
		self.options['data'] = data
		return self.options

	def __call__(self):
		data = {}
		self.cat = ContactsAddedTimeseries(self.db.session,
										   self.context.start_date,
										   self.context.end_date,
										   period=self.context.period)

		if self.cat.dataframe.empty:
			self.options['has_contacts_added_data'] = False
		else:
			self.options['has_contacts_added_data'] = True
			data = self.generate_contacts_added_plots(data)

		self.crt = ContactsRemovedTimeseries(self.db.session,
										   	 self.context.start_date,
											 self.context.end_date,
											 period=self.context.period)
		if self.crt.dataframe.empty:
			self.options['has_contacts_removed_data'] = False
		else:
			self.options['has_contacts_removed_data'] = True
			data = self.generate_contacts_removed_plots(data)


		if not self.cat.dataframe.empty and not self.crt.dataframe.empty:
			self.cet = ContactsEventsTimeseries(cat=self.cat, crt=self.crt)
			data = self.generate_combined_contact_related_events(data)

		self.flmat = FriendsListsMemberAddedTimeseries(self.db.session,
												   	   self.context.start_date,
													   self.context.end_date,
													   period=self.context.period)
		if self.flmat.dataframe.empty:
			self.options['has_friendlist_members_added_data'] = False
		else:
			self.options['has_friendlist_members_added_data'] = True
			data = self.generate_friendlist_members_added_plots(data)

		self.cit = ChatsInitiatedTimeseries(self.db.session,
										   	self.context.start_date,
											self.context.end_date,
											period=self.context.period)
		self.cjt = ChatsJoinedTimeseries(self.db.session,
									   	 self.context.start_date,
										 self.context.end_date,
										 period=self.context.period)

		if not self.cit.dataframe.empty or not self.cjt.dataframe.empty:
			self.options['has_chats_data'] = True
			self.ctp = ChatsTimeseriesPlot(cit=self.cit, cjt=self.cjt)
			data = self.generate_chats_initiated_plots(data)
			data = self.generate_chats_initiated_plots_per_application_type(data)
			data = self.get_number_of_users_join_chats_per_date_plots(data)
			data = self.generate_one_one_and_group_chat_plots(data)

		self.epvt = EntityProfileViewsTimeseries(self.db.session,
											   	 self.context.start_date,
												 self.context.end_date,
												 period=self.context.period)
		self.epavt = EntityProfileActivityViewsTimeseries(self.db.session,
													   	  self.context.start_date,
														  self.context.end_date,
														  period=self.context.period)
		self.epmvt = EntityProfileMembershipViewsTimeseries(self.db.session,
														   	self.context.start_date,
															self.context.end_date,
															period=self.context.period)
		self.epvet = EntityProfileViewEventsTimeseries(epvt=self.epvt, epavt=self.epavt, epmvt=self.epmvt)
		if self.epvet.period is not None:
			self.options['has_profile_view_events'] = True
			if not self.epvt.dataframe.empty:
				data = self.generate_profile_view_plots(data)
			if not self.epavt.dataframe.empty:
				data = self.generate_profile_activity_view_plots(data)
			if not self.epmvt.dataframe.empty:
				data = self.generate_profile_membership_view_plots(data)
		else:
			self.options['has_profile_view_events'] = False

		self._build_data(data)
		return self.options

	def generate_chats_initiated_plots(self, data):
		plots = self.ctp.explore_chats_initiated(self.context.period_breaks,
												 self.context.minor_period_breaks,
												 self.context.theme_bw_)
		if plots:
			data['chats_initiated'] = build_plot_images_dictionary(plots)
			self.options['has_chats_initiated'] = True
		else:
			self.options['has_chats_initiated'] = False
		return data

	def generate_chats_initiated_plots_per_application_type(self, data):
		plots = self.ctp.analyze_application_types(self.context.period_breaks,
												   self.context.minor_period_breaks,
												   self.context.theme_bw_)
		if plots:
			data['chats_initiated_per_application_type'] = build_plot_images_dictionary(plots)
			self.options['has_chats_initiated_per_application_type'] = True
		else:
			self.options['has_chats_initiated_per_application_type'] = False
		return data

	def get_number_of_users_join_chats_per_date_plots(self, data):
		plots = self.ctp.analyze_number_of_users_join_chats_per_date(
												   self.context.period_breaks,
												   self.context.minor_period_breaks,
												   self.context.theme_bw_)
		if plots:
			data['users_join_chats'] = build_plot_images_dictionary(plots)
			self.options['has_users_join_chats'] = True
		else:
			self.options['has_users_join_chats'] = False
		return data

	def generate_one_one_and_group_chat_plots(self, data):
		plot = self.ctp.analyze_one_one_and_group_chat(self.context.period_breaks,
													   self.context.minor_period_breaks,
													   self.context.theme_bw_)
		if plot:
			print(plot)
			data['one_one_and_group_chat'] = build_plot_images_dictionary(plot)
			self.options['has_one_one_or_group_chats'] = True
		else:
			self.options['has_one_one_or_group_chats'] = False
		return data

	def generate_contacts_added_plots(self, data):
		self.catp = ContactsAddedTimeseriesPlot(self.cat)
		data = self.get_contacts_added_plots(data)
		data = self.get_contacts_added_plots_per_application_type(data)
		data = self.get_the_most_active_users_contacts_added(data)
		return data

	def get_contacts_added_plots(self, data):
		plots = self.catp.analyze_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['contacts_added'] = build_plot_images_dictionary(plots)
		return data

	def get_contacts_added_plots_per_application_type(self, data):
		plots = self.catp.analyze_application_types(self.context.period_breaks,
										 			self.context.minor_period_breaks,
										 			self.context.theme_bw_)
		if plots:
			data['contacts_added_per_application_type'] = build_plot_images_dictionary(plots)
			self.options['has_contacts_added_per_application_type'] = True
		else:
			self.options['has_contacts_added_per_application_type'] = False
		return data

	def get_the_most_active_users_contacts_added(self, data):
		plot = self.catp.plot_the_most_active_users(max_rank_number=self.context.number_of_most_active_user)
		if plot:
			data['contacts_added_users'] = build_plot_images_dictionary(plot)
			self.options['has_contacts_added_users'] = True
		else:
			self.options['has_contacts_added_users'] = False
		return data

	def generate_contacts_removed_plots(self, data):
		self.crtp = ContactsRemovedTimeseriesPlot(self.crt)
		data = self.get_contacts_removed_plots(data)
		data = self.get_contacts_removed_plots_per_application_type(data)
		data = self.get_the_most_active_users_contacts_removed(data)
		return data

	def get_contacts_removed_plots(self, data):
		plots = self.crtp.analyze_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['contacts_removed'] = build_plot_images_dictionary(plots)
		return data

	def get_contacts_removed_plots_per_application_type(self, data):
		plots = self.crtp.analyze_application_types(self.context.period_breaks,
													self.context.minor_period_breaks,
													self.context.theme_bw_)
		if plots:
			data['contacts_removed_per_application_type'] = build_plot_images_dictionary(plots)
			self.options['has_contacts_removed_per_application_type'] = True
		else:
			self.options['has_contacts_removed_per_application_type'] = False
		return data

	def get_the_most_active_users_contacts_removed(self, data):
		plot = self.crtp.plot_the_most_active_users(max_rank_number=self.context.number_of_most_active_user)
		if plot:
			data['contacts_removed_users'] = build_plot_images_dictionary(plot)
			self.options['has_contacts_removed_users'] = True
		else:
			self.options['has_contacts_removed_users'] = False
		return data

	def generate_combined_contact_related_events(self, data):
		self.cetp = ContactsEventsTimeseriesPlot(self.cet)
		plot = self.cetp.combine_events(self.context.period_breaks,
										self.context.minor_period_breaks,
										self.context.theme_bw_)
		if plot :
			data['combine_contact_events'] = build_plot_images_dictionary(plot)
			self.options['has_combined_contact_event_data'] = True
		return data

	def generate_friendlist_members_added_plots(self, data):
		self.flmatp = FriendsListsMemberAddedTimeseriesPlot(self.flmat)
		data = self.get_friendlist_members_added_plots(data)
		return data

	def get_friendlist_members_added_plots(self, data):
		plots = self.flmatp.analyze_number_of_friend_list_members_added(
										self.context.period_breaks,
										self.context.minor_period_breaks,
										self.context.theme_bw_)
		if plots:
			data['friendlist_members_added'] = build_plot_images_dictionary(plots)
		return data

	def generate_profile_view_plots(self, data):
		self.epvtp = EntityProfileViewsTimeseriesPlot(self.epvt)
		data = self.get_profile_view_plots(data)
		data = self.get_profile_view_plots_per_application_type(data)
		data = self.get_profile_view_plots_per_viewer_type(data)
		data = self.get_profile_views_most_active_users_plot(data)
		data = self.get_the_most_viewed_profiles_plot(data)
		return data

	def get_profile_view_plots(self, data):
		plots = self.epvtp.explore_events(self.context.period_breaks,
										  self.context.minor_period_breaks,
										  self.context.theme_bw_)
		if plots:
			data['profile_views'] = build_plot_images_dictionary(plots)
			self.options['has_profile_views'] = True
		else:
			self.options['has_profile_views'] = False
		return data

	def get_profile_view_plots_per_application_type(self, data):
		plots = self.epvtp.analyze_application_types(self.context.period_breaks,
													 self.context.minor_period_breaks,
													 self.context.theme_bw_)
		if plots:
			data['profile_views_per_application_type'] = build_plot_images_dictionary(plots)
			self.options['has_profile_views_per_application_type'] = True
		else:
			self.options['has_profile_views_per_application_type'] = False
		return data

	def get_profile_view_plots_per_viewer_type(self, data):
		plots = self.epvtp.analyze_views_by_owner_or_by_others(self.context.period_breaks,
															   self.context.minor_period_breaks,
															   self.context.theme_bw_)
		if plots:
			data['profile_views_per_viewer_type'] = build_plot_images_dictionary(plots)
			self.options['has_profile_views_per_viewer_type'] = True
		else:
			self.options['has_profile_views_per_viewer_type'] = False
		return data

	def get_profile_views_most_active_users_plot(self, data):
		plots = self.epvtp.plot_the_most_active_users(max_rank_number=self.context.number_of_most_active_user)
		if plots:
			data['profile_views_most_active_users'] = build_plot_images_dictionary(plots)
			self.options['has_profile_views_most_active_users'] = True
		else:
			self.options['has_profile_views_most_active_users'] = False
		return data

	def get_the_most_viewed_profiles_plot(self, data):
		plots = self.epvtp.plot_the_most_viewed_profiles(max_rank_number=self.context.number_of_most_active_user)
		if plots:
			data['most_viewed_profiles'] = build_plot_images_dictionary(plots)
			self.options['has_most_viewed_profiles'] = True
		else:
			self.options['has_most_viewed_profiles'] = False
		return data


	def generate_profile_activity_view_plots(self, data):
		self.epavtp = EntityProfileActivityViewsTimeseriesPlot(self.epavt)
		data = self.get_profile_activity_view_plots(data)
		data = self.get_profile_activity_view_plots_per_application_type(data)
		data = self.get_profile_activity_view_plots_per_viewer_type(data)
		data = self.get_profile_activity_views_most_active_users_plot(data)
		data = self.get_the_most_viewed_profile_activities_plot(data)
		return data

	def get_profile_activity_view_plots(self, data):
		plots = self.epavtp.explore_events(self.context.period_breaks,
										   self.context.minor_period_breaks,
										   self.context.theme_bw_)
		if plots:
			data['profile_activity_views'] = build_plot_images_dictionary(plots)
			self.options['has_profile_activity_views'] = True
		else:
			self.options['has_profile_activity_views'] = False
		return data

	def get_profile_activity_view_plots_per_application_type(self, data):
		plots = self.epavtp.analyze_application_types(self.context.period_breaks,
													  self.context.minor_period_breaks,
													  self.context.theme_bw_)
		if plots:
			data['profile_activity_views_per_application_type'] = build_plot_images_dictionary(plots)
			self.options['has_profile_activity_views_per_application_type'] = True
		else:
			self.options['has_profile_activity_views_per_application_type'] = False
		return data

	def get_profile_activity_view_plots_per_viewer_type(self, data):
		plots = self.epavtp.analyze_views_by_owner_or_by_others(self.context.period_breaks,
															    self.context.minor_period_breaks,
															    self.context.theme_bw_)
		if plots:
			data['profile_activity_views_per_viewer_type'] = build_plot_images_dictionary(plots)
			self.options['has_profile_activity_views_per_viewer_type'] = True
		else:
			self.options['has_profile_activity_views_per_viewer_type'] = False
		return data

	def get_profile_activity_views_most_active_users_plot(self, data):
		plots = self.epavtp.plot_the_most_active_users(max_rank_number=self.context.number_of_most_active_user)
		if plots:
			data['profile_activity_views_most_active_users'] = build_plot_images_dictionary(plots)
			self.options['has_profile_activity_views_most_active_users'] = True
		else:
			self.options['has_profile_activity_views_most_active_users'] = False
		return data

	def get_the_most_viewed_profile_activities_plot(self, data):
		plots = self.epavtp.plot_the_most_viewed_profile_activities(max_rank_number=self.context.number_of_most_active_user)
		if plots:
			data['most_viewed_profile_activities'] = build_plot_images_dictionary(plots)
			self.options['has_most_viewed_profile_activities'] = True
		else:
			self.options['has_most_viewed_profile_activities'] = False
		return data

	def generate_profile_membership_view_plots(self, data):
		self.epmvtp = EntityProfileMembershipViewsTimeseriesPlot(self.epmvt)
		data = self.get_profile_membership_view_plots(data)
		data = self.get_profile_membership_view_plots_per_application_type(data)
		data = self.get_profile_membership_view_plots_per_viewer_type(data)
		data = self.get_profile_membership_views_most_active_users_plot(data)
		data = self.get_the_most_viewed_profile_memberships_plot(data)
		return data

	def get_profile_membership_view_plots(self, data):
		plots = self.epmvtp.explore_events(self.context.period_breaks,
										   self.context.minor_period_breaks,
										   self.context.theme_bw_)
		if plots:
			data['profile_membership_views'] = build_plot_images_dictionary(plots)
			self.options['has_profile_membership_views'] = True
		else:
			self.options['has_profile_membership_views'] = False
		return data

	def get_profile_membership_view_plots_per_application_type(self, data):
		plots = self.epmvtp.analyze_application_types(self.context.period_breaks,
													  self.context.minor_period_breaks,
													  self.context.theme_bw_)
		if plots:
			data['profile_membership_views_per_application_type'] = build_plot_images_dictionary(plots)
			self.options['has_profile_membership_views_per_application_type'] = True
		else:
			self.options['has_profile_membership_views_per_application_type'] = False
		return data

	def get_profile_membership_view_plots_per_viewer_type(self, data):
		plots = self.epmvtp.analyze_views_by_owner_or_by_others(self.context.period_breaks,
															    self.context.minor_period_breaks,
															    self.context.theme_bw_)
		if plots:
			data['profile_membership_views_per_viewer_type'] = build_plot_images_dictionary(plots)
			self.options['has_profile_membership_views_per_viewer_type'] = True
		else:
			self.options['has_profile_membership_views_per_viewer_type'] = False
		return data

	def get_profile_membership_views_most_active_users_plot(self, data):
		plots = self.epmvtp.plot_the_most_active_users(max_rank_number=self.context.number_of_most_active_user)
		if plots:
			data['profile_membership_views_most_active_users'] = build_plot_images_dictionary(plots)
			self.options['has_profile_membership_views_most_active_users'] = True
		else:
			self.options['has_profile_membership_views_most_active_users'] = False
		return data

	def get_the_most_viewed_profile_memberships_plot(self, data):
		plots = self.epmvtp.plot_the_most_viewed_profile_memberships(max_rank_number=self.context.number_of_most_active_user)
		if plots:
			data['most_viewed_profile_memberships'] = build_plot_images_dictionary(plots)
			self.options['has_most_viewed_profile_memberships'] = True
		else:
			self.options['has_most_viewed_profile_memberships'] = False
		return data

View = SocialTimeseriesReport = SocialTimeseriesReportView
