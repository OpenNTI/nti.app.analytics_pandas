#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

import unittest

import pandas as pd

from hamcrest import is_
from hamcrest import equal_to
from hamcrest import assert_that

from nti.app.analytics_pandas.views.commons import extract_group_dataframe


class TestCommonMethods(unittest.TestCase):

    def test_extract_group_dataframe(self):
        data = {
            'Groups': ['Amy', 'Jason', 'Tina', 'Tina', 'Jason'],
            'Date': ['2012, 02, 08', '2012, 02, 08', '2012, 02, 08', '2012, 02, 08', '2012, 02, 08'],
            'Score': [4, 24, 31, 2, 3]
        }
        df = pd.DataFrame(data)
        data_list, groups = extract_group_dataframe(df, 'Groups')
        assert_that(len(data_list), is_(3))
        assert_that(len(data_list[0]), is_(1))
        assert_that(len(data_list[1]), is_(2))
        assert_that(len(data_list[2]), is_(2))
        assert_that(len(groups), equal_to(len(data_list)))
        assert_that(groups[0], is_('Amy'))
        assert_that(groups[1], is_('Jason'))
        assert_that(groups[2], is_('Tina'))
