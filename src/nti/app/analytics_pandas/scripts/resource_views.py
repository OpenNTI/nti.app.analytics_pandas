#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os

from nti.app.analytics_pandas.reports.model import ResourceViewsTimeseriesContext

from nti.app.analytics_pandas.reports.report import Report
from nti.app.analytics_pandas.reports.report import process_args
from nti.app.analytics_pandas.reports.report import setup_configs
from nti.app.analytics_pandas.reports.report import configure_config

from nti.app.analytics_pandas.views.resource_views import ResourceViewsTimeseriesReportView

logger = __import__('logging').getLogger(__name__)


def main():
    # Parse command line args
    args = process_args()

    setup_configs()
    configure_config()

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
    report = report_generator.build()
    return report


if __name__ == '__main__':  # pragma: no cover
    main()
