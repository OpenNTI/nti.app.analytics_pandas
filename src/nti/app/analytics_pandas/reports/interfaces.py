#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.schema import Int

from zope.viewlet.interfaces import IViewletManager

from nti.contenttypes.reports.interfaces import IReport

from nti.schema.field import TextLine
from nti.schema.field import ListOrTuple
from nti.schema.field import Bool

class IPDFReportView(interface.Interface):
	"""
	An interface that all the reporting views
	that generate PDFs and work from the same set
	of PDF templates are expected to implement.

	In this way, we have a distinct way of registering :mod:`z3c.macro``
	definitions.
	"""

	filename = TextLine(title="The final portion of the file name, usually the view name",
						required=False,
						default="")

	report_title = TextLine(title="The title of the report.")

class IPDFReportHeaderManager(IViewletManager):
	"""
	Viewlet manager for the headers of pdf reports.
	"""


class IPandasReportContext(interface.Interface):
	"""
	Special model for a report in analytics_pandas
	"""
	start_date = TextLine(title="Start date of the report context",
                       required=False,
                       default=None)
	
	end_date = TextLine(title="End date of the report context",
                     	required=False,
                     	default=None)
	
	courses = ListOrTuple(title="Courses in this context",
                       value_type=TextLine(title="Course number"),
                       required=False,
                       default=None)
	
	period_breaks = TextLine(title="Period breaks for this context",
                          required=False,
                          default='1 week')
	
	minor_period_breaks = TextLine(title="Minor period breaks for this context",
                                required=False,
                                default='1 day')
	
	theme_bw_ = Bool(title="Theme for the report",
                    required=False,
                    default=True)

	number_of_most_active_user = Int(title="Number of most active users in this context",
                                      required=False,
                                      default=10)
	
	period = TextLine(title="Period for this context",
                   required=False,
                   default='daily')

class IPandasReport(IReport):
	"""
	An analytics_pandas report
	"""
