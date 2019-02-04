# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import zserver
from plone.testing import zope

try:
    from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
    HAS_ROBOT = True
except ImportError:
    HAS_ROBOT = False

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


if HAS_ROBOT:
    LINEAGE_ACCEPTANCE_TESTING = FunctionalTesting(
        bases=(
            LINEAGE_FIXTURE,
            REMOTE_LIBRARY_BUNDLE_FIXTURE,
            zserver.ZSERVER_FIXTURE
        ),
        name='collective.lineage:AcceptanceTesting'
    )
