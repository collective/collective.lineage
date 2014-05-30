from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from zope.configuration import xmlconfig


class CollectiveLineage(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.lineage
        xmlconfig.file('configure.zcml', collective.lineage,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        self['portal'] = portal
        applyProfile(portal, 'collective.lineage:default')
        roles = ('Member', 'Manager')
        portal.portal_membership.addMember('manager', 'secret', roles, [])
        roles = ('Member', 'Contributor')
        portal.portal_membership.addMember('contributor', 'secret', roles, [])

LINEAGE_FIXTURE = CollectiveLineage()
LINEAGE_INTEGRATION_TESTING = (
    IntegrationTesting(
        bases=(LINEAGE_FIXTURE, ),
        name="collective.lineage:Integration")
)
