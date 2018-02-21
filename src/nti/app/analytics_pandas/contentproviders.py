#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from zope.contentprovider.interfaces import IContentProvider

from zope.contentprovider.provider import ContentProviderBase

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IContentProvider)
class DummyContentProvider(ContentProviderBase):

    def render(self, *unused_args, **unused_kwargs):
        return u"<tr><td/></tr>"
