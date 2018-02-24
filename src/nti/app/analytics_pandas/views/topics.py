#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import shutil
import base64
import tempfile

from pyramid.view import view_config

from reportlab.lib.colors import PCMYKColor

from nti.analytics_pandas.analysis import TopicsCreationTimeseries

from nti.analytics_pandas.analysis.common import get_data

from nti.app.analytics_pandas.views import MessageFactory as _

from nti.app.analytics_pandas.model import TopicsTimeseriesContext

from nti.app.analytics_pandas.views.commons import iternamedtuples
from nti.app.analytics_pandas.views.commons import get_course_names

from nti.app.analytics_pandas.views.mixins import AbstractReportView

from nti.app.analytics_pandas.charts.line_chart import TimeSeriesChart

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
        df_column_list = ['date', 'number_of_unique_users', 'number_of_events', 'ratio']
        topics_created['tuples'] = iternamedtuples(dataframes['df_by_timestamp'].astype(str), df_column_list)
        topics_created['ratio'] = dataframes['df_by_timestamp'].ratio.values.tolist()
        topics_created['date_of_events'] = dataframes['df_by_timestamp'].timestamp_period.values.tolist()
        topics_created['number_of_events'] = dataframes['df_by_timestamp'].number_of_topics_created.values.tolist()
        topics_created['number_of_unique_users'] = dataframes['df_by_timestamp'].number_of_unique_users.values.tolist()
        
        ##for sample 
        ##todo : replace chart data with topics data
        chart_data = [[(19010706, 3.3900000000000001), (19010806, 3.29), (19010906, 3.2999999999999998), (19011006, 3.29), (19011106, 3.3399999999999999), (19011206, 3.4100000000000001), (19020107, 3.3700000000000001), (19020207, 3.3700000000000001), (19020307, 3.3700000000000001), (19020407, 3.5), (19020507, 3.6200000000000001), (19020607, 3.46), (19020707, 3.3900000000000001)], [(19010706, 3.2000000000000002), (19010806, 3.1200000000000001), (19010906, 3.1400000000000001), (19011006, 3.1400000000000001), (19011106, 3.1699999999999999), (19011206, 3.23), (19020107, 3.1899999999999999), (19020207, 3.2000000000000002), (19020307, 3.1899999999999999), (19020407, 3.3100000000000001), (19020507, 3.4300000000000002), (19020607, 3.29), (19020707, 3.2200000000000002)]]
        legend = [(PCMYKColor(0,100,100,40,alpha=100), 'Bovis Homes'), (PCMYKColor(100,0,90,50,alpha=100), 'HSBC Holdings')]
        chart = TimeSeriesChart(data=chart_data, legend_color_name_pairs=legend)
        #chart_base64 = base64.b64encode(chart.asString('png'))
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        with temp_file as fp:
            fp.write(chart.asString('png'))
            fp.seek(0)
            topics_created['events_chart'] = temp_file.name
        return topics_created
