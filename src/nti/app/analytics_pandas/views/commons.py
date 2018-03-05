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
import atexit
import shutil
import tempfile
import numpy as np

from collections import Mapping
from collections import namedtuple

from contextlib import contextmanager

from matplotlib import pyplot as plt

from z3c.rml import rml2pdf

from nti.analytics_pandas.queries import QueryCourses

from nti.app.analytics_pandas import MessageFactory as _

from nti.app.analytics_pandas.charts.colors import three_lines_colors

from nti.app.analytics_pandas.charts.line_chart import TimeSeriesSimpleChart
from nti.app.analytics_pandas.charts.line_chart import TimeSeriesGroupedChart

from nti.analytics_pandas.utils import Plot
from nti.analytics_pandas.utils import save_plot_

logger = __import__('logging').getLogger(__name__)


def build_images_dict_from_plot_dict(plots, image_type='png', dirname=None):
    """
    proceed set of plots stored in dictionary
    """
    images = {}
    if dirname is None:
        dirname = tempfile.mkdtemp()
        atexit.register(shutil.rmtree, dirname)

    if isinstance(plots, Mapping):
        for key in plots:
            if isinstance(plots[key], Mapping):
                images[key] = build_images_dict_from_plot_dict(plots[key],
                                                               dirname=dirname,
                                                               image_type=image_type)
            elif isinstance(plots[key], (list, tuple)):
                images[key] = build_plot_images_dictionary(plots[key],
                                                           dirname=dirname,
                                                           image_type=image_type)
            elif isinstance(plots[key], Plot):
                with copy_plot_to_temporary_file(plots[key], image_type, dirname=dirname) as filename:
                    images[key] = filename
    return images


@contextmanager
def copy_plot_to_temporary_file(plot, image_type, dirname=None):
    image_file = tempfile.NamedTemporaryFile(delete=False, dir=dirname)
    try:
        plt.figure.Figure = plot.plot.draw()
        plt.savefig(image_file.name, format=image_type)
        plt.close()
    finally:
        image_file.close()
        yield image_file.name


def build_plot_images_dictionary(plots, image_type='png', dirname=None):
    images = {}
    for plot in plots:
        if isinstance(plot, Plot):
            with copy_plot_to_temporary_file(plot, image_type, dirname=dirname) as filename:
                images[plot.plot_name] = filename
    return images


def copy_plot_to_temporary_file_(plot, image_type, dirname=None):
    """
    ega: please keep this function for further reference
    """
    image = save_plot_(plot.plot, plot.plot_name, image_type)
    try:
        image_file = tempfile.NamedTemporaryFile(delete=False, dir=dirname)
        image.data.seek(0)
        shutil.copyfileobj(image.data, image_file)
    finally:
        image.data.close()
    return image_file.name


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
    df_table = df.round({'ratio': 2})
    tuples = iternamedtuples(df_table.astype(str), column_list)
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


def build_events_created_by_device_type(df, events_dict):
    events_dict['tuples_device_type'] = build_event_grouped_table_data(df)
    events_dict['device_col'] = 'Device Type'
    events_dict['num_rows_device'] = df.shape[0]
    timestamp_num = len(np.unique(df['timestamp_period'].values.ravel()))
    if events_dict['num_rows_device'] > 1 and timestamp_num > 1:
        chart = build_event_grouped_chart_data(df, 'device_type')
        events_dict['by_device_chart'] = save_chart_to_temporary_file(chart)
    else:
        events_dict['by_device_chart'] = False
    return events_dict


def build_events_created_by_enrollment_type(df, events_dict):
    events_dict['num_rows_enrollment'] = df.shape[0]
    # building table data
    events_dict['tuples_enrollment_type'] = build_event_grouped_table_data(df)
    events_dict['enrollment_col'] = 'Enrollment Type'
    timestamp_num = len(np.unique(df['timestamp_period'].values.ravel()))
    # building chart
    if events_dict['num_rows_enrollment'] > 1 and timestamp_num > 1:
        chart = build_event_grouped_chart_data(df, 'enrollment_type')
        events_dict['by_enrollment_chart'] = save_chart_to_temporary_file(chart)
    else:
        events_dict['by_enrollment_chart'] = False

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
