#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: __init__.py 73598 2015-09-24 18:01:09Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import zope.i18nmessageid
MessageFactory = zope.i18nmessageid.MessageFactory('nti.analytics_pandas')
