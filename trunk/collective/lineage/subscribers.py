from zope.app.component.interfaces import ISite
import zope.event

from Products.CMFCore.utils import getToolByName
from Products.Five.component import disableSite
from five.localsitemanager import make_objectmanager_site

from collective.lineage.interfaces import IChildSite
from collective.lineage.events import ChildSiteCreatedEvent
from collective.lineage.events import ChildSiteRemovedEvent

def enableChildSite(event):
    """When a lineage folder is created, turn it into a component site
    """
    if event.subtype.type_interface == IChildSite:
        folder = event.object
        if not ISite.providedBy(folder):
            make_objectmanager_site(folder)
        # reindex so that the object_provides index is aware of our
        # new interface
        pc = getToolByName(folder, 'portal_catalog')
        pc.reindexObject(
            folder,
            idxs=['object_provides']
            )
        zope.event.notify(ChildSiteCreatedEvent(event.object))

def disableChildSite(event):
    """When a child site is turned off, remove the local components
    """
    if event.subtype is not None and \
      event.subtype.type_interface == IChildSite:
        folder = event.object
        # remove local site components
        disableSite(folder)
        
        # reindex the object so that the object_provides index is
        # aware that we've removed it
        pc = getToolByName(folder, 'portal_catalog')
        pc.reindexObject(
            folder,
            idxs=['object_provides']
            )
        zope.event.notify(ChildSiteRemovedEvent(event.object))
