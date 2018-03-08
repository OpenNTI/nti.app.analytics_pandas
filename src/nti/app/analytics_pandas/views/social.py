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

@view_config(name="SocialsReport")
class SocialsTimeseriesReportView(AbstractReportView):

    @property
    def report_title(self):
        return _(u'socials Report')

    def _build_data(self, data=_('sample socials report')):
        keys = self.options.keys()
        self.options['data'] = data
        return self.options

    def __call__(self):
        values = self.readInput()
        if "MimeType" not in values.keys():
            values["MimeType"] = 'application/vnd.nextthought.reports.socialeventstimeseriescontext'
        self.options['ntiid'] = values['ntiid']
        course_ids, course_names = get_course_id_and_name_given_ntiid(self.db.session,
                                                                      self.options['ntiid'])
        data = {}
        if course_ids and course_names:
            self.options['course_ids'] = course_ids
            self.options['course_names'] = ", ".join(map(str, course_names or ()))
            self.options['start_date'] = values['start_date']
            self.options['end_date'] = values['end_date']
            if 'period' in values.keys():
                self.options['period'] = values['period']
            else:
                self.options['period'] = u'daily'
        self._build_data(data)
        return self.options