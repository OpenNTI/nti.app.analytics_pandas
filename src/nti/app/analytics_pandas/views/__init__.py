#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.interfaces import IRequest

from zope import interface
from zope import component

from zope.container.contained import Contained

from zope.location.interfaces import IContained

from zope.traversing.interfaces import IPathAdapter

from nti.app.analytics_pandas import MessageFactory

from nti.dataserver.interfaces import IDataserverFolder


@interface.implementer(IPathAdapter)
@component.adapter(IDataserverFolder, IRequest)
class PandasReportAdapter(Contained):

    __name__ = 'pandas_reports'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context
