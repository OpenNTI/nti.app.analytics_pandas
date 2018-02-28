#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

from hamcrest import is_
from hamcrest import assert_that

import unittest

from nti.app.analytics_pandas.charts.colors import generate_random_hex_colors


class TestColorsMethods(unittest.TestCase):

    def test_generate_random_hex_colors(self):
        colors = generate_random_hex_colors(3)
        assert_that(len(colors), is_(3))

        colors = generate_random_hex_colors(10)
        assert_that(len(colors), is_(10))
