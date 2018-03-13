#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.view import view_config

from nti.analytics_pandas.analysis import ChatsJoinedTimeseries
from nti.analytics_pandas.analysis import ChatsInitiatedTimeseries

from nti.analytics_pandas.analysis import ContactsAddedTimeseries
from nti.analytics_pandas.analysis import ContactsRemovedTimeseries

from nti.analytics_pandas.analysis import FriendsListsMemberAddedTimeseries

from nti.analytics_pandas.analysis import EntityProfileViewsTimeseries

from nti.analytics_pandas.analysis.common import reset_dataframe_

from nti.app.analytics_pandas.views import MessageFactory as _

from nti.app.analytics_pandas.views.commons import build_event_chart_data
from nti.app.analytics_pandas.views.commons import build_event_table_data
from nti.app.analytics_pandas.views.commons import save_chart_to_temporary_file
from nti.app.analytics_pandas.views.commons import build_event_grouped_chart_data
from nti.app.analytics_pandas.views.commons import build_event_grouped_table_data

from nti.app.analytics_pandas.views.mixins import AbstractReportView

logger = __import__('logging').getLogger(__name__)

@view_config(name="SocialReport")
class SocialTimeseriesReportView(AbstractReportView):

    @property
    def report_title(self):
        return _(u'Social Report')

    def _build_data(self, data=_('sample social report')):
        keys = self.options.keys()
        if 'has_chats_initiated' not in keys:
            self.options['has_chats_initiated'] = False
        if 'has_chats_joined' not in keys:
            self.options['has_chats_joined'] = False
        if 'has_contacts_added' not in keys:
            self.options['has_contacts_added'] = False
        if 'has_contacts_removed' not in keys:
            self.options['has_contacts_removed'] = False
        if 'has_friend_list_member_added' not in keys:
            self.options['has_friend_list_member_added'] = False
        if 'has_profile_views' not in keys:
            self.options['has_profile_views'] = False
            self.options['has_profile_viewers'] = False
        self.options['data'] = data
        return self.options

    def __call__(self):
        values = self.readInput()
        if "MimeType" not in values.keys():
            values["MimeType"] = 'application/vnd.nextthought.reports.socialeventstimeseriescontext'
        self.options['start_date'] = values['start_date']
        self.options['end_date'] = values['end_date']
        data = {}
        if 'period' in values.keys():
            self.options['period'] = values['period']
        else:
            self.options['period'] = u'daily'
        cit = ChatsInitiatedTimeseries(self.db.session,
                                    self.options['start_date'],
                                    self.options['end_date'],
                                    period=self.options['period'])
        if not cit.dataframe.empty:
            data['chats_initiated'] = self.build_chats_initiated_data(cit)

        cjt = ChatsJoinedTimeseries(self.db.session,
                                    self.options['start_date'],
                                    self.options['end_date'],
                                    period=self.options['period'])
        if not cjt.dataframe.empty:
            data['chats_joined'] = self.build_chats_joined_data(cjt)

        cat = ContactsAddedTimeseries(self.db.session,
                                      self.options['start_date'],
                                      self.options['end_date'],
                                      period=self.options['period'])
        if not cat.dataframe.empty:
            data['contacts_added'] = self.build_contacts_added_data(cat)

        crt = ContactsRemovedTimeseries(self.db.session,
                                      self.options['start_date'],
                                      self.options['end_date'],
                                      period=self.options['period'])
        if not crt.dataframe.empty:
            data['contacts_removed'] = self.build_contacts_removed_data(crt)
        
        flmat = FriendsListsMemberAddedTimeseries(self.db.session,
                                      self.options['start_date'],
                                      self.options['end_date'],
                                      period=self.options['period'])
        if not flmat.dataframe.empty:
            data['friend_list'] = self.build_friend_list_member_added_data(flmat)
        
        epvt = EntityProfileViewsTimeseries(self.db.session,
                                      self.options['start_date'],
                                      self.options['end_date'],
                                      period=self.options['period'])
        if not epvt.dataframe.empty:
            data['profile_views'] = self.build_entity_profile_views_data(epvt)
            data['profile_viewers'] = self.build_profile_viewers_data(epvt)
        self._build_data(data)
        return self.options

    def build_chats_initiated_data(self, cit):
        df = cit.analyze_events()
        if df.empty:
            self.options['has_chats_initiated'] = False
            return
        self.options['has_chats_initiated'] = True
        chats_initiated = {}
        chats_initiated['num_rows'] = df.shape[0]
        chats_initiated['column_name'] = _(u'Chats Initiated')
        if chats_initiated['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_chats_initiated',
                                           chats_initiated['column_name'])
            chats_initiated['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            chats_initiated['events_chart'] = ()
        
        if chats_initiated['num_rows'] == 1:
            chats_initiated['tuples'] = build_event_table_data(df)
        else:
            chats_initiated['tuples'] = ()
        return chats_initiated

    def build_chats_joined_data(self, cjt):
        df = cjt.analyze_one_one_and_group_chat()
        if df.empty:
            self.options['has_chats_joined'] = False
            return
        self.options['has_chats_joined'] = True
        df = reset_dataframe_(df)
        columns = ['timestamp_period', 'chat_type', 'number_of_chats']
        df = df[columns]
        df['timestamp_period'] = df['timestamp_period'].astype(str)
        chats_joined = {}
        timestamp_num = len(df['timestamp_period'].unique())
        chats_joined['num_rows'] = df.shape[0]
        chats_joined['column_name'] = _(u'Chats')
        if chats_joined['num_rows'] > 1 and timestamp_num > 1:
            chart = build_event_grouped_chart_data(df, 'chat_type')
            chats_joined['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            chats_joined['events_chart'] = ()
            
        if chats_joined['num_rows'] == 1 or timestamp_num == 1:
            chats_joined['tuples'] = build_event_grouped_table_data(df)
        else:
            chats_joined['tuples'] = ()
        return chats_joined

    def build_contacts_added_data(self, cat):
        df = cat.analyze_events()
        if df.empty:
            self.options['has_contacts_added'] = False
            return
        self.options['has_contacts_added'] = True
        contacts_added = {}
        contacts_added['num_rows'] = df.shape[0]
        contacts_added['column_name'] = _(u'Contacts Added')
        if contacts_added['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_contacts_added',
                                           contacts_added['column_name'])
            contacts_added['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            contacts_added['events_chart'] = ()
        
        if contacts_added['num_rows'] == 1:
            contacts_added['tuples'] = build_event_table_data(df)
        else:
            contacts_added['tuples'] = ()
        return contacts_added

    def build_contacts_removed_data(self, crt):
        df = crt.analyze_events()
        if df.empty:
            self.options['has_contacts_removed'] = False
            return
        self.options['has_contacts_removed'] = True
        contacts_removed = {}
        contacts_removed['num_rows'] = df.shape[0]
        contacts_removed['column_name'] = _(u'Contacts Removed')
        if contacts_removed['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_contacts_removed',
                                           contacts_removed['column_name'])
            contacts_removed['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            contacts_removed['events_chart'] = ()
        
        if contacts_removed['num_rows'] == 1:
            contacts_removed['tuples'] = build_event_table_data(df)
        else:
            contacts_removed['tuples'] = ()
        return contacts_removed

    def build_friend_list_member_added_data(self, flmat):
        df = flmat.analyze_number_of_friend_list_members_added()
        if df.empty:
            self.options['has_friend_list_member_added'] = False
            return
        self.options['has_friend_list_member_added'] = True
        df = reset_dataframe_(df) 
        df = df.round({'average_number_of_friend_list_members_added' : 2})
        friend_list = {}
        friend_list['tuples'] = build_event_table_data(df, column_list=df.columns)
        return friend_list

    def build_entity_profile_views_data(self, epvt):
        df = epvt.analyze_events()
        if df.empty:
            self.options['has_profile_views'] = False
            return
        self.options['has_profile_views'] = True
        profile_views = {}
        profile_views['num_rows'] = df.shape[0]
        profile_views['column_name'] = _(u'Profile Views')
        if profile_views['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_profile_views',
                                           profile_views['column_name'])
            profile_views['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            profile_views['events_chart'] = ()
        
        if profile_views['num_rows'] == 1:
            profile_views['tuples'] = build_event_table_data(df)
        else:
            profile_views['tuples'] = ()
        return profile_views

    def build_profile_viewers_data(self, epvt):
        df = epvt.analyze_views_by_owner_or_by_others()
        if df.empty:
            self.options['has_profile_viewers'] = False
            return
        self.options['has_profile_viewers'] = True
        columns = ['timestamp_period', 'viewers', 'number_of_profile_views']
        df = reset_dataframe_(df)
        df = df[columns]
        df['timestamp_period'] = df['timestamp_period'].astype(str)
        timestamp_num = len(df['timestamp_period'].unique())
        profile_viewers = {}
        profile_viewers['num_rows'] = df.shape[0]
        profile_viewers['column_name'] = _(u'Number of Profile Views')
        if profile_viewers['num_rows'] > 1 and timestamp_num > 1:
            chart = build_event_grouped_chart_data(df, 'viewers')
            profile_viewers['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            profile_viewers['events_chart'] = False
            
        if profile_viewers['num_rows'] == 1 or timestamp_num == 1:
            profile_viewers['tuples'] = build_event_grouped_table_data(df)
            profile_viewers['col'] = _(u'Viewers')
        else:
            profile_viewers['tuples'] = False
        return profile_viewers
