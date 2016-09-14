#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .. import MessageFactory as _

import pytz
import textwrap
from datetime import datetime

from zope import interface

from z3c.pagelet.browser import BrowserPagelet

from ..interfaces import IPDFReportView

def adjust_date(date):
	"""
	Takes a date and returns a timezoned datetime
	"""
	utc_date = pytz.utc.localize(date)
	cst_tz = pytz.timezone('US/Central')
	return utc_date.astimezone(cst_tz)

def adjust_timestamp(timestamp):
	"""
	Takes a timestamp and returns a timezoned datetime
	"""
	date = datetime.utcfromtimestamp(timestamp)
	return adjust_date(date)

def format_datetime(local_date):
	"""
	Returns a string formatted datetime object
	"""
	return local_date.strftime("%Y-%m-%d %H:%M")

@interface.implementer(IPDFReportView)
class AbstractReportView(BrowserPagelet):

	def __init__(self, context=None, request=None):
		BrowserPagelet.__init__(self, context, request)
		self.options = {}
			
	@property
	def filename(self):
		return 'report.pdf'

	@property
	def report_title(self):
		return _('Report')

	def generate_footer(self):
		date = adjust_date(datetime.utcnow())
		date = date.strftime('%b %d, %Y %I:%M %p')
		title = self.report_title
		return "%s %s" % (title, date)

	def wrap_text(self, text, size):
		return textwrap.fill(text, size)
