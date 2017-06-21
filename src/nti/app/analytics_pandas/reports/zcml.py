#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.app.analytics_pandas.reports.interfaces import IPandasReport

from nti.app.analytics_pandas.reports.report import PandasReport

from nti.contenttypes.reports.zcml import IRegisterReport
from nti.contenttypes.reports.zcml import registerReport


class IRegisterPandasReport(IRegisterReport):
    """
    Register parameters for an analytics_pandas report
    """


def registerPandasReport(_context, name, title, description, contexts,
                         permission, supported_types, registration_name=None):
    """
    Register an analytics_pandas report
    """
    registerReport(_context=_context,
                   name=name,
                   title=title,
                   description=description,
                   contexts=contexts,
                   permission=permission,
                   supported_types=supported_types,
                   registration_name=registration_name,
                   report_class=PandasReport,
                   report_interface=IPandasReport)
