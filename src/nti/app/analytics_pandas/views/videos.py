#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.view import view_config

from nti.analytics_pandas.analysis import VideoEventsTimeseries

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

@view_config(name="VideosReport")
class VideosTimeseriesReportView(AbstractReportView):

    @property
    def report_title(self):
        return _(u'Video Events Report')

    def _build_data(self, data=_('sample videos report')):
        keys = self.options.keys()
        if 'has_video_events_data' not in keys:
            self.options['has_video_events_data'] = False
            self.options['has_videos_watched'] = False
            self.options['has_videos_skipped'] = False
        self.options['data'] = data
        return self.options

    def __call__(self):
        values = self.readInput()
        if "MimeType" not in values.keys():
            values["MimeType"] = 'application/vnd.nextthought.reports.videoeventstimeseriescontext'
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
            vet = VideoEventsTimeseries(self.db.session,
                                        self.options['start_date'],
                                        self.options['end_date'],
                                        self.options['course_ids'] or (),
                                        period=self.options['period'])
            if not vet.dataframe.empty:
                self.options['has_video_events_data'] = True
                data['video_events'] = self.build_video_events_report(vet)
        self._build_data(data)
        return self.options

    def build_video_events_report(self, vet):
        video_events = {}
        self.build_video_event_types(vet, video_events)
        self.build_videos_watched_data(vet, video_events)
        self.build_videos_skipped_data(vet, video_events)
        return video_events

    def build_video_event_types(self, vet, video_events):
        df = vet.analyze_video_events_types()
        if df.empty:
            return 
        df = reset_dataframe_(df)
        columns = ['timestamp_period', 'video_event_type',
                   'number_of_video_events']
        df = df[columns]
        df['timestamp_period'] = df['timestamp_period'].astype(str)
        timestamp_num = len(df['timestamp_period'].unique())
        video_events['num_rows_video_event_type'] = df.shape[0]
        
        if video_events['num_rows_video_event_type'] > 1 and timestamp_num > 1:
            chart = build_event_grouped_chart_data(df, 'video_event_type')
            video_events['by_video_event_type_chart'] = save_chart_to_temporary_file(chart)
        else:
            video_events['by_video_event_type_chart'] = False
            
        if video_events['num_rows_video_event_type'] == 1 or timestamp_num == 1:
            video_events['tuples_video_event_type'] = build_event_grouped_table_data(df)
            video_events['video_event_col'] = 'Video Events Type'
        else:
            video_events['tuples_video_event_type'] = False

    def build_videos_watched_data(self, vet, video_events):
        df = vet.analyze_video_events(video_event_type=u'WATCH')
        df = reset_dataframe_(df)
        if df.empty:
            self.options['has_videos_watched'] = False
            return
        self.options['has_videos_watched'] = True
        video_events['num_rows'] = df.shape[0]
        video_events['column_name'] = _(u'Videos Watched')
        if video_events['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_video_events',
                                           'Videos Watched')
            video_events['events_chart'] = save_chart_to_temporary_file(chart)
        else:
            video_events['events_chart'] = ()
        
        if video_events['num_rows'] == 1:
            video_events['tuples'] = build_event_table_data(df)
        else:
            video_events['tuples'] = ()

        self.build_videos_watched_by_enrollment_type_data(vet, video_events)

    def build_videos_skipped_data(self, vet, video_events):
        df = vet.analyze_video_events(video_event_type=u'SKIP')
        df = reset_dataframe_(df)
        if df.empty:
            self.options['has_videos_skipped'] = False
            return
        self.options['has_videos_skipped'] = True
        video_events['num_rows_skip'] = df.shape[0]
        video_events['column_name_skip'] = _(u'Videos Skipped')
        if video_events['num_rows'] > 1:
            chart = build_event_chart_data(df,
                                           'number_of_video_events',
                                           'Videos Skipped')
            video_events['events_chart_skip'] = save_chart_to_temporary_file(chart)
        else:
            video_events['events_chart_skip'] = ()
        
        if video_events['num_rows_skip'] == 1:
            video_events['tuples_skip'] = build_event_table_data(df)
        else:
            video_events['tuples_skip'] = ()

    def build_videos_watched_by_enrollment_type_data(self, vet, video_events):
        df = vet.analyze_video_events_enrollment_types(video_event_type='WATCH')
        df = reset_dataframe_(df)
        if df.empty:
            self.options['has_videos_watched_per_enrollment_types'] = False
            return
        self.options['has_videos_watched_per_enrollment_types'] = True
        columns = ['timestamp_period', 'enrollment_type',
                   'number_of_video_events']
        df = df[columns]
        videos_watched = {}
        build_events_data_by_enrollment_type(df, videos_watched)
        video_events['videos_watched'] = videos_watched
