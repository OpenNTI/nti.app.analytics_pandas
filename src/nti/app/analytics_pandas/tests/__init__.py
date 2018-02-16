#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

import unittest
import functools

from zope import component

from zope.component import getGlobalSiteManager

from nti.analytics_database.interfaces import IAnalyticsDatabase

from nti.analytics_database.database import AnalyticsDB

from nti.analytics_pandas.tests import read_sample_data


class DatabaseTestMixin(object):

    @classmethod
    def register_db(cls):
        cls.db = AnalyticsDB(dburi="sqlite://",
                             defaultSQLite=True,
                             autocommit=True)
        getGlobalSiteManager().registerUtility(cls.db, IAnalyticsDatabase)
        read_sample_data(cls.db.engine)

    @classmethod
    def unregister_db(cls):
        getGlobalSiteManager().unregisterUtility(cls.db, IAnalyticsDatabase)
        # pylint: disable=no-member
        cls.db.session.commit()
        cls.db.session.close()

    @property
    def session(self):
        # pylint: disable=no-member
        return self.db.session

    @property
    def engine(self):
        # pylint: disable=no-member
        return self.db.engine

    @property
    def sessionmaker(self):
        return self.db.sessionmaker

    def close(self):
        # pylint: disable=no-member
        self.session.close()


from zope.testing import cleanup as testing_cleanup

from nti.testing.layers import GCLayerMixin
from nti.testing.layers import ZopeComponentLayer
from nti.testing.layers import ConfiguringLayerMixin


class SharedConfiguringTestLayer(ZopeComponentLayer,
                                 GCLayerMixin,
                                 ConfiguringLayerMixin,
                                 DatabaseTestMixin):

    set_up_packages = ('nti.app.analytics_pandas',)

    @classmethod
    def setUp(cls):
        cls.setUpPackages()
        cls.register_db()

    @classmethod
    def tearDown(cls):
        cls.unregister_db()
        cls.tearDownPackages()
        testing_cleanup.cleanUp()

    @classmethod
    def testSetUp(cls, test=None):
        pass

    @classmethod
    def testTearDown(cls):
        pass


class AppAnalyticsTestBase(unittest.TestCase):
    layer = SharedConfiguringTestLayer


from nti.app.analytics_pandas.reports.interfaces import IPandasReport

from nti.app.analytics_pandas.reports.report import PandasReport

from nti.app.contenttypes.reports.interfaces import IReportLinkProvider

from nti.app.contenttypes.reports.tests import TestPredicate
from nti.app.contenttypes.reports.tests import TestReportContext

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.contenttypes.reports.interfaces import IReportAvailablePredicate

from nti.contenttypes.reports.tests import ITestReportContext

from nti.dataserver.authorization import ACT_NTI_ADMIN


class PandasReportsLayerTest(ApplicationLayerTest,
                             DatabaseTestMixin):

    set_up_packages = ('nti.app.analytics_pandas',)

    utils = []
    factory = None
    predicate = None
    link_provider = None

    @classmethod
    def setUp(cls):
        """
        Set up environment for app layer report testing
        """
        def _register_report(name, title, description,
                             contexts, permission, supported_types):
            """
            Manual and temporary registration of reports
            """

            # Build a report factory
            report = functools.partial(PandasReport,
                                       name=name,
                                       title=title,
                                       description=description,
                                       contexts=contexts,
                                       permission=permission,
                                       supported_types=supported_types)
            cls.factory = report

            report_obj = report()
            # Register as a utility
            getGlobalSiteManager().registerUtility(report_obj, IPandasReport, name)

            for interface in contexts:
                # Register it as a subscriber
                getGlobalSiteManager().registerSubscriptionAdapter(report,
                                                                   (interface,),
                                                                   IPandasReport)

            return report_obj

        # Register three reports to test with
        cls.utils.append(_register_report("TestReport",
                                          "Test Report",
                                          "TestDescription",
                                          (ITestReportContext,),
                                          ACT_NTI_ADMIN.id,
                                          ["csv", "pdf"]))

        cls.predicate = functools.partial(TestPredicate)

        gsm = getGlobalSiteManager()
        gsm.registerSubscriptionAdapter(cls.predicate,
                                        (TestReportContext,),
                                        IReportAvailablePredicate)

        cls.register_db()

    @classmethod
    def tearDown(cls):
        """
        Unregister all test utilities and subscribers
        """
        sm = component.getGlobalSiteManager()
        for util in cls.utils:
            sm.unregisterUtility(component=util,
                                 provided=IPandasReport,
                                 name=util.name)

        sm.unregisterSubscriptionAdapter(factory=cls.factory,
                                         required=(ITestReportContext,),
                                         provided=IPandasReport)

        sm.unregisterSubscriptionAdapter(factory=cls.predicate,
                                         required=(TestReportContext,),
                                         provided=IReportAvailablePredicate)

        sm.unregisterSubscriptionAdapter(factory=cls.link_provider,
                                         required=(PandasReport,),
                                         provided=IReportLinkProvider)
        cls.unregister_db()
