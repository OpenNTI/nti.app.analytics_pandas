#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import has_property

from pyramid.testing import DummyRequest

from nti.app.analytics_pandas.tests import PandasReportsLayerTest

from nti.app.analytics_pandas.views.social import SocialTimeseriesReportView

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestSocialView(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_social_report(self):
        response = self.testapp.post_json('/dataserver2/pandas_reports/SocialReport',
                                          {	  'start_date': '2015-01-01',
                                              'end_date': '2015-05-31'
                                          },
                                          extra_environ=self._make_extra_environ())
        assert_that(response,
                    has_property('content_type', 'application/pdf'))


class TestSocialOptions(ApplicationLayerTest):

    layer = PandasReportsLayerTest

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_social_report(self):
        request = DummyRequest(params={'start_date': '2015-01-01',
                                       'end_date': '2015-05-31'})
        view = SocialTimeseriesReportView(request=request)
        options = view()
        assert_that(options, is_not(none()))
        assert_that(options,
                    has_entries('has_chats_initiated', True,
                                'has_chats_joined', True,
                                'has_contacts_added', True,
                                'has_contacts_removed', True,
                                'has_friend_list_member_added', True,
                                'has_profile_views', False))
        assert_that(options,
                    has_entries('data',
                                has_entries('chats_initiated', is_not(none()),
                                            'chats_initiated', 
                                            has_entries('num_rows', 60,
                                                        'events_chart', is_not(none()),
                                                        'tuples', (),
                                                        'column_name', u'Chats Initiated'),
                                            'chats_joined', is_not(none()),
                                            'chats_joined', 
                                            has_entries('num_rows', 62,
                                                        'events_chart', is_not(none()),
                                                        'tuples', (),
                                                        'column_name', u'Chats'),
                                            'contacts_added', is_not(none()),
                                            'contacts_added', 
                                            has_entries('num_rows', 91,
                                                        'events_chart', is_not(none()),
                                                        'tuples', (),
                                                        'column_name', u'Contacts Added'),
                                            'contacts_removed', is_not(none()),
                                            'contacts_removed', 
                                            has_entries('num_rows', 9,
                                                        'events_chart', is_not(none()),
                                                        'tuples', (),
                                                        'column_name', u'Contacts Removed'),
                                            'friend_list', is_not(none()),
                                            'friend_list', 
                                            has_entries('tuples', is_not(none()))
                                            )
                                )
                    )