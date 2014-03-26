from Products.CMFCore.utils import getToolByName
from Products.Five.component import disableSite
from collective.lineage.events import ChildSiteCreatedEvent
from collective.lineage.events import ChildSiteRemovedEvent
from collective.lineage.events import ChildSiteWillBeCreatedEvent
from collective.lineage.events import ChildSiteWillBeRemovedEvent
from collective.lineage.interfaces import IChildSite
from five.localsitemanager import make_objectmanager_site
from p4a.subtyper.interfaces import ISubtypeAddedEvent
from p4a.subtyper.interfaces import ISubtypeRemovedEvent
from zope.component import adapter
from zope.component.interfaces import ISite
import zope.event


def reindexObjectProvides(folder):
    pc = getToolByName(folder, 'portal_catalog')
    pc.reindexObject(
        folder,
        idxs=['object_provides']
    )


def enableFolder(folder):
    zope.event.notify(ChildSiteWillBeCreatedEvent(folder))
    if not ISite.providedBy(folder):
        make_objectmanager_site(folder)
    # reindex so that the object_provides index is aware of our
    # new interface
    reindexObjectProvides(folder)
    zope.event.notify(ChildSiteCreatedEvent(folder))


def disableFolder(folder):
    zope.event.notify(ChildSiteWillBeRemovedEvent(folder))
    # remove local site components
    disableSite(folder)

    # reindex the object so that the object_provides index is
    # aware that we've removed it
    reindexObjectProvides(folder)
    zope.event.notify(ChildSiteRemovedEvent(folder))


@adapter(ISubtypeAddedEvent)
def enableChildSite(event):
    """When a lineage folder is created, turn it into a component site
    """
    if not IChildSite.providedBy(event.object):
        return
    folder = event.object
    enableFolder(folder)


@adapter(ISubtypeRemovedEvent)
def disableChildSite(event):
    """When a child site is turned off, remove the local components
    """
    subtype = event.subtype
    if subtype is not None and subtype.type_interface == IChildSite:
        folder = event.object
        disableFolder(folder)
