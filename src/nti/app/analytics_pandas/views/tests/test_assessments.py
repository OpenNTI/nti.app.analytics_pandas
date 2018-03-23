#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import assert_that
from hamcrest import has_property

from nti.app.analytics_pandas.tests import PandasReportsLayerTest

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestAssessmentViews(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_assessment_report(self):
        response = self.testapp.post_json('/dataserver2/pandas_reports/AssessmentsReport',
										  {
											 'ntiid': 'course-ntiid',
										  },
                                    	  extra_environ=self._make_extra_environ())
        assert_that(response,
                    has_property('content_type', 'application/pdf'))
