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

from nti.app.analytics_pandas.views.notes import NotesTimeseriesReportView

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestNotesView(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_notes_report(self):
        response = self.testapp.post_json('/dataserver2/pandas_reports/NotesReport',
                                          {
                                              'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                              'start_date': '2015-01-01',
                                              'end_date': '2015-05-31'
                                          },
                                          extra_environ=self._make_extra_environ())
        assert_that(response,
                    has_property('content_type', 'application/pdf'))


class TestNotesOptions(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_notes_report(self):
        request = DummyRequest(params={'ntiid': 'tag:nextthought.com,2011-10:NTI-CourseInfo-Spring2015_SOC_1113',
                                       'start_date': '2015-01-01',
                                       'end_date': '2015-05-31'})
        view = NotesTimeseriesReportView(request=request)
        options = view()
        assert_that(options, is_not(none()))
        assert_that(options,
                    has_entries('course_ids', is_([388]),
                                'has_note_view_events', True,
                                'has_note_create_events', True,
                                'has_note_like_events', False,
                                'has_note_favorite_events', False))
        assert_that(options,
                    has_entries('data',
                                has_entries('notes_viewed', is_not(none()),
                                            'notes_viewed', 
                                            has_entries('num_rows', 42,
                                                        'events_chart', is_not(none()),
                                                        'tuples', (),
                                                        'column_name', u'Notes Viewed'),
                                            'notes_created', is_not(none()),
                                            'notes_created', 
                                            has_entries('num_rows', 20,
                                                        'events_chart', is_not(none()),
                                                        'tuples', (),
                                                        'column_name', u'Notes Created')
                                            )
                                )
                    )
