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

from zope.testing import cleanup as testing_cleanup

from nti.app.analytics_pandas.reports.interfaces import IPandasReport

from nti.app.analytics_pandas.reports.report import PandasReport

from nti.app.contenttypes.reports.interfaces import IReportLinkProvider

from nti.app.contenttypes.reports.tests import TestPredicate
from nti.app.contenttypes.reports.tests import TestReportContext

from nti.contenttypes.reports.interfaces import IReportAvailablePredicate

from nti.contenttypes.reports.tests import ITestReportContext

from nti.dataserver.authorization import ACT_NTI_ADMIN

from nti.testing.layers import GCLayerMixin
from nti.testing.layers import ZopeComponentLayer
from nti.testing.layers import ConfiguringLayerMixin


class SharedConfiguringTestLayer(ZopeComponentLayer,
                                 GCLayerMixin,
                                 ConfiguringLayerMixin):

    set_up_packages = ('nti.app.analytics_pandas',)

    @classmethod
    def setUp(cls):
        cls.setUpPackages()

    @classmethod
    def tearDown(cls):
        cls.tearDownPackages()
        testing_cleanup.cleanUp()

    @classmethod
    def testSetUp(cls, test=None):
        pass

    @classmethod
    def testTearDown(cls):
        pass


from nti.analytics_database import Base

from nti.analytics_pandas.databases.interfaces import IDBConnection

from nti.analytics_pandas.tests import create_engine
from nti.analytics_pandas.tests import create_session
from nti.analytics_pandas.tests import read_sample_data
from nti.analytics_pandas.tests import create_sessionmaker


def setup_database(self):
    dburi = "sqlite://"
    self.engine = create_engine(dburi=dburi)
    self.metadata = getattr(Base, 'metadata')
    self.metadata.create_all(bind=self.engine)
    read_sample_data(self.engine)
    self.sessionmaker = create_sessionmaker(self.engine)
    self.session = create_session(self.sessionmaker)


class AppAnalyticsTestBase(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def setUp(self):
        setup_database(self)
        component.getGlobalSiteManager().registerUtility(self, IDBConnection)

    def tearDown(self):
        self.close()
        component.getGlobalSiteManager().unregisterUtility(self, IDBConnection)

    def close(self):
        # pylint: disable=no-member
        self.session.close()

from nti.app.testing.application_webtest import ApplicationLayerTest


class PandasReportsLayerTest(ApplicationLayerTest):

    set_up_packages = ('nti.app.analytics_pandas',)

    utils = []
    factory = None
    predicate = None
    link_provider = None

    @classmethod
    def setUp(self):
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
            self.factory = report

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
        self.utils.append(_register_report(u"TestReport",
                                           u"Test Report",
                                           u"TestDescription",
                                           (ITestReportContext,),
                                           ACT_NTI_ADMIN.id,
                                           [u"csv", u"pdf"]))

        self.predicate = functools.partial(TestPredicate)

        gsm = getGlobalSiteManager()
        gsm.registerSubscriptionAdapter(self.predicate,
                                        (TestReportContext,),
                                        IReportAvailablePredicate)

        setup_database(self)
        component.getGlobalSiteManager().registerUtility(self, IDBConnection)

    @classmethod
    def tearDown(self):
        """
        Unregister all test utilities and subscribers
        """
        sm = component.getGlobalSiteManager()
        for util in self.utils:
            sm.unregisterUtility(component=util,
                                 provided=IPandasReport,
                                 name=util.name)

        sm.unregisterSubscriptionAdapter(factory=self.factory,
                                         required=(ITestReportContext,),
                                         provided=IPandasReport)

        sm.unregisterSubscriptionAdapter(factory=self.predicate,
                                         required=(TestReportContext,),
                                         provided=IReportAvailablePredicate)

        sm.unregisterSubscriptionAdapter(factory=self.link_provider,
                                         required=(PandasReport,),
                                         provided=IReportLinkProvider)
        # pylint: disable=no-member
        self.close()
        component.getGlobalSiteManager().unregisterUtility(self, IDBConnection)

    @classmethod
    def close(self):
        # pylint: disable=no-member
        self.session.close()
