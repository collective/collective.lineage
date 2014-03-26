from Products.CMFCore.utils import getToolByName
from cStringIO import StringIO
from collective.lineage.interfaces import IChildSite
from p4a.subtyper.interfaces import IFolderishContentTypeDescriptor
from p4a.subtyper.interfaces import ISubtyped
from p4a.z2utils.utils import remove_marker_ifaces


def runProfile(portal, profileName):
    setupTool = getToolByName(portal, 'portal_setup')
    setupTool.runAllImportStepsFromProfile(profileName)


def install(portal):
    """Run the GS profile to install this package"""
    out = StringIO()
    runProfile(portal, 'profile-collective.lineage:default')
    print >> out, "Installed collective.lineage"
    return out.getvalue()


def _unregisterUtility(portal):
    sm = portal.getSiteManager()
    util = sm.queryUtility(
        IFolderishContentTypeDescriptor, u'collective.lineage.childsite')
    sm.unregisterUtility(
        util,
        IFolderishContentTypeDescriptor, name=u'collective.lineage.childsite')
    if IFolderishContentTypeDescriptor in sm.utilities._subscribers[0]:
        del sm.utilities._subscribers[0][IFolderishContentTypeDescriptor]


def uninstall(portal, reinstall=False):
    """Run the GS profile to install this package"""
    out = StringIO()
    if not reinstall:
        runProfile(portal, 'profile-collective.lineage:uninstall')
        _unregisterUtility(portal)
        remove_marker_ifaces(portal, (IChildSite, ISubtyped))
        print >> out, "Uninstalled collective.lineage"

    return out.getvalue()
