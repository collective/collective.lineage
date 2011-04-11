from zope.app.component.interfaces import ISite
import zope.event

from Products.CMFCore.utils import getToolByName
from Products.Five.component import disableSite
from five.localsitemanager import make_objectmanager_site

from collective.lineage.interfaces import IChildSite
from collective.lineage.events import ChildSiteCreatedEvent
from collective.lineage.events import ChildSiteRemovedEvent

def reindexObjectProvides(folder):
    pc = getToolByName(folder, 'portal_catalog')
    pc.reindexObject(
        folder,
        idxs=['object_provides']
    )

def enableFolder(folder):
    if not ISite.providedBy(folder):
        make_objectmanager_site(folder)
    # reindex so that the object_provides index is aware of our
    # new interface
    reindexObjectProvides(folder)
    zope.event.notify(ChildSiteCreatedEvent(folder))

def disableFolder(folder):
    # remove local site components
    disableSite(folder)

    # reindex the object so that the object_provides index is
    # aware that we've removed it
    reindexObjectProvides(folder)
    zope.event.notify(ChildSiteRemovedEvent(folder))

def enableChildSite(event):
    """When a lineage folder is created, turn it into a component site
    """
    if event.subtype.type_interface == IChildSite:
        folder = event.object
        enableFolder(folder)

def disableChildSite(event):
    """When a child site is turned off, remove the local components
    """
    if event.subtype is not None and \
      event.subtype.type_interface == IChildSite:
        folder = event.object
        disableFolder(folder)
