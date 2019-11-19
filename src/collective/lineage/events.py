# -*- coding: utf-8 -*-
from collective.lineage.interfaces import IChildSiteCreatedEvent
from collective.lineage.interfaces import IChildSiteRemovedEvent
from collective.lineage.interfaces import IChildSiteWillBeCreatedEvent
from collective.lineage.interfaces import IChildSiteWillBeRemovedEvent

from zope.interface import implementer
from zope.interface.interfaces import ObjectEvent


class ChildSiteWillBeCreatedEvent(ObjectEvent):
    implementer(IChildSiteWillBeCreatedEvent)


class ChildSiteCreatedEvent(ObjectEvent):
    implementer(IChildSiteCreatedEvent)


class ChildSiteWillBeRemovedEvent(ObjectEvent):
    implementer(IChildSiteWillBeRemovedEvent)


class ChildSiteRemovedEvent(ObjectEvent):
    implementer(IChildSiteRemovedEvent)
