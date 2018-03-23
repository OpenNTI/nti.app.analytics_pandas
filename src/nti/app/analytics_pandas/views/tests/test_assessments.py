#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import has_property

from pyramid.testing import DummyRequest

from nti.app.analytics_pandas.tests import PandasReportsLayerTest

from nti.app.analytics_pandas.views.assessments import AssessmentsTimeseriesReportView

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestAssessmentViews(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_assessment_report(self):
        response = self.testapp.post_json('/dataserver2/pandas_reports/AssessmentsReport',
                                          {
                                              'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                              'start_date' : '2015-02-01',
                                              'end_date' : '2015-02-28'
                                          },
                                          extra_environ=self._make_extra_environ())
        assert_that(response,
                    has_property('content_type', 'application/pdf'))


class TestAssessmentOptions(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_assessment_report(self):
        request = DummyRequest(params={'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113', 
                                       'start_date' : '2015-02-01',
                                       'end_date' : '2015-02-28'})
        view = AssessmentsTimeseriesReportView(request=request)
        options = view()
        options = view()
        assert_that(options, is_not(none()))
        assert_that(options,
                    has_entries('course_ids', is_([388]),
                                'has_assessment_event_data', True,
                                'has_assignments_taken', True,
                                'has_self_assessment_taken_per_enrollment_type', True,
                                'has_self_assessment_taken', True,
                                'has_assignments_taken_per_enrollment_type', True))
        assert_that(options,
                    has_entries('data',
                                has_entries('assignments_taken', is_not(none()),
                                            'assignments_taken', 
                                            has_entries('num_rows', 6,
                                                        'events_chart', is_not(none()),
                                                        'tuples', (),
                                                        'column_name', u'Assignments Taken'),
                                            'self_assessment_taken', is_not(none()),
                                            'self_assessment_taken', 
                                            has_entries('num_rows', 26,
                                                        'events_chart', is_not(none()),
                                                        'tuples', (),
                                                        'column_name', u'Self Assessments Taken'),
                                            'assessment_events', is_not(none()),
                                            'assessment_events', 
                                            has_entries('num_rows', 32,
                                                        'events_chart', is_not(none()),
                                                        'tuples', (),
                                                        'column_name', u'Total Events')
                                            )
                                )
                    )
