#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import six
import shutil
import tempfile
import datetime as DT
from collections import Mapping
from collections import namedtuple

import numpy as np

from z3c.rml import rml2pdf

from nti.analytics_pandas.queries import QueryCourses

from nti.app.analytics_pandas import MessageFactory as _

from nti.app.analytics_pandas.charts.colors import color02
from nti.app.analytics_pandas.charts.colors import three_lines_colors

from nti.app.analytics_pandas.charts.line_chart import TimeSeriesSimpleChart
from nti.app.analytics_pandas.charts.line_chart import TimeSeriesGroupedChart

logger = __import__('logging').getLogger(__name__)


def get_default_start_end_date():
    end_date = DT.date.today()
    start_date = end_date - DT.timedelta(days=7)
    end_date = end_date.strftime("%Y-%m-%d")
    start_date = start_date.strftime("%Y-%m-%d")
    return start_date, end_date


def add_one_more_day(end_date):
    # since the query exclude the end date then we need to add one more day to
    # end date
    if isinstance(end_date, six.string_types):
        end_date = DT.datetime.strptime(end_date, "%Y-%m-%d") + DT.timedelta(days=1)
        end_date = end_date.strftime("%Y-%m-%d")
    return end_date


def get_course_names(session, courses_id):
    qc = QueryCourses(session)
    df = qc.get_context_name(courses_id)
    course_names = ''
    if not df.empty:
        course_names = df['context_name'].tolist()
    return course_names


def get_course_id_and_name_given_ntiid(session, course_ntiid):
    qc = QueryCourses(session)
    df = qc.get_course_given_ntiid(course_ntiid)

    course_ids = ()
    course_names = ()
    if not df.empty:
        course_ids = df['context_id'].tolist()
        course_names = df['context_name'].tolist()
    return course_ids, course_names


def create_pdf_file_from_rml(rml, filepath):
    pdf_stream = rml2pdf.parseString(rml)
    try:
        pdf_stream.seek(0)
        with open(filepath, 'w') as fp:
            shutil.copyfileobj(pdf_stream, fp)
    finally:
        pdf_stream.close()


def cleanup_temporary_file(data):
    if isinstance(data, six.string_types):
        if os.path.isfile(data):
            os.unlink(data)
    elif isinstance(data, Mapping):
        for value in data.values():
            cleanup_temporary_file(value)


def series_to_string(series1, series2):
    list1 = series1.values.tolist()
    list2 = series2.values.tolist()
    new_list = alternate_lists(list1, list2)
    return u' '.join(str(item) for item in new_list)


def alternate_lists(list1, list2):
    """
    Combine two pandas series into a new list whose even-index values come from the first list 
    and whose odd-index values come from the second list.
    """
    new_list = [None] * (len(list1) + len(list2))
    new_list[::2] = list1
    new_list[1::2] = list2
    return new_list


def iternamedtuples(df, column_list):
    """
    convert a dataframe to namedTuples
    """
    df.columns = column_list
    Row = namedtuple('Row', df.columns)
    for row in df.itertuples():
        yield Row(*row[1:])


def save_chart_to_temporary_file(chart):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    with temp_file as fp:
        fp.write(chart.asString('png'))
        fp.seek(0)
        fname = temp_file.name
        return fname


def build_timeseries_chart(df, col_name_alias):
    events = [tuple(i) for i in df.values]
    legend = [(color02, col_name_alias)]
    chart_data = [events]
    chart = TimeSeriesSimpleChart(data=chart_data,
                                  legend_color_name_pairs=legend)
    return chart


def build_event_chart_data(df, event_unique_col_name, col_name_alias,
                           unused_legend_colors=three_lines_colors):
    # Building line chart
    events_df = df[['timestamp_period', event_unique_col_name]]
    events = [tuple(i) for i in events_df.values]
    users_df = df[['timestamp_period', 'number_of_unique_users']]
    users = [tuple(i) for i in users_df.values]
    ratio_df = df[['timestamp_period', 'ratio']]
    ratio = [tuple(i) for i in ratio_df.values]
    chart_data = [events, users, ratio]
    legend = [
        (three_lines_colors[0], col_name_alias),
        (three_lines_colors[1], _(u'Unique Users')),
        (three_lines_colors[2], _(u'Ratio'))
    ]
    chart = TimeSeriesSimpleChart(data=chart_data,
                                  legend_color_name_pairs=legend)
    return chart


def build_event_table_data(df, column_list=('date', 'number_of_unique_users', 'number_of_events', 'ratio')):
    if 'ratio' in df.columns:
        df = df.round({'ratio': 2})
    tuples = iternamedtuples(df.astype(str), column_list)
    return tuples


def build_event_grouped_table_data(df, column_list=('date', 'group_type', 'number_of_events')):
    if 'timestamp_period' in df.columns:
        df['timestamp_period'] = df['timestamp_period'].astype(str)
    tuples = iternamedtuples(df, column_list)
    return tuples


def build_event_grouped_chart_data(df, group_col):
    # Building grouped line chart
    chart_data, groups = extract_group_dataframe(df, group_col)
    chart = TimeSeriesGroupedChart(data=chart_data, group_legend=groups)
    return chart


def build_events_data_by_device_type(df, events_dict):
    events_dict['num_rows_device'] = df.shape[0]
    timestamp_num = len(np.unique(df['timestamp_period'].values.ravel()))
    if events_dict['num_rows_device'] > 1 and timestamp_num > 1:
        chart = build_event_grouped_chart_data(df, 'device_type')
        events_dict['by_device_chart'] = save_chart_to_temporary_file(chart)
    else:
        events_dict['by_device_chart'] = ()

    if events_dict['num_rows_device'] == 1 or timestamp_num == 1:
        events_dict['tuples_device_type'] = build_event_grouped_table_data(df)
        events_dict['device_col'] = _(u'Device Type')
    else:
        events_dict['tuples_device_type'] = ()
    return events_dict


def build_events_data_by_enrollment_type(df, events_dict):
    events_dict['num_rows_enrollment'] = df.shape[0]
    timestamp_num = len(np.unique(df['timestamp_period'].values.ravel()))
    if events_dict['num_rows_enrollment'] > 1 and timestamp_num > 1:
        chart = build_event_grouped_chart_data(df, 'enrollment_type')
        events_dict['by_enrollment_chart'] = save_chart_to_temporary_file(
            chart)
    else:
        events_dict['by_enrollment_chart'] = ()

    if events_dict['num_rows_enrollment'] == 1 or timestamp_num == 1:
        events_dict['tuples_enrollment_type'] = build_event_grouped_table_data(
            df)
        events_dict['enrollment_col'] = _(u'Enrollment Type')
    else:
        events_dict['tuples_enrollment_type'] = ()


def build_events_data_by_resource_type(df, events_dict):
    events_dict['num_rows_resource'] = df.shape[0]
    timestamp_num = len(np.unique(df['timestamp_period'].values.ravel()))
    if events_dict['num_rows_resource'] > 1 and timestamp_num > 1:
        chart = build_event_grouped_chart_data(df, 'resource_type')
        events_dict['by_resource_chart'] = save_chart_to_temporary_file(chart)
    else:
        events_dict['by_resource_chart'] = ()

    if events_dict['num_rows_resource'] == 1 or timestamp_num == 1:
        events_dict['tuples_resource_type'] = build_event_grouped_table_data(df)
        events_dict['resource_col'] = _(u'Resource Type')
    else:
        events_dict['tuples_resource_type'] = ()


def build_events_data_by_sharing_type(df, events_dict):
    events_dict['num_rows_sharing'] = df.shape[0]
    timestamp_num = len(np.unique(df['timestamp_period'].values.ravel()))
    if events_dict['num_rows_sharing'] > 1 and timestamp_num > 1:
        chart = build_event_grouped_chart_data(df, 'sharing')
        events_dict['by_sharing_chart'] = save_chart_to_temporary_file(chart)
    else:
        events_dict['by_sharing_chart'] = ()

    if events_dict['num_rows_sharing'] == 1 or timestamp_num == 1:
        events_dict['tuples_sharing_type'] = build_event_grouped_table_data(df)
        events_dict['sharing_col'] = _(u'Sharing Type')
    else:
        events_dict['tuples_sharing_type'] = ()


def extract_group_dataframe(df, group_col):
    """
    Given a column name, extract dataframe into a data list.
    'data' list consist of list of tuple 
    The number of item in the data list would be the same with the number of 
    unique values in the given column name
    """
    groups = df[group_col].unique()
    data = []
    for group in groups:
        temp_df = df.loc[df[group_col] == group]
        temp_df = temp_df.loc[:, temp_df.columns != group_col]
        tuples = [tuple(i) for i in temp_df.values]
        data.append(tuples)
    return data, groups
