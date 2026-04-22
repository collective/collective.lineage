"""
Common Lineage test fixtures and cases.
"""

from plone.app import testing as pa_testing
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import zope
from plone.testing.zope import WSGI_SERVER_FIXTURE

import unittest


class LineageLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.lineage
        import plone.app.contenttypes

        self.loadZCML(package=collective.lineage)
        self.loadZCML(package=plone.app.contenttypes)
        zope.installProduct(app, "plone.app.contenttypes")

    def setUpPloneSite(self, portal):
        applyProfile(portal, "plone.app.contenttypes:default")
        applyProfile(portal, "collective.lineage:default")


LINEAGE_FIXTURE = LineageLayer()


LINEAGE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LINEAGE_FIXTURE,), name="collective.lineage:IntegrationTesting"
)


LINEAGE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LINEAGE_FIXTURE,), name="collective.lineage:FunctionalTesting"
)


LINEAGE_SERVER_TESTING = FunctionalTesting(
    bases=(LINEAGE_FIXTURE, WSGI_SERVER_FIXTURE),
    name="collective.lineage:ServerTesting",
)


class LineageTestCase(unittest.TestCase):
    layer = LINEAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        pa_testing.setRoles(
            self.portal, pa_testing.TEST_USER_ID, ["Site Administrator"]
        )

        self.portal.invokeFactory(id="site1", type_name="Folder")
        self.childsite = self.portal["site1"]
