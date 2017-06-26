#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from zope import interface

from nti.app.analytics_pandas.views.interfaces import IAssessmentsEventsTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import IBookmarksTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import IForumsTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import IEnrollmentTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import IHighlightsTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import INoteEventsTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import IResourceViewsTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import ISocialTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import ITopicsTimeseriesContext
from nti.app.analytics_pandas.views.interfaces import IVideosTimeseriesContext

from nti.app.analytics_pandas.reports.report import PandasReportContext


@interface.implementer(IAssessmentsEventsTimeseriesContext)
class AssessmentsEventsTimeseriesContext(PandasReportContext):

    def __init__(self, *args, **kwargs):
        super(AssessmentsEventsTimeseriesContext,self).__init__(*args,**kwargs)


@interface.implementer(IBookmarksTimeseriesContext)
class BookmarksTimeseriesContext(PandasReportContext):

    def __init__(self, *args, **kwargs):
        super(BookmarksTimeseriesContext, self).__init__(*args, **kwargs)


@interface.implementer(IForumsTimeseriesContext)
class ForumsTimeseriesContext(PandasReportContext):

    def __init__(self, *args, **kwargs):
        super(ForumsTimeseriesContext, self).__init__(*args, **kwargs)


@interface.implementer(IEnrollmentTimeseriesContext)
class EnrollmentTimeseriesContext(PandasReportContext):

    def __init__(self, *args, **kwargs):
        super(EnrollmentTimeseriesContext, self).__init__(*args, **kwargs)


@interface.implementer(IHighlightsTimeseriesContext)
class HighlightsTimeseriesContext(PandasReportContext):

    def __init__(self, *args, **kwargs):
        super(HighlightsTimeseriesContext, self).__init__(*args, **kwargs)


@interface.implementer(INoteEventsTimeseriesContext)
class NoteEventsTimeseriesContext(PandasReportContext):

    def __init__(self, *args, **kwargs):
        super(NoteEventsTimeseriesContext, self).__init__(*args, **kwargs)


@interface.implementer(IResourceViewsTimeseriesContext)
class ResourceViewsTimeseriesContext(PandasReportContext):

    def __init__(self, *args, **kwargs):
        super(ResourceViewsTimeseriesContext, self).__init__(*args, **kwargs)


@interface.implementer(ISocialTimeseriesContext)
class SocialTimeseriesContext(PandasReportContext):

    def __init__(self, *args, **kwargs):
        super(SocialTimeseriesContext, self).__init__(*args, **kwargs)


@interface.implementer(ITopicsTimeseriesContext)
class TopicsTimeseriesContext(PandasReportContext):

    def __init__(self, *args, **kwargs):
        super(TopicsTimeseriesContext, self).__init__(*args, **kwargs)


@interface.implementer(IVideosTimeseriesContext)
class VideosTimeseriesContext(PandasReportContext):

    def __init__(self, *args, **kwargs):
        super(VideosTimeseriesContext, self).__init__(*args, **kwargs)
