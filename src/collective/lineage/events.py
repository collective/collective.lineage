# -*- coding: utf-8 -*-
from collective.lineage.interfaces import IChildSiteCreatedEvent
from collective.lineage.interfaces import IChildSiteRemovedEvent
from collective.lineage.interfaces import IChildSiteWillBeCreatedEvent
from collective.lineage.interfaces import IChildSiteWillBeRemovedEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implements


class ChildSiteWillBeCreatedEvent(ObjectEvent):
    implements(IChildSiteWillBeCreatedEvent)


class ChildSiteCreatedEvent(ObjectEvent):
    implements(IChildSiteCreatedEvent)


class ChildSiteWillBeRemovedEvent(ObjectEvent):
    implements(IChildSiteWillBeRemovedEvent)


class ChildSiteRemovedEvent(ObjectEvent):
    implements(IChildSiteRemovedEvent)
