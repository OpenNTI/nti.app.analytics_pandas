#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import textwrap
from datetime import datetime

import pytz

from pyramid.view import view_defaults

from zope import component
from zope import interface

from z3c.pagelet.browser import BrowserPagelet

from nti.app.analytics_pandas.interfaces import IPDFReportView

from nti.app.analytics_pandas.views import MessageFactory as _
from nti.app.analytics_pandas.views import PandasReportAdapter

from nti.app.base.abstract_views import AbstractAuthenticatedView

from nti.app.externalization.view_mixins import ModeledContentUploadRequestUtilsMixin

from nti.analytics_database.interfaces import IAnalyticsDatabase

from nti.dataserver import authorization as nauth

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

logger = __import__('logging').getLogger(__name__)


def get_analytics_db(strict=True):
    method = component.getUtility if strict else component.queryUtility
    return method(IAnalyticsDatabase)


def adjust_date(date):
    """
    Takes a date and returns a timezoned datetime
    """
    utc_date = pytz.utc.localize(date)
    cst_tz = pytz.timezone('US/Central')
    return utc_date.astimezone(cst_tz)


def adjust_timestamp(timestamp):
    """
    Takes a timestamp and returns a timezoned datetime
    """
    date = datetime.utcfromtimestamp(timestamp)
    return adjust_date(date)


def format_datetime(local_date):
    """
    Returns a string formatted datetime object
    """
    return local_date.strftime("%Y-%m-%d %H:%M")


@view_defaults(route_name='objects.generic.traversal',
               renderer="../templates/std_report_layout.rml",
               context=PandasReportAdapter,
               permission=nauth.ACT_NTI_ADMIN)
@interface.implementer(IPDFReportView)
class AbstractReportView(AbstractAuthenticatedView,
                         BrowserPagelet,
                         ModeledContentUploadRequestUtilsMixin):

    def __init__(self, context=None, request=None):
        AbstractAuthenticatedView.__init__(self, request)
        BrowserPagelet.__init__(self, context, request)
        self.db = get_analytics_db()
        self.options = {}

    @property
    def filename(self):
        return 'report.pdf'

    @property
    def report_title(self):
        return _(u'Report')

    def generate_footer(self):
        date = adjust_date(datetime.utcnow())
        date = date.strftime('%b %d, %Y %I:%M %p')
        title = self.report_title
        return u"%s %s" % (title, date)

    def wrap_text(self, text, size):
        return textwrap.fill(text, size)

    def _build_context(self, unused_context_class, params):
        return self._create_object_from_external(map_obj=params)

    def readInput(self, value=None):
        if self.request.body:
            values = super(AbstractReportView, self).readInput(value)
        else:
            values = dict(self.request.params)
        return values

    def _create_object_from_external(self, map_obj, notify=False, _exec=True):
        # find factory
        factory = find_factory_for(map_obj)
        if _exec:
            assert factory is not None, "Could not find factory for external object"
        # create and update
        result = factory()
        update_from_external_object(result, map_obj, notify=notify)
        return result
