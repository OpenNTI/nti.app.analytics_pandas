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

from nti.app.analytics_pandas.views.videos import VideosTimeseriesReportView
from nti.app.analytics_pandas.views.videos import VideosTimeseriesContext

from nti.app.analytics_pandas.reports.z3c_zpt import ViewPageTemplateFile

from nti.app.analytics_pandas.tests import AppAnalyticsTestBase
from nti.app.analytics_pandas.tests import PandasReportsLayerTest

from nti.app.analytics_pandas.views.tests import _build_sample_context

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestVideosEvents(AppAnalyticsTestBase):

	@Lazy
	def std_report_layout_rml(self):
		path = os.path.join(
                    os.path.dirname(__file__),
                    '../../templates/std_report_layout.rml')
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
		context = VideosTimeseriesContext()
		view = VideosTimeseriesReportView(context)
		view._build_data('Bleach')
		system = {'view': view, 'context': context}
		rml = self.template(path).bind(view)(**system)

		pdf_stream = rml2pdf.parseString(rml)
		result = pdf_stream.read()
		assert_that(result, has_length(greater_than(1)))


class TestVideosViews(PandasReportsLayerTest):

	@WithSharedApplicationMockDS(testapp=True, users=True)
	def test_video_view(self):
		context = _build_sample_context(VideosTimeseriesContext)
		params = json.dumps(context.__dict__)
		response = self.testapp.post_json('/dataserver2/pandas_reports/VideosRelatedEvents',
                                    params,
                                    extra_environ=self._make_extra_environ())
		assert_that(response, has_property('content_type', 'application/pdf'))
