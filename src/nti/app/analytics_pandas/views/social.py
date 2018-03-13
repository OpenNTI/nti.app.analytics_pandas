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
from nti.analytics_pandas.analysis import ContactsEventsTimeseries

from nti.analytics_pandas.analysis import FriendsListsMemberAddedTimeseries

from nti.analytics_pandas.analysis import EntityProfileViewsTimeseries
from nti.analytics_pandas.analysis import EntityProfileViewEventsTimeseries
from nti.analytics_pandas.analysis import EntityProfileActivityViewsTimeseries
from nti.analytics_pandas.analysis import EntityProfileMembershipViewsTimeseries

from nti.analytics_pandas.analysis.common import reset_dataframe_

from nti.app.analytics_pandas.views import MessageFactory as _

from nti.app.analytics_pandas.views.commons import build_event_chart_data
from nti.app.analytics_pandas.views.commons import build_event_table_data
from nti.app.analytics_pandas.views.commons import save_chart_to_temporary_file
from nti.app.analytics_pandas.views.commons import build_event_grouped_chart_data
from nti.app.analytics_pandas.views.commons import build_event_grouped_table_data
from nti.app.analytics_pandas.views.commons import get_course_id_and_name_given_ntiid
from nti.app.analytics_pandas.views.commons import build_events_data_by_sharing_type
from nti.app.analytics_pandas.views.commons import build_events_data_by_resource_type
from nti.app.analytics_pandas.views.commons import build_events_data_by_enrollment_type

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
