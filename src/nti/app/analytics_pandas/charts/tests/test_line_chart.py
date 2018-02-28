#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest

from hamcrest import is_
from hamcrest import assert_that

from nti.app.analytics_pandas.charts.colors import color01, color02
from nti.app.analytics_pandas.charts.line_chart import TimeSeriesSimpleChart
from nti.app.analytics_pandas.charts.line_chart import TimeSeriesGroupedChart

class TestLineChart(unittest.TestCase):

    def test_time_series_chart(self):
    	data = [[(19010706, 3.3900000000000001), (19010806, 3.29), (19010906, 3.2999999999999998), (19011006, 3.29), (19011106, 3.3399999999999999), (19011206, 3.4100000000000001), (19020107, 3.3700000000000001), (19020207, 3.3700000000000001), (19020307, 3.3700000000000001), (19020407, 3.5), (19020507, 3.6200000000000001), (19020607, 3.46), (19020707, 3.3900000000000001)], [(19010706, 3.2000000000000002), (19010806, 3.1200000000000001), (19010906, 3.1400000000000001), (19011006, 3.1400000000000001), (19011106, 3.1699999999999999), (19011206, 3.23), (19020107, 3.1899999999999999), (19020207, 3.2000000000000002), (19020307, 3.1899999999999999), (19020407, 3.3100000000000001), (19020507, 3.4300000000000002), (19020607, 3.29), (19020707, 3.2200000000000002)]]
    	legend= [(color01, 'Bovis Homes'), (color02, 'HSBC Holdings')]
    	chart = TimeSeriesSimpleChart(data=data, 
    							legend_color_name_pairs=legend)
    	assert_that(chart.asString('png'), is_(str))

    def test_time_series_chart2(self):
    	data = [[(20070201, 1.0), (20070228, 1.0089999999999999), (20070331, 1.0264), (20070430, 1.0430999999999999), (20070531, 1.0649), (20070630, 1.0720000000000001), (20070731, 1.0742), (20070831, 1.0553999999999999), (20070930, 1.0713999999999999), (20071031, 1.1031), (20071130, 1.093), (20071231, 1.1005), (20080131, 1.0740000000000001)], [(20070201, 1.0), (20070228, 1.0154000000000001), (20070331, 1.0155000000000001), (20070430, 1.0208999999999999), (20070531, 1.0132000000000001), (20070630, 1.0101), (20070731, 1.0185), (20070831, 1.0309999999999999), (20070930, 1.0388999999999999), (20071031, 1.0482), (20071130, 1.0670999999999999), (20071231, 1.0701000000000001), (20080131, 1.0880000000000001)], [(20070201, 1.0), (20070228, 1.0089999999999999), (20070331, 1.0182), (20070430, 1.0311999999999999), (20070531, 1.0471999999999999), (20070630, 1.0518000000000001), (20070731, 1.0532999999999999), (20070831, 1.0344), (20070930, 1.0470999999999999), (20071031, 1.0699000000000001), (20071130, 1.0613999999999999), (20071231, 1.0621), (20080131, 1.0455000000000001)]]
    	legend= ['Liberty International', 'Persimmon', 'Royal Bank of Scotland',]
    	chart = TimeSeriesGroupedChart(data=data, 
    							 legend=legend)
    	assert_that(chart.asString('png'), is_(str))

    def test_time_series_chart3(self):
        data = [[(20070201, 1.0), (20070228, 1.0089999999999999), (20070331, 1.0264), (20070430, 1.0430999999999999), (20070531, 1.0649), (20070630, 1.0720000000000001), (20070731, 1.0742), (20070831, 1.0553999999999999), (20070930, 1.0713999999999999), (20071031, 1.1031), (20071130, 1.093), (20071231, 1.1005), (20080131, 1.0740000000000001)], [(20070201, 1.0), (20070228, 1.0154000000000001), (20070331, 1.0155000000000001), (20070430, 1.0208999999999999), (20070531, 1.0132000000000001), (20070630, 1.0101), (20070731, 1.0185), (20070831, 1.0309999999999999), (20070930, 1.0388999999999999), (20071031, 1.0482), (20071130, 1.0670999999999999), (20071231, 1.0701000000000001), (20080131, 1.0880000000000001)], [(20070201, 1.0), (20070228, 1.0089999999999999), (20070331, 1.0182), (20070430, 1.0311999999999999), (20070531, 1.0471999999999999), (20070630, 1.0518000000000001), (20070731, 1.0532999999999999), (20070831, 1.0344), (20070930, 1.0470999999999999), (20071031, 1.0699000000000001), (20071130, 1.0613999999999999)]]
        legend= ['Liberty International', 'Persimmon', 'Royal Bank of Scotland',]
        chart = TimeSeriesGroupedChart(data=data, 
                                 legend=legend)
        assert_that(chart.asString('png'), is_(str))