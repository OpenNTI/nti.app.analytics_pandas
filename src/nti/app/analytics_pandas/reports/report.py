#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import logging
import argparse

from zope import interface

from zope.configuration import xmlconfig, config

import nti.analytics_pandas

from nti.app.analytics_pandas.reports.interfaces import IPandasReport

from nti.app.analytics_pandas.reports.interfaces import IPandasReportContext

from nti.app.analytics_pandas.reports.z3c_zpt import ViewPageTemplateFile

from nti.app.analytics_pandas.views.commons import cleanup_temporary_file
from nti.app.analytics_pandas.views.commons import create_pdf_file_from_rml

from nti.base._compat import text_

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured

DEFAULT_FORMAT_STRING = '[%(asctime)-15s] [%(name)s] %(levelname)s: %(message)s'

logger = __import__('logging').getLogger(__name__)


def _parse_args():
    arg_parser = argparse.ArgumentParser(description="NTI Analytics")
    arg_parser.add_argument('start_date',
                            help="Report duration start date, use the format %s" % 'yyyy-mm-dd')
    arg_parser.add_argument('end_date',
                            help="Report duration end date, use the format %s" % 'yyyy-mm-dd')
    arg_parser.add_argument('-p', '--period',
                            default='daily',
                            help="Determine how the events will be aggregated. The default value is daily is %s" % "daily")
    arg_parser.add_argument('-pb', '--period_breaks',
                            default=None,
                            help="Set period breaks on generated plots. The default is %s" % "None")
    arg_parser.add_argument('-mpb', '--minor_period_breaks',
                            default=None,
                            help="Set minor period breaks on generated plots. The default is %s" % "None")
    arg_parser.add_argument('-ts', '--theme_bw',
                            default=True,
                            help="Seaborn theme for generated plots. The default it is 1 (true)")
    arg_parser.add_argument('-o', '--output',
                            default='output',
                            help="The output directory. The default is: %s" % 'output')
    return arg_parser


def _configure_logging(level='INFO'):
    nl = getattr(logging, level.upper(), None)
    nl = logging.INFO if not isinstance(nl, int) else nl
    logging.basicConfig(level=nl)
configure_logging = _configure_logging


def _setup_configs():
    _configure_logging()
setup_configs = _setup_configs


def _configure_config():
    context = config.ConfigurationMachine()
    xmlconfig.registerCommonDirectives(context)
    xmlconfig.file('configure.zcml',
                   package=nti.analytics_pandas, context=context)


configure_config = _configure_config


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def process_args(social=False):
    arg_parser = _parse_args()
    if not social:
        arg_parser.add_argument('courses',
                                help="Course/s ID. For example %s" % '1068, 1096, 1097, 1098, 1099')
    args = arg_parser.parse_args()
    args_dict = {}
    args_dict['end_date'] = text_(args.end_date)
    args_dict['start_date'] = text_(args.start_date)

    if not social:
        if ',' in args.courses:
            args_dict['courses'] = [text_(x) for x in args.courses.split(',')]
        else:
            args_dict['courses'] = [text_(x) for x in args.courses.split()]

    args_dict['period'] = args.period
    if args.period == 'daily':
        args_dict['period_breaks'] = u'1 day'
        args_dict['minor_period_breaks'] = None
    elif args.period == 'weekly':
        args_dict['period_breaks'] = u'1 week'
        args_dict['minor_period_breaks'] = None
    else:
        args_dict['period_breaks'] = text_(args.period_breaks)
        args_dict['minor_period_breaks'] = text_(args.minor_period_breaks)

    if isinstance(args.theme_bw, bool):
        args_dict['theme_bw'] = args.theme_bw
    else:
        args_dict['theme_bw'] = str2bool(args.theme_bw)

    args_dict['output'] = text_(args.output)
    return args_dict


@interface.implementer(IPandasReportContext)
class PandasReportContext(SchemaConfigured):
    createDirectFieldProperties(IPandasReportContext)


@interface.implementer(IPandasReport)
class PandasReport(SchemaConfigured):
    createDirectFieldProperties(IPandasReport)


class Report(object):

    def __init__(self, Context, View, start_date, end_date, courses,
                 period_breaks, minor_period_breaks, theme_bw_,
                 filepath, period=u'daily'):  # pylint: disable=unused-argument
        if not courses:
            self.context = Context(start_date=start_date,
                                   end_date=end_date,
                                   period_breaks=period_breaks,
                                   minor_period_breaks=minor_period_breaks,
                                   theme_bw_=theme_bw_)
        else:
            self.context = Context(start_date=start_date,
                                   end_date=end_date,
                                   courses=courses,
                                   period_breaks=period_breaks,
                                   minor_period_breaks=minor_period_breaks,
                                   theme_bw_=theme_bw_)
        self.view = View(self.context)
        self.filepath = filepath

    def std_report_layout_rml(self):
        path = os.path.join(os.path.dirname(__file__),
                            'templates/std_report_layout.rml')
        return path

    def template(self, path):
        result = ViewPageTemplateFile(path,
                                      auto_reload=(False,),
                                      debug=False)
        return result

    def build(self):
        self.view()
        path = self.std_report_layout_rml()
        system = {'view': self.view, 'context': self.context}
        rml = self.template(path).bind(self.view)(**system)
        data = self.view.options['data']
        create_pdf_file_from_rml(rml, self.filepath)
        cleanup_temporary_file(data)
