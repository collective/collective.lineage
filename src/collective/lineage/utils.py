# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from collective.lineage.events import ChildSiteCreatedEvent
from collective.lineage.events import ChildSiteRemovedEvent
from collective.lineage.events import ChildSiteWillBeCreatedEvent
from collective.lineage.events import ChildSiteWillBeRemovedEvent
from collective.lineage.interfaces import IChildSite
from five.localsitemanager import make_objectmanager_site
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.component import disableSite
from zope.component.hooks import getSite
from zope.component.interfaces import ISite
from zope.event import notify
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


def enable_childsite(context):
    notify(ChildSiteWillBeCreatedEvent(context))

    # enable site
    if not ISite.providedBy(context):
        make_objectmanager_site(context)

    # provide IChildSite
    alsoProvides(context, IChildSite)

    context.reindexObject(idxs=('object_provides'))
    notify(ChildSiteCreatedEvent(context))


def disable_childsite(context):
    notify(ChildSiteWillBeRemovedEvent(context))

    # remove local site components
    disableSite(context)

    # remove IChildSite
    noLongerProvides(context, IChildSite)

    context.reindexObject(idxs=('object_provides'))
    notify(ChildSiteRemovedEvent(context))


def parent_site():

    def _find_site(ctx):
        # First, stop at IPloneSiteRoot
        if IPloneSiteRoot.providedBy(ctx):
            return ctx
        # Then walk up
        ctx = aq_parent(ctx)
        if IChildSite.providedBy(ctx):
            return ctx
        return _find_site(ctx)

    # Start at current site
    site = _find_site(getSite())
    return site
