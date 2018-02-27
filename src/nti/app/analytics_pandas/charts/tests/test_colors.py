#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest

from hamcrest import is_
from hamcrest import assert_that

from nti.app.analytics_pandas.charts.colors import generate_random_hex_colors

class TestColorsMethods(unittest.TestCase):

    def test_generate_random_hex_colors(self):
        colors = generate_random_hex_colors(3)
        assert_that(len(colors), is_(3))

        colors = generate_random_hex_colors(10)
        assert_that(len(colors), is_(10))