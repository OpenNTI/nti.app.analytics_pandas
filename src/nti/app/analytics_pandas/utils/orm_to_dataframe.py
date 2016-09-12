#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from pandas import DataFrame

def create_row(obj, columns):
	dictionary = {col:getattr(obj, col) for col in columns if hasattr(obj, col)}
	return dictionary

def orm_dataframe(orm_query, columns):
	"""
	takes sqlachemy orm query and a list of its columns and transform it to pandas dataframe
	"""
	result = DataFrame([create_row(i, columns) for i in orm_query])
	return result
