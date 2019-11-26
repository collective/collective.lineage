# -*- coding: utf-8 -*-
"""
Common Lineage test fixtures and cases.
"""

try:
    # BBB
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from plone.testing import zope
except ImportError:
    # BBB Plone 5.1
    from plone.testing import z2 as zope
try:
    from plone.testing.zope import WSGI_SERVER_FIXTURE as SERVER_FIXTURE
except ImportError:
    # BBB Plone 5.1
    from plone.testing.z2 import ZSERVER_FIXTURE as SERVER_FIXTURE
from plone.app import testing as pa_testing
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    # BBB for Plone 5.0 and lower.
    get_installer = None


class LineageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.lineage
        try:
            import plone.app.contenttypes
            self['has_pact'] = True
        except ImportError:
            self['has_pact'] = False
        self.loadZCML(package=collective.lineage)
        if self['has_pact']:
            self.loadZCML(package=plone.app.contenttypes)
        if self['has_pact']:
            zope.installProduct(app, 'plone.app.contenttypes')

    def setUpPloneSite(self, portal):
        if self['has_pact']:
            applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'collective.lineage:default')


LINEAGE_FIXTURE = LineageLayer()


LINEAGE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LINEAGE_FIXTURE,),
    name='collective.lineage:IntegrationTesting'
)


LINEAGE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LINEAGE_FIXTURE,),
    name='collective.lineage:FunctionalTesting'
)


LINEAGE_SERVER_TESTING = FunctionalTesting(
    bases=(LINEAGE_FIXTURE, SERVER_FIXTURE),
    name='collective.lineage:ServerTesting'
)


class LineageTestCase(unittest.TestCase):

    layer = LINEAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        pa_testing.setRoles(
            self.portal, pa_testing.TEST_USER_ID, ['Site Administrator'])

        self.portal.invokeFactory(id='site1', type_name='Folder')
        self.childsite = self.portal['site1']
