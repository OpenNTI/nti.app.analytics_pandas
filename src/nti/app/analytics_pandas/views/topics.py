#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.view import view_config

from nti.analytics_pandas.analysis import TopicsCreationTimeseries

from nti.analytics_pandas.analysis.common import get_data

from nti.app.analytics_pandas.views import MessageFactory as _

from nti.app.analytics_pandas.model import TopicsTimeseriesContext

from nti.app.analytics_pandas.views.commons import iternamedtuples
from nti.app.analytics_pandas.views.commons import get_course_names

from nti.app.analytics_pandas.views.mixins import AbstractReportView

logger = __import__('logging').getLogger(__name__)


@view_config(name="TopicsReport")
class TopicsTimeseriesReportView(AbstractReportView):

    @property
    def report_title(self):
        return _(u'Topics Report')

    def _build_data(self, data=_(u'sample topics related events report')):
        keys = self.options.keys()

        if 'has_topics_created_data' not in keys:
            self.options['has_topics_created_data'] = False
            self.options['has_topics_created_per_device_types'] = False
            self.options['has_topics_created_per_course_sections'] = False
            self.options['has_topics_created_per_enrollment_types'] = False

        if 'has_topic_views_data' not in keys:
            self.options['has_topic_views_data'] = False
            self.options['has_topic_views_per_course_sections'] = False
            self.options['has_topic_views_per_device_types'] = False
            self.options['has_topic_views_per_enrollment_types'] = False

        if 'has_topic_likes_data' not in keys:
            self.options['has_topic_likes_data'] = False

        if 'has_topic_favorites_data' not in keys:
            self.options['has_topic_favorites_data'] = False

        self.options['data'] = data
        return self.options

    def __call__(self):
        values = self.readInput()
        if "MimeType" not in values.keys():
            values["MimeType"] = 'application/vnd.nextthought.analytics.topicstimeseriescontext'
        # pylint: disable=attribute-defined-outside-init
        self.report = self._build_context(TopicsTimeseriesContext, values)

        course_names = get_course_names(self.db.session,
                                        self.report.courses or ())
        self.options['course_names'] = ", ".join(map(str, course_names or ()))
        self.options['start_date'] = values['start_date']
        self.options['end_date'] = values['end_date']

        tct = TopicsCreationTimeseries(self.db.session,
                                       self.report.start_date,
                                       self.report.end_date,
                                       self.report.courses or (),
                                       period=self.report.period)

        data = {}
        if not tct.dataframe.empty:
            self.options['has_topics_created_data'] = True
            data['topics_created'] = self.build_topic_creation_data(tct)
        self._build_data(data)
        return self.options

    def build_topic_creation_data(self, tct):
        topics_created = {}
        dataframes = get_data(tct)
        topics_created['tuples'] = iternamedtuples(dataframes['df_by_timestamp'])
        topics_created['ratio'] = dataframes['df_by_timestamp'].ratio.values.tolist()
        topics_created['date_of_events'] = dataframes['df_by_timestamp'].timestamp_period.values.tolist()
        topics_created['number_of_events'] = dataframes['df_by_timestamp'].number_of_topics_created.values.tolist()
        topics_created['number_of_unique_users'] = dataframes['df_by_timestamp'].number_of_unique_users.values.tolist()
        return topics_created
