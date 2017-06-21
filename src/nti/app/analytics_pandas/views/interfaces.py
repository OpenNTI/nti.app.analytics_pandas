#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.contenttypes.reports.interfaces import IReportContext

"""
    Interfaces for tagging contexts onto an IPandasReport
"""

class IAssessmentsEventsTimeseriesContext(IReportContext):
    pass
    
class IBookmarksTimeseriesContext(IReportContext):
    pass

class IEnrollmentTimeseriesContext(IReportContext):
    pass

class IForumsTimeseriesContext(IReportContext):
    pass

class IHighlightsTimeseriesContext(IReportContext):
    pass

class INoteEventsTimeseriesContext(IReportContext):
    pass

class IResourceViewsTimeseriesContext(IReportContext):
    pass

class ISocialTimeseriesContext(IReportContext):
    pass

class ITopicsTimeseriesContext(IReportContext):
    pass

class IVideosTimeseriesContext(IReportContext):
    pass
