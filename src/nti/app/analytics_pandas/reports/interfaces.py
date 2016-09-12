#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.viewlet.interfaces import IViewletManager

from nti.schema.field import TextLine

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
