from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName

from p4a.subtyper.interfaces import IFolderishContentTypeDescriptor

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
    util = sm.queryUtility(IFolderishContentTypeDescriptor, u'collective.lineage.childsite')
    sm.unregisterUtility(util, IFolderishContentTypeDescriptor, name=u'collective.lineage.childsite')
    del sm.utilities._subscribers[0][IFolderishContentTypeDescriptor]

def uninstall(portal, reinstall=False):
    """Run the GS profile to install this package"""
    out = StringIO()
    if not reinstall:
        runProfile(portal, 'profile-collective.lineage:uninstall')
        _unregisterUtility(portal)
        print >> out, "Uninstalled collective.lineage"
    
    return out.getvalue()
