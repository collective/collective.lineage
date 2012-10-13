from zope.interface import implements
from zope.component.interfaces import ObjectEvent

from collective.lineage.interfaces import IChildSiteWillBeCreatedEvent
from collective.lineage.interfaces import IChildSiteCreatedEvent
from collective.lineage.interfaces import IChildSiteWillBeRemovedEvent
from collective.lineage.interfaces import IChildSiteRemovedEvent


class ChildSiteWillBeCreatedEvent(ObjectEvent):
    implements(IChildSiteWillBeCreatedEvent)


class ChildSiteCreatedEvent(ObjectEvent):
    implements(IChildSiteCreatedEvent)


class ChildSiteWillBeRemovedEvent(ObjectEvent):
    implements(IChildSiteWillBeRemovedEvent)


class ChildSiteRemovedEvent(ObjectEvent):
    implements(IChildSiteRemovedEvent)
