#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os

from ..report import Report
from ..report import process_args
from ..report import setup_configs
from ..report import configure_config

from ..views import SocialTimeseriesContext
from ..views import SocialTimeseriesReportView

def main():
	# Parse command line args
	args = process_args(social=True)

	setup_configs()
	configure_config()

	# Create the output directory if it does not exist
	if not os.path.exists(args['output']):
		os.mkdir(args['output'])

	filepath = '%s/social.pdf' % (args['output'])

	report_generator = Report(Context=SocialTimeseriesContext,
							  View=SocialTimeseriesReportView,
							  start_date=args['start_date'],
							  end_date=args['end_date'],
							  courses=False,
						 	  period_breaks=args['period_breaks'],
						 	  minor_period_breaks=args['minor_period_breaks'],
						 	  theme_seaborn_=args['theme_seaborn'],
						 	  filepath=filepath,
						 	  period=args['period'])
	report = report_generator.build()
	return report

if __name__ == '__main__':  # pragma: no cover
	main()
