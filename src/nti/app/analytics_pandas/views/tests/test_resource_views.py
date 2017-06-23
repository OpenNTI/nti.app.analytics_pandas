#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import greater_than
from hamcrest import has_property

import os
import json

from zope.cachedescriptors.property import Lazy

from z3c.rml import rml2pdf

from nti.app.analytics_pandas.views.commons import cleanup_temporary_file

from nti.app.analytics_pandas.views.resource_views import ResourceViewsTimeseriesReportView
from nti.app.analytics_pandas.views.resource_views import ResourceViewsTimeseriesContext

from nti.app.analytics_pandas.reports.z3c_zpt import ViewPageTemplateFile

from nti.app.analytics_pandas.tests import AppAnalyticsTestBase
from nti.app.analytics_pandas.tests import PandasReportsLayerTest

from nti.app.analytics_pandas.views.tests import _build_sample_context

from nti.app.testing.decorators import WithSharedApplicationMockDS

class TestResourceViews(AppAnalyticsTestBase):

	def setUp(self):
		super(TestResourceViews, self).setUp()

	@Lazy
	def std_report_layout_rml(self):
		path = os.path.join(os.path.dirname(__file__), '../../templates/std_report_layout.rml')
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
		context = ResourceViewsTimeseriesContext(start_date=start_date, 
						  end_date=end_date, 
						  courses=courses,
						  period_breaks=period_breaks, 
						  minor_period_breaks=minor_period_breaks, 
						  theme_bw_=theme_bw_)
		
		view = ResourceViewsTimeseriesReportView(context)
		view._build_data('Bleach')
		system = {'view':view, 'context':context}
		rml = self.template(path).bind(view)(**system)

		pdf_stream = rml2pdf.parseString(rml)
		result = pdf_stream.read()
		assert_that(result, has_length(greater_than(1)))

class TestReourceViewsView(PandasReportsLayerTest):
	
	@WithSharedApplicationMockDS(testapp=True, users=True)
	def test_resource_views_view(self):
		context = _build_sample_context(ResourceViewsTimeseriesContext)
		params = json.dumps(context.__dict__)
		response = self.testapp.post_json('/dataserver2/pandas_reports/ResourceViews',
                                    params,
                                    extra_environ=self._make_extra_environ())
		assert_that(response, has_property('content_type', 'application/pdf'))