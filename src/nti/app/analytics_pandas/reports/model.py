#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from nti.app.analytics_pandas.views.interfaces import IForumsTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import ISocialTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import ITopicsTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import IVideosTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import IBookmarksTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import IEnrollmentTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import IHighlightsTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import INoteEventsTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import IResourceViewsTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import IAssessmentsEventsTimeseriesContext

from nti.app.analytics_pandas.reports.report import PandasReportContext

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IAssessmentsEventsTimeseriesContext)
class AssessmentsEventsTimeseriesContext(PandasReportContext):
    pass


@interface.implementer(IBookmarksTimeseriesContext)
class BookmarksTimeseriesContext(PandasReportContext):
    pass


@interface.implementer(IForumsTimeseriesContext)
class ForumsTimeseriesContext(PandasReportContext):
    pass


@interface.implementer(IEnrollmentTimeseriesContext)
class EnrollmentTimeseriesContext(PandasReportContext):
    pass


@interface.implementer(IHighlightsTimeseriesContext)
class HighlightsTimeseriesContext(PandasReportContext):
    pass


@interface.implementer(INoteEventsTimeseriesContext)
class NoteEventsTimeseriesContext(PandasReportContext):
    pass


@interface.implementer(IResourceViewsTimeseriesContext)
class ResourceViewsTimeseriesContext(PandasReportContext):
    pass


@interface.implementer(ISocialTimeseriesContext)
class SocialTimeseriesContext(PandasReportContext):
    pass


@interface.implementer(ITopicsTimeseriesContext)
class TopicsTimeseriesContext(PandasReportContext):
    pass


@interface.implementer(IVideosTimeseriesContext)
class VideosTimeseriesContext(PandasReportContext):
    pass
