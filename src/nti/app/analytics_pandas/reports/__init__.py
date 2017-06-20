#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: __init__.py 74920 2015-10-16 20:50:14Z carlos.sanchez $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .. import MessageFactory

from . z3c_zpt import ViewPageTemplateFile
