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
        self.options['courses'] = values['courses']
        course_names = get_course_names(self.db.session,
                                        self.options['courses'] or ())
        self.options['course_names'] = ", ".join(map(str, course_names or ()))
        self.options['start_date'] = values['start_date']
        self.options['end_date'] = values['end_date']
        if 'period' in values.keys():
            self.options['period'] = values['period']
        else:
            self.options['period'] = u'daily'

        data = {}
        tct = TopicsCreationTimeseries(self.db.session,
                                       self.options['start_date'],
                                       self.options['end_date'],
                                       self.options['courses'] or (),
                                       period=self.options['period'])

        if not tct.dataframe.empty:
            self.options['has_topics_created_data'] = True
            data['topics_created'] = self.build_topic_creation_data(tct)

        tvt = TopicViewsTimeseries(self.db.session,
                                   self.options['start_date'],
                                   self.options['end_date'],
                                   self.options['courses'] or (),
                                   period=self.options['period'])
        if not tvt.dataframe.empty:
            self.options['has_topic_views_data'] = True
            data['topics_viewed'] = self.build_topic_view_data(tvt)

        tlt = TopicLikesTimeseries(self.db.session,
                                   self.options['start_date'],
                                   self.options['end_date'],
                                   self.options['courses'] or (),
                                   period=self.options['period'])
        if not tlt.dataframe.empty:
            self.options['has_topic_likes_data'] = True
            data['topics_liked'] = self.build_topic_like_data(tlt)

        tft = TopicFavoritesTimeseries(self.db.session,
                                       self.options['start_date'],
                                       self.options['end_date'],
                                       self.options['courses'] or (),
                                       period=self.options['period'])
        if not tft.dataframe.empty:
            self.options['has_topic_favorites_data'] = True
            data['topics_favorite'] = self.build_topic_favorite_data(tft)

        self._build_data(data)
        return self.options

    def build_topic_creation_data(self, tct):
        topics_created = {}
        dataframes = get_data(tct)
        topics_created['num_rows'] = dataframes['df_by_timestamp'].shape[0]

        # Building table data
        topics_created['tuples'] = build_event_table_data(
            dataframes['df_by_timestamp'])
        topics_created['column_name'] = u'Topics Created'

        # Building chart Data
        if topics_created['num_rows'] > 1:
            chart = build_event_chart_data(dataframes['df_by_timestamp'],
                                       'number_of_topics_created',
                                       'Topics Created')
            topics_created['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            topics_created['events_chart'] = False
        
        #Building table and chart grouped by enrollment type
        if not dataframes['df_per_enrollment_type'].empty:
            self.options['has_topics_created_per_enrollment_types'] = True
            self.build_topic_created_by_enrollment_type(dataframes['df_per_enrollment_type'], topics_created)

        #Building table and chart grouped by device type
        if not dataframes['df_per_device_types'].empty:
            self.options['has_topics_created_per_device_types'] = True
            self.build_topic_created_by_device_type(dataframes['df_per_device_types'], topics_created)
        
        return topics_created

    def build_topic_created_by_enrollment_type(self, df, topics_created):
        columns = ['timestamp_period', 'enrollment_type', 'number_of_topics_created']
        new_df = df[columns]
        topics_created['num_rows_enrollment'] = new_df.shape[0]
        
        #building table data
        topics_created['tuples_enrollment_type'] = build_event_grouped_table_data(new_df)
        topics_created['enrollment_col'] = 'Enrollment Type'

        #building chart
        if topics_created['num_rows_enrollment'] > 1:
            chart = build_event_grouped_chart_data(new_df, 'enrollment_type')
            topics_created['by_enrollment_chart'] = save_chart_to_temporary_file(chart)

    def build_topic_created_by_device_type(self, df, topics_created):
        columns = ['timestamp_period', 'device_type', 'number_of_topics_created']
        new_df = df[columns]
        topics_created['tuples_device_type'] = build_event_grouped_table_data(new_df)
        topics_created['device_col'] = 'Device Type'

        topics_created['num_rows_device'] = new_df.shape[0]
        if topics_created['num_rows_device'] > 1:
            chart = build_event_grouped_chart_data(new_df, 'device_type')
            topics_created['by_device_chart'] = save_chart_to_temporary_file(chart)

    def build_topic_view_data(self, tvt):
        topics_viewed = {}
        dataframes = get_data(tvt)
        topics_viewed['num_rows'] = dataframes['df_by_timestamp'].shape[0]
        # Building table data
        topics_viewed['tuples'] = build_event_table_data(dataframes['df_by_timestamp'])
        topics_viewed['column_name'] = u'Topics Viewed'

        # Building chart Data
        if topics_viewed['num_rows'] > 1:
            chart = build_event_chart_data(dataframes['df_by_timestamp'],
                                           'number_of_topics_viewed',
                                           'Topics Viewed')
            topics_viewed['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            topics_viewed['events_chart'] = False
        return topics_viewed

    def build_topic_like_data(self, tlt):
        topics_liked = {}
        dataframes = get_data(tlt)
        topics_liked['num_rows'] = dataframes['df_by_timestamp'].shape[0]

        # Building table data
        topics_liked['tuples'] = build_event_table_data(dataframes['df_by_timestamp'])
        topics_liked['column_name'] = u'Topics Liked'

        # Building chart Data
        if topics_liked['num_rows'] > 1:
            chart = build_event_chart_data(dataframes['df_by_timestamp'],
                                           'number_of_topic_likes',
                                           'Topics Liked')
            topics_liked['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            topics_liked['events_chart'] = False
        return topics_liked

    def build_topic_favorite_data(self, tft):
        topics_favorite = {}
        dataframes = get_data(tft)
        topics_favorite['num_rows'] = dataframes['df_by_timestamp'].shape[0]
        # Building table data
        topics_favorite['tuples'] = build_event_table_data(dataframes['df_by_timestamp'])
        topics_favorite['column_name'] = u'Topics Favorite'

        # Building chart Data
        if topics_favorite['num_rows'] > 1:
            chart = build_event_chart_data(dataframes['df_by_timestamp'],
                                           'number_of_topic_favorites',
                                           'Topics Favorite')
            topics_favorite['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            topics_favorite['events_chart'] = False
        return topics_favorite
