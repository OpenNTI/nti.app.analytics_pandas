#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from zope.testing import cleanup as testing_cleanup

from zope import component

from zope.component import getGlobalSiteManager

import unittest
import functools

from nti.app.analytics_pandas.reports.report import PandasReport

from nti.app.analytics_pandas.reports.interfaces import IPandasReport

from nti.contenttypes.reports.interfaces import IReportAvailablePredicate

from nti.contenttypes.reports.tests import ITestReportContext

from nti.app.contenttypes.reports.interfaces import IReportLinkProvider

from nti.app.contenttypes.reports.tests import TestReportContext
from nti.app.contenttypes.reports.tests import TestPredicate

from nti.dataserver.authorization import ACT_NTI_ADMIN

from nti.testing.layers import GCLayerMixin
from nti.testing.layers import ZopeComponentLayer
from nti.testing.layers import ConfiguringLayerMixin


class SharedConfiguringTestLayer(ZopeComponentLayer,
                                 GCLayerMixin,
                                 ConfiguringLayerMixin):

    set_up_packages = ('nti.app.analytics_pandas.reports',
                       'nti.app.analytics_pandas.views',
                       'nti.app.analytics_pandas')

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


from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine as sqlalchemy_create_engine


def create_engine(dburi, pool_size=30, max_overflow=10, pool_recycle=300):
    try:
        if dburi == 'sqlite://':
            result = sqlalchemy_create_engine(dburi,
                                              connect_args={
                                                  'check_same_thread': False},
                                              poolclass=StaticPool)

        else:
            result = sqlalchemy_create_engine(dburi,
                                              pool_size=pool_size,
                                              max_overflow=max_overflow,
                                              pool_recycle=pool_recycle)
    except TypeError:
        # SQLite does not use pooling anymore.
        result = sqlalchemy_create_engine(dburi)
    return result


def create_sessionmaker(engine, autoflush=True, twophase=True):
    result = sessionmaker(bind=engine,
                          autoflush=autoflush,
                          twophase=twophase)
    return result


def create_session(sessionmaker):
    return scoped_session(sessionmaker)


from nti.analytics_database import Base

from nti.analytics_pandas.databases.db_connection import DBConnection

from nti.analytics_pandas.databases.interfaces import IDBConnection


class AppAnalyticsTestBase(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def setUp(self):
        # TODO: Fix URI
        self.db = DBConnection()
        component.getGlobalSiteManager().registerUtility(self.db, IDBConnection)

    def tearDown(self):
        self.db.session.close()
        component.getGlobalSiteManager().unregisterUtility(self.db)


from nti.app.testing.application_webtest import ApplicationLayerTest


class PandasReportsLayerTest(ApplicationLayerTest):

    set_up_packages = ('nti.app.analytics_pandas',
                       'nti.app.analytics_pandas.reports')

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
        self.db = DBConnection()
        component.getGlobalSiteManager().registerUtility(self.db, IDBConnection)

    @classmethod
    def tearDown(self):
        """
        Unregister all test utilities and
        subscribers
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
        self.db.session.close()
        component.getGlobalSiteManager().unregisterUtility(self.db)
