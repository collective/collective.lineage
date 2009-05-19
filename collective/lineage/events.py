from zope.interface import implements
from zope.component.interfaces import ObjectEvent

from collective.lineage.interfaces import IChildSiteCreatedEvent
from collective.lineage.interfaces import IChildSiteRemovedEvent

class ChildSiteCreatedEvent(ObjectEvent):
    implements(IChildSiteCreatedEvent)


class ChildSiteRemovedEvent(ObjectEvent):
    implements(IChildSiteRemovedEvent)

