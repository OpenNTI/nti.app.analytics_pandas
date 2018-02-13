#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

from hamcrest import is_
from hamcrest import not_none
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import contains_inanyorder

from zope import component
from zope import interface

from zope.configuration import config
from zope.configuration import xmlconfig

from zope.dottedname import resolve as dottedname

from nti.app.analytics_pandas.reports.interfaces import IPandasReport

from nti.contenttypes.reports.tests import ITestReportContext

from nti.app.analytics_pandas.tests import PandasReportsLayerTest


HEAD_ZCML_STRING = u"""
<configure  xmlns="http://namespaces.zope.org/zope"
            xmlns:i18n="http://namespaces.zope.org/i18n"
            xmlns:zcml="http://namespaces.zope.org/zcml"
            xmlns:rep="http://nextthought.com/reports">

    <include package="zope.component" file="meta.zcml" />
    <include package="zope.component" />
    <include package="zope.vocabularyregistry" />

    <include package=".reports" file="meta.zcml"/>

    <configure>
        <rep:registerPandasReport name="ZCML_TestReport"
                                  title="Test Report"
                                  description="TestDescription"
                                  contexts="nti.contenttypes.reports.tests.ITestReportContext"
                                  permission="zope.View"
                                  supported_types="csv pdf" />
    </configure>

</configure>
"""


@interface.implementer(ITestReportContext)
class TestReportContext(object):
    """
    For the purpose have grabbing registered
    reports
    """
    pass


class TestPandasZCML(PandasReportsLayerTest):
    """
    Test that analytics_pandas reports are registered correctly
    """

    def _test_for_test_report(self, report):
        assert_that(report, has_property("name", "ZCML_TestReport"))
        assert_that(report, has_property("title", "Test Report"))
        assert_that(report, has_property("description", "TestDescription"))
        assert_that(report, has_property("contexts", not_none()))
        assert_that(report, has_property("supported_types",
                                         contains_inanyorder("pdf", "csv")))
        assert_that(report, has_property("permission", "zope.View"))

    def test_zcml_registration(self):
        context = config.ConfigurationMachine()
        context.package = dottedname.resolve("nti.app.analytics_pandas")
        xmlconfig.registerCommonDirectives(context)
        xmlconfig.string(HEAD_ZCML_STRING, context)

        report = component.getUtility(IPandasReport, "ZCML_TestReport")
        assert_that(report, is_(not_none()))
        self._test_for_test_report(report)
