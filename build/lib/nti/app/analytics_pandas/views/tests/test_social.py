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

from nti.app.analytics_pandas.views.commons import cleanup_temporary_file

from nti.app.analytics_pandas.views.social import View
from nti.app.analytics_pandas.views.social import Context

from nti.app.analytics_pandas.reports.z3c_zpt import ViewPageTemplateFile

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestHighlightsEvents(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestHighlightsEvents, self).setUp()

	@Lazy
	def std_report_layout_rml(self):
		path = os.path.join(os.path.dirname(__file__), '../../templates/std_report_layout.rml')
		return path

	@Lazy
	def highlights_rml(self):
		path = os.path.join(os.path.dirname(__file__), '../../templates/highlights.rml')
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
		context = Context()
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
		start_date = '2015-06-01'
		end_date = '2015-10-19'
		period = 'weekly'
		period_breaks = '1 week'
		minor_period_breaks = None
		theme_bw_ = True
		context = Context(start_date=start_date,
						  end_date=end_date,
				 		  period_breaks=period_breaks,
				 		  minor_period_breaks=minor_period_breaks,
				 		  theme_bw_=theme_bw_,
				 		  number_of_most_active_user=10,
				 		  period=period)
		assert_that(context.start_date, equal_to('2015-06-01'))

		view = View(context)
		view()
		assert_that(view.options['data'] , instance_of(dict))
		assert_that(view.options['data'].keys(), has_item('contacts_added'))

		system = {'view':view, 'context':context}
		rml = self.template(path).bind(view)(**system)

		pdf_stream = rml2pdf.parseString(rml)
		pdf_stream.seek(0)
		readbuf = pdf_stream.read()
		assert_that(readbuf, has_length(greater_than(0)))

		data = view.options['data']
		cleanup_temporary_file(data)
