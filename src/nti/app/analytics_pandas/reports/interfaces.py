#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

from zope import interface

from zope.schema import Int

from zope.viewlet.interfaces import IViewletManager

from nti.contenttypes.reports.interfaces import IReport

from nti.schema.field import Bool
from nti.schema.field import ListOrTuple
from nti.schema.field import DecodingValidTextLine as TextLine


class IPDFReportView(interface.Interface):
    """
    An interface that all the reporting views
    that generate PDFs and work from the same set
    of PDF templates are expected to implement.

    In this way, we have a distinct way of registering :mod:`z3c.macro``
    definitions.
    """

    filename = TextLine(title=u"The final portion of the file name, usually the view name",
                        required=False,
                        default=u"")

    report_title = TextLine(title=u"The title of the report.")


class IPDFReportHeaderManager(IViewletManager):
    """
    Viewlet manager for the headers of pdf reports.
    """


class IPandasReportContext(interface.Interface):
    """
    Special model for a report in analytics_pandas
    """
    start_date = TextLine(title=u"Start date of the report context",
                          required=False,
                          default=None)

    end_date = TextLine(title=u"End date of the report context",
                        required=False,
                        default=None)

    courses = ListOrTuple(title=u"Courses in this context",
                          value_type=TextLine(title=u"Course number"),
                          required=False,
                          default=None)

    period_breaks = TextLine(title=u"Period breaks for this context",
                             required=False,
                             default=u'1 week')

    minor_period_breaks = TextLine(title=u"Minor period breaks for this context",
                                   required=False,
                                   default=u'1 day')

    theme_bw_ = Bool(title=u"Theme for the report",
                     required=False,
                     default=True)

    number_of_most_active_user = Int(title=u"Number of most active users in this context",
                                     required=False,
                                     default=10)

    period = TextLine(title=u"Period for this context",
                      required=False,
                      default=u'daily')


class IPandasReport(IReport):
    """
    An analytics_pandas report
    """
