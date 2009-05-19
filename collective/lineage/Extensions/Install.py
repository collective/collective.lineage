from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName

def runProfile(portal, profileName):
    setupTool = getToolByName(portal, 'portal_setup')
    setupTool.runAllImportStepsFromProfile(profileName)

def install(portal):
    """Run the GS profile to install this package"""
    out = StringIO()
    runProfile(portal, 'profile-collective.lineage:default')
    print >>out, "Installed collective.lineage"
    return out.getvalue()

def uninstall(portal, reinstall=False):
    """Run the GS profile to install this package"""
    out = StringIO()
    if not reinstall:
        runProfile(portal, 'profile-collective.lineage:uninstall')
        print >>out, "Uninstalled collective.lineage"
    return out.getvalue()
