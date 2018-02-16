#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

from hamcrest import has_item
from hamcrest import has_entry
from hamcrest import assert_that

import json

from nti.app.analytics_pandas.tests import PandasReportsLayerTest

from nti.app.contenttypes.reports.tests import TestReportContext

from nti.app.testing.decorators import WithSharedApplicationMockDS

from nti.dataserver.tests import mock_dataserver

from nti.ntiids.oids import to_external_ntiid_oid


class TestPandasDecorators(PandasReportsLayerTest):

    basic_user = u"pgreazy"

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_pandas_report_decorators(self):

        with mock_dataserver.mock_db_trans(self.ds):
            user = self._create_user(self.basic_user)
            test_context = TestReportContext()
            test_context.containerId = u"tag:nti:foo"
            test_context.creator = self.basic_user
            user.addContainedObject(test_context)
            ntiid = to_external_ntiid_oid(test_context)

        response = self.testapp.get('/dataserver2/Objects/' + ntiid,
                                    extra_environ=self._make_extra_environ(self.basic_user))

        res_dict = json.loads(response.body)

        assert_that(res_dict,
                    has_entry("Links",
                              has_item(has_entry("rel", "report-TestReport"))))
