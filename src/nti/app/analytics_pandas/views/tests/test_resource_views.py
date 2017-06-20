#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import instance_of
from hamcrest import greater_than

import os

from zope.cachedescriptors.property import Lazy

from z3c.rml import rml2pdf

from nti.analytics_pandas.reports.views.commons import cleanup_temporary_file

from nti.analytics_pandas.reports.views.resource_views import View
from nti.analytics_pandas.reports.views.resource_views import Context

from nti.analytics_pandas.reports.z3c_zpt import ViewPageTemplateFile

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestResourceViews(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestResourceViews, self).setUp()

	@Lazy
	def std_report_layout_rml(self):
		path = os.path.join(os.path.dirname(__file__), '../../templates/std_report_layout.rml')
		return path

	@Lazy
	def resource_views_rml(self):
		path = os.path.join(os.path.dirname(__file__), '../../templates/resource_views.rml')
		return path

	def template(self, path):
		result = ViewPageTemplateFile(path,
									  auto_reload=(False,),
									  debug=False)
		return result

	def test_std_report_layout_rml(self):
		# make sure  template exists
		path = self.std_report_layout_rml
		assert_that(os.path.exists(path), is_(True))

		# prepare view and context
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		courses = ['388']
		period_breaks = '1 week'
		minor_period_breaks = '1 day'
		theme_bw_ = True
		context = Context(session=self.session, 
						  start_date=start_date, 
						  end_date=end_date, 
						  courses=courses,
						  period_breaks=period_breaks, 
						  minor_period_breaks=minor_period_breaks, 
						  theme_bw_=theme_bw_)
		
		view = View(context)
		view._build_data('Bleach')
		system = {'view':view, 'context':context}
		rml = self.template(path).bind(view)(**system)

		pdf_stream = rml2pdf.parseString(rml)
		result = pdf_stream.read()
		assert_that(result, has_length(greater_than(1)))

	def test_generate_pdf_from_rml(self):
		# make sure  template exists
		path = self.std_report_layout_rml
		assert_that(os.path.exists(path), is_(True))

		# prepare view and context
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		courses = ['388']
		period_breaks = '1 week'
		minor_period_breaks = '1 day'
		theme_bw_ = True
		context = Context(session=self.session, 
						  start_date=start_date, 
						  end_date=end_date, 
						  courses=courses,
						  period_breaks=period_breaks, 
						  minor_period_breaks=minor_period_breaks, 
						  theme_bw_=theme_bw_)
		assert_that(context.start_date, equal_to('2015-01-01'))

		view = View(context)
		view()
		assert_that(view.options['data'] , instance_of(dict))
		assert_that(view.options['data'].keys(), has_item('resource_view_events'))

		system = {'view':view, 'context':context}
		rml = self.template(path).bind(view)(**system)

		pdf_stream = rml2pdf.parseString(rml)
		pdf_stream.seek(0)
		readbuf = pdf_stream.read()
		assert_that(readbuf, has_length(greater_than(0)))

		data = view.options['data']
		cleanup_temporary_file(data)
