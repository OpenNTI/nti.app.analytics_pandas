#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RML content providers.

.. $Id: contentproviders.py 73928 2015-10-01 16:16:17Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from zope.contentprovider.interfaces import IContentProvider
from zope.contentprovider.provider import ContentProviderBase

@interface.implementer(IContentProvider)
class DummyContentProvider(ContentProviderBase):

	def render(self, *args, **kwargs):
		return "<tr><td/></tr>"
