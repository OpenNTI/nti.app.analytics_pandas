#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id:
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from sqlalchemy.orm.scoping import scoped_session

from zope import interface

from zope.dottedname import resolve as dottedname

from zope.schema import Field

from zope.schema._field import _isdotted  # Private method

from zope.schema.interfaces import WrongType
from zope.schema.interfaces import IFromUnicode
from zope.schema.interfaces import InvalidDottedName

from nti.schema.field import Object


@interface.implementer(IFromUnicode)
class ValidDBSession(Object):

    _type = scoped_session

    def __init__(self, **kw):
        Field.__init__(self, **kw)

    def _validate(self, value):
        if not isinstance(value, self._type):
            raise WrongType(value, self._type, self.__name__)

    def fromUnicode(self, value):
        value = value.strip()
        if not _isdotted(value):
            raise InvalidDottedName(value)
        value = dottedname.resolve(value)
        self._validate(value)
        return value
