#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

def _build_sample_context(context):
        start_date = '2015-10-05'
        end_date = '2015-10-20'
        courses = ['1068', '1096', '1097', '1098', '1099']
        period_breaks = '1 week'
        minor_period_breaks = '1 day'
        theme_bw_ = True
        number_of_most_active_user = 10
        period = "daily"
        ret_context = context(start_date=start_date,
                              end_date=end_date,
                              courses=courses,
                              period_breaks=period_breaks,
                              minor_period_breaks=minor_period_breaks,
                              theme_bw_=theme_bw_,
                              number_of_most_active_user=number_of_most_active_user,
                              period=period)
        return ret_context