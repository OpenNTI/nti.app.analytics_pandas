#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import warnings

try:
	from pandas.core.categorical import Categorical
except ImportError:
	Categorical = type(None)
	warnings.warn("pandas.core.categorical.Categorical not available")

def get_values_of_series_categorical_index_(categorical_series):
	index = categorical_series.index.values
	if isinstance(index, Categorical) or hasattr(index, 'get_values'):
		return index.get_values()
	else:
		return index

def cast_columns_as_category_(df, list_of_columns):
	if len(df.index) > 0:
		for column in list_of_columns:
			df[column] = df[column].astype('category')
	return df
