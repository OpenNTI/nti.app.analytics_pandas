#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest

import pandas as pd

from hamcrest import is_
from hamcrest import assert_that

from nti.app.analytics_pandas.views.commons import extract_group_dataframe

class TestCommonMethods(unittest.TestCase):

    def test_extract_group_dataframe(self):
    	data = {'Groups': ['Jason', 'Jason', 'Tina', 'Tina', 'Amy'], 
        		'Date': ['2012, 02, 08', '2012, 02, 08', '2012, 02, 08', '2012, 02, 08', '2012, 02, 08'], 
        		'Score': [4, 24, 31, 2, 3]}
        df = pd.DataFrame(data, index = ['Cochice', 'Pima', 'Santa Cruz', 'Maricopa', 'Yuma']) 
        data_list = extract_group_dataframe(df, 'Groups')
        assert_that(len(data_list), is_(3)) 