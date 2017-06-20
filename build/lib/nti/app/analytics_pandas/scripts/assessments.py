#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: assessments.py 115510 2017-06-19 16:21:39Z austin.graham $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os

from ..report import Report
from ..report import process_args
from ..report import setup_configs
from ..report import configure_config

from ..views import AssessmentsEventsTimeseriesContext
from ..views import AssessmentsEventsTimeseriesReportView

def main():
	# Parse command line args
	args = process_args()

	setup_configs()
	configure_config()

	# Create the output directory if it does not exist
	if not os.path.exists(args['output']):
		os.mkdir(args['output'])

	filepath = '%s/assessments.pdf' % (args['output'])

	report_generator = Report(Context=AssessmentsEventsTimeseriesContext,
							  View=AssessmentsEventsTimeseriesReportView,
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
