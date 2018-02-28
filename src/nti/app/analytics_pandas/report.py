#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from nti.app.analytics_pandas.interfaces import IPandasReport

from nti.app.analytics_pandas.interfaces import IPandasReportContext

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IPandasReportContext)
class PandasReportContext(SchemaConfigured):
    createDirectFieldProperties(IPandasReportContext)


@interface.implementer(IPandasReport)
class PandasReport(SchemaConfigured):
    createDirectFieldProperties(IPandasReport)

    # pylint: disable=unused-argument
    def __init__(self, *unused_args, **kwargs):
        # NOTE: Must ignore args
        SchemaConfigured.__init__(self, **kwargs)
