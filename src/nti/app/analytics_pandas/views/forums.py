#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import numpy as np

from pyramid.view import view_config

from nti.analytics_pandas.analysis import ForumsCreatedTimeseries
from nti.analytics_pandas.analysis import ForumCommentLikesTimeseries
from nti.analytics_pandas.analysis import ForumsCommentsCreatedTimeseries
from nti.analytics_pandas.analysis import ForumCommentFavoritesTimeseries

from nti.analytics_pandas.analysis.common import get_data
from nti.analytics_pandas.analysis.common import reset_dataframe_

from nti.app.analytics_pandas.views import MessageFactory as _

from nti.app.analytics_pandas.views.commons import iternamedtuples
from nti.app.analytics_pandas.views.commons import build_event_chart_data
from nti.app.analytics_pandas.views.commons import build_event_table_data
from nti.app.analytics_pandas.views.commons import save_chart_to_temporary_file
from nti.app.analytics_pandas.views.commons import build_event_grouped_chart_data
from nti.app.analytics_pandas.views.commons import build_event_grouped_table_data
from nti.app.analytics_pandas.views.commons import get_course_id_and_name_given_ntiid
from nti.app.analytics_pandas.views.commons import build_events_data_by_device_type
from nti.app.analytics_pandas.views.commons import build_events_data_by_sharing_type
from nti.app.analytics_pandas.views.commons import build_events_data_by_resource_type
from nti.app.analytics_pandas.views.commons import build_events_data_by_enrollment_type

from nti.app.analytics_pandas.views.mixins import AbstractReportView

logger = __import__('logging').getLogger(__name__)

@view_config(name="ForumsReport")
class ForumsTimeseriesReportView(AbstractReportView):

    @property
    def report_title(self):
        return _(u'Forums Report')

    def _build_data(self, data=_('sample forums report')):
        keys = self.options.keys()
        self.options['data'] = data
        if 'has_forums_created_data' not in keys:
            self.options['has_forums_created_data'] = False
        
        return self.options

    def __call__(self):
        values = self.readInput()
        if "MimeType" not in values.keys():
            values["MimeType"] = 'application/vnd.nextthought.reports.forumeventstimeseriescontext'
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

        fct = ForumsCreatedTimeseries(self.db.session,
                                      self.options['start_date'],
                                      self.options['end_date'],
                                      self.options['course_ids'] or (),
                                      period=self.options['period'])        
        if not fct.dataframe.empty:
            self.options['has_forums_created_data'] = True
            self.build_forums_created_data(fct)
        self._build_data(data)
        return self.options

    def build_forums_created_data(self, fct):
        forums_created = {}
        dataframes = get_data(fct)
        from IPython.terminal.debugger import set_trace;set_trace()
        df = dataframes['df_by_timestamp']
        forums_created['num_rows'] = df.shape[0]
        forums_created['column_name'] = _(u'Forums Created')
        if forums_created['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_forums_created',
                                           'Forums Created')
            forums_created['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            forums_created['events_chart'] = ()
        
        if forums_created['num_rows'] == 1:
            forums_created['tuples'] = build_event_table_data(df)
        else:
            forums_created['tuples'] = ()
        return forums_created

 