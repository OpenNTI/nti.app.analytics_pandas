#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest

from hamcrest import not_none
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import contains_inanyorder

from zope import component
from zope import interface

from zope.configuration import config
from zope.configuration import xmlconfig

from nti.app.analytics_pandas.reports.interfaces import IPandasReport

from nti.contenttypes.reports.tests import ITestReportContext

from nti.testing.base import AbstractTestBase

HEAD_ZCML_STRING = u"""
<configure  xmlns="http://namespaces.zope.org/zope"
            xmlns:i18n="http://namespaces.zope.org/i18n"
            xmlns:zcml="http://namespaces.zope.org/zcml"
            xmlns:rep="http://nextthought.com/reports">

    <include package="zope.component" file="meta.zcml" />
    <include package="zope.security" file="meta.zcml" />
    <include package="zope.component" />
    <include package=".reports" file="meta.zcml"/>

    <configure>
        <rep:registerPandasReport name="TestReport"
                            title="Test Report"
                            description="TestDescription"
                            contexts="nti.contenttypes.reports.tests.ITestReportContext"
                            permission="TestPermission"
                            supported_types="csv pdf" />
    </configure>
</configure>
"""

@interface.implementer(ITestReportContext)
class TestReportContext():
    """
    For the purpose have grabbing registered
    reports
    """
    pass

class TestPandasZCML(unittest.TestCase):
    """
    Test that analytics_pandas reports are registered
    correctly
    """
    
    get_config_package = AbstractTestBase.get_configuration_package.__func__
    
    def _test_for_test_report(self, report):
        assert_that(report, has_property("name", "TestReport"))
        assert_that(report, has_property("title", "Test Report"))
        assert_that(report, has_property("description", "TestDescription"))
        assert_that(report, has_property("contexts", not_none()))
        assert_that(report, has_property("supported_types",
                                         contains_inanyorder("pdf", "csv")))
        assert_that(report, has_property("permission", "TestPermission"))
    
    def test_zcml_registration(self):
        context = config.ConfigurationMachine()
        context.package = self.get_config_package()
        xmlconfig.registerCommonDirectives(context)
        xmlconfig.string(HEAD_ZCML_STRING, context)
        
        report = component.subscribers((TestReportContext(),), IPandasReport)
        assert_that(report, has_length(1))
        self._test_for_test_report(report[0])
        
        report = list(component.getAllUtilitiesRegisteredFor(IPandasReport))
        assert_that(report, has_length(1))
        self._test_for_test_report(report[0])
        