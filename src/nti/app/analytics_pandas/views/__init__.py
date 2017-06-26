#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .. import MessageFactory

from zope import interface
from zope import component
 
from zope.container.contained import Contained
 
from zope.location.interfaces import IContained
 
from zope.traversing.interfaces import IPathAdapter

from nti.dataserver.interfaces import IDataserverFolder

from pyramid.interfaces import IRequest

from zope.traversing.interfaces import IPathAdapter
 
 
@interface.implementer(IPathAdapter)
@component.adapter(IDataserverFolder, IRequest)
class PandasReportAdapter(Contained):
 
    __name__ = 'pandas_reports'
 
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context
