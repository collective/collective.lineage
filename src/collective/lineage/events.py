# -*- coding: utf-8 -*-
from collective.lineage.interfaces import IChildSiteCreatedEvent
from collective.lineage.interfaces import IChildSiteRemovedEvent
from collective.lineage.interfaces import IChildSiteWillBeCreatedEvent
from collective.lineage.interfaces import IChildSiteWillBeRemovedEvent

try:
    from zope.interface.interfaces import ObjectEvent
except ImportError:
    # BBB Plone 4.3
    from zope.component.interfaces import ObjectEvent
from zope.interface import implementer


class ChildSiteWillBeCreatedEvent(ObjectEvent):
    implementer(IChildSiteWillBeCreatedEvent)


class ChildSiteCreatedEvent(ObjectEvent):
    implementer(IChildSiteCreatedEvent)


class ChildSiteWillBeRemovedEvent(ObjectEvent):
    implementer(IChildSiteWillBeRemovedEvent)


class ChildSiteRemovedEvent(ObjectEvent):
    implementer(IChildSiteRemovedEvent)
