#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import sys

from nti.app.analytics_pandas.reports.model import ResourceViewsTimeseriesContext

from nti.app.analytics_pandas.reports.report import Report
from nti.app.analytics_pandas.reports.report import process_args
from nti.app.analytics_pandas.reports.report import setup_configs
from nti.app.analytics_pandas.reports.report import configure_config

from nti.app.analytics_pandas.views.resource_views import ResourceViewsTimeseriesReportView

from nti.dataserver.utils import run_with_dataserver

from nti.dataserver.utils.base_script import create_context

logger = __import__('logging').getLogger(__name__)


def _process_report(args):
    # Create the output directory if it does not exist
    if not os.path.exists(args['output']):
        os.mkdir(args['output'])
        
    filepath = '%s/resource_views.pdf' % (args['output'])
    report_generator = Report(Context=ResourceViewsTimeseriesContext,
                              View=ResourceViewsTimeseriesReportView,
                              start_date=args['start_date'],
                              end_date=args['end_date'],
                              courses=args['courses'],
                              period_breaks=args['period_breaks'],
                              minor_period_breaks=args['minor_period_breaks'],
                              theme_bw_=args['theme_bw'],
                              filepath=filepath,
                              period=args['period'])
    report_generator.build()


def main():
    args = process_args()

    setup_configs()
    configure_config()

    env_dir = os.getenv('DATASERVER_DIR')
    if not env_dir or not os.path.exists(env_dir) and not os.path.isdir(env_dir):
        raise IOError("Invalid dataserver environment root directory")

    conf_packages = ('nti.appserver',)
    context = create_context(env_dir, with_library=False)
    run_with_dataserver(environment_dir=env_dir,
                        verbose=True,
                        xmlconfig_packages=conf_packages,
                        context=context,
                        minimal_ds=True,
                        function=lambda: _process_report(args))
    sys.exit(0)


if __name__ == '__main__':  # pragma: no cover
    main()
