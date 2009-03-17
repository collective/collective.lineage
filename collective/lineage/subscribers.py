from zope.app.component.interfaces import ISite
from five.localsitemanager import make_objectmanager_site
from collective.lineage.interfaces import IChildSite

def enableChildSite(event):
    """When a lineage folder is created, turn it into a component site
    """
    if event.subtype.type_interface == IChildSite:
        folder = event.object
        if not ISite.providedBy(folder):
            make_objectmanager_site(folder)
        # reindex so that the object_provides index is aware of our
        # new interface
        folder.reindexObject()

def disableChildSite(event):
    """When a child site is turned off, remove the local components
    """
    if event.subtype is not None and \
      event.subtype.type_interface == IChildSite:
        folder = event.object
        # XXX remove local site components here
        
        # reindex the object so that the object_provides index is
        # aware that we've removed it
        folder.reindexObject()
