#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from nti.app.analytics_pandas.interfaces import IForumsTimeseriesContext
from nti.app.analytics_pandas.interfaces import ISocialTimeseriesContext
from nti.app.analytics_pandas.interfaces import ITopicsTimeseriesContext
from nti.app.analytics_pandas.interfaces import IVideosTimeseriesContext
from nti.app.analytics_pandas.interfaces import IBookmarksTimeseriesContext
from nti.app.analytics_pandas.interfaces import IEnrollmentTimeseriesContext
from nti.app.analytics_pandas.interfaces import IHighlightsTimeseriesContext
from nti.app.analytics_pandas.interfaces import INoteEventsTimeseriesContext
from nti.app.analytics_pandas.interfaces import IResourceViewsTimeseriesContext
from nti.app.analytics_pandas.interfaces import IAssessmentsEventsTimeseriesContext

from nti.app.analytics_pandas.report import PandasReportContext

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IAssessmentsEventsTimeseriesContext)
class AssessmentsEventsTimeseriesContext(PandasReportContext):
    mimeType = mime_type = 'application/vnd.nextthought.analytics.assessmentseventstimeseriesContext'


@interface.implementer(IBookmarksTimeseriesContext)
class BookmarksTimeseriesContext(PandasReportContext):
    mimeType = mime_type = 'application/vnd.nextthought.analytics.bookmarkstimeseriescontext'


@interface.implementer(IForumsTimeseriesContext)
class ForumsTimeseriesContext(PandasReportContext):
    mimeType = mime_type = 'application/vnd.nextthought.analytics.forumstimeseriescontext'


@interface.implementer(IEnrollmentTimeseriesContext)
class EnrollmentTimeseriesContext(PandasReportContext):
    mimeType = mime_type = 'application/vnd.nextthought.analytics.enrollmenttimeseriescontext'


@interface.implementer(IHighlightsTimeseriesContext)
class HighlightsTimeseriesContext(PandasReportContext):
    mimeType = mime_type = 'application/vnd.nextthought.analytics.highlightstimeseriescontext'


@interface.implementer(INoteEventsTimeseriesContext)
class NoteEventsTimeseriesContext(PandasReportContext):
    mimeType = mime_type = 'application/vnd.nextthought.analytics.noteeventstimeseriesContext'


@interface.implementer(IResourceViewsTimeseriesContext)
class ResourceViewsTimeseriesContext(PandasReportContext):
    mimeType = mime_type = 'application/vnd.nextthought.analytics.resourceviewstimeseriesContext'


@interface.implementer(ISocialTimeseriesContext)
class SocialTimeseriesContext(PandasReportContext):
    mimeType = mime_type = 'application/vnd.nextthought.analytics.socialtimeseriesContext'


@interface.implementer(ITopicsTimeseriesContext)
class TopicsTimeseriesContext(PandasReportContext):
    mimeType = mime_type = 'application/vnd.nextthought.analytics.topicstimeseriescontext'


@interface.implementer(IVideosTimeseriesContext)
class VideosTimeseriesContext(PandasReportContext):
    mimeType = mime_type = 'application/vnd.nextthought.analytics.videostimeseriescontext'
