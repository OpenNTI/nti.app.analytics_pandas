#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.view import view_config

from nti.analytics_pandas.analysis import TopicViewsTimeseries
from nti.analytics_pandas.analysis import TopicLikesTimeseries
from nti.analytics_pandas.analysis import TopicsCreationTimeseries
from nti.analytics_pandas.analysis import TopicFavoritesTimeseries

from nti.analytics_pandas.analysis.common import get_data

from nti.app.analytics_pandas.model import TopicsTimeseriesContext

from nti.app.analytics_pandas.views import MessageFactory as _

from nti.app.analytics_pandas.views.commons import get_course_names
from nti.app.analytics_pandas.views.commons import build_event_table_data
from nti.app.analytics_pandas.views.commons import build_event_chart_data
from nti.app.analytics_pandas.views.commons import save_chart_to_temporary_file
from nti.app.analytics_pandas.views.commons import build_event_grouped_table_data
from nti.app.analytics_pandas.views.commons import build_event_grouped_chart_data

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
        from IPython.terminal.debugger import set_trace
        set_trace()
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

        data = {}
        tct = TopicsCreationTimeseries(self.db.session,
                                       self.report.start_date,
                                       self.report.end_date,
                                       self.report.courses or (),
                                       period=self.report.period)

        if not tct.dataframe.empty:
            self.options['has_topics_created_data'] = True
            data['topics_created'] = self.build_topic_creation_data(tct)

        tvt = TopicViewsTimeseries(self.db.session,
                                   self.report.start_date,
                                   self.report.end_date,
                                   self.report.courses or (),
                                   period=self.report.period)
        if not tvt.dataframe.empty:
            self.options['has_topic_views_data'] = True
            data['topics_viewed'] = self.build_topic_view_data(tvt)

        tlt = TopicLikesTimeseries(self.db.session,
                                   self.report.start_date,
                                   self.report.end_date,
                                   self.report.courses or (),
                                   period=self.report.period)
        if not tlt.dataframe.empty:
            self.options['has_topic_likes_data'] = True
            data['topics_liked'] = self.build_topic_like_data(tlt)

        tft = TopicFavoritesTimeseries(self.db.session,
                                       self.report.start_date,
                                       self.report.end_date,
                                       self.report.courses or (),
                                       period=self.report.period)
        if not tft.dataframe.empty:
            self.options['has_topic_favorites_data'] = True
            data['topics_favorite'] = self.build_topic_favorite_data(tft)

        self._build_data(data)
        return self.options

    def build_topic_creation_data(self, tct):
        topics_created = {}
        dataframes = get_data(tct)

        # Building table data
        topics_created['tuples'] = build_event_table_data(
            dataframes['df_by_timestamp'])
        topics_created['column_name'] = u'Topics Created'

        # Building chart Data
        chart = build_event_chart_data(dataframes['df_by_timestamp'],
                                       'number_of_topics_created',
                                       'Topics Created')
        topics_created['events_chart'] = save_chart_to_temporary_file(chart)
        
        #Building chart grouped by enrollment type
        if not dataframes['df_per_enrollment_type'].empty:
            self.build_topic_created_by_enrollment_type(dataframes['df_per_enrollment_type'], topics_created)
            self.options['has_topics_created_per_enrollment_types'] = True

        return topics_created

    def build_topic_created_by_enrollment_type(self, df, topics_created):
        columns = ['timestamp_period', 'enrollment_type', 'number_of_topics_created']
        new_df = df[columns]
        
        #building table data
        topics_created['tuples_enrollment_type'] = build_event_grouped_table_data(new_df)
        topics_created['enrollment_col'] = 'Enrollment Type'

        #building chart
        chart = build_event_grouped_chart_data(new_df, 'enrollment_type')
        topics_created['by_enrollment_chart'] = save_chart_to_temporary_file(chart)

    def build_topic_view_data(self, tvt):
        topics_viewed = {}
        dataframes = get_data(tvt)
        # Building table data
        topics_viewed['tuples'] = build_event_table_data(dataframes['df_by_timestamp'])
        topics_viewed['column_name'] = u'Topics Viewed'

        # Building chart Data
        chart = build_event_chart_data(dataframes['df_by_timestamp'],
                                       'number_of_topics_viewed',
                                       'Topics Viewed')
        topics_viewed['events_chart'] = save_chart_to_temporary_file(chart)
        return topics_viewed

    def build_topic_like_data(self, tlt):
        topics_liked = {}
        dataframes = get_data(tlt)
        # Building table data
        topics_liked['tuples'] = build_event_table_data(dataframes['df_by_timestamp'])
        topics_liked['column_name'] = u'Topics Liked'

        # Building chart Data
        chart = build_event_chart_data(dataframes['df_by_timestamp'],
                                       'number_of_topic_likes',
                                       'Topics Liked')
        topics_liked['events_chart'] = save_chart_to_temporary_file(chart)
        return topics_liked

    def build_topic_favorite_data(self, tft):
        topics_favorite = {}
        dataframes = get_data(tft)
        # Building table data
        topics_favorite['tuples'] = build_event_table_data(dataframes['df_by_timestamp'])
        topics_favorite['column_name'] = u'Topics Favorite'

        # Building chart Data
        chart = build_event_chart_data(dataframes['df_by_timestamp'],
                                       'number_of_topic_favorites',
                                       'Topics Favorite')
        topics_favorite['events_chart'] = save_chart_to_temporary_file(chart)
        return topics_favorite
