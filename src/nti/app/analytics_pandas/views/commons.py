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

from collections import Mapping
from collections import namedtuple

from contextlib import contextmanager

from matplotlib import pyplot as plt

from z3c.rml import rml2pdf

from nti.analytics_pandas.queries import QueryCourses

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
    new_list = [None]*(len(list1) + len(list2))
    new_list[::2] = list1
    new_list[1::2] = list2
    return new_list

def iternamedtuples(df):
    """
    convert a dataframe to a list of namedTuples
    """
    df.columns = ['date', 'number_of_events', 'number_of_unique_users', 'ratio']
    Row = namedtuple('Row', df.columns)
    for row in df.itertuples():
        yield Row(*row[1:])
