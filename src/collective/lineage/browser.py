from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import isDefaultPage
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.component import disableSite
from collective.lineage.events import ChildSiteCreatedEvent
from collective.lineage.events import ChildSiteRemovedEvent
from collective.lineage.events import ChildSiteWillBeCreatedEvent
from collective.lineage.events import ChildSiteWillBeRemovedEvent
from collective.lineage.interfaces import IChildSite
from five.localsitemanager import make_objectmanager_site
from plone.folder.interfaces import IFolder
from zope.component import getMultiAdapter
from zope.component.interfaces import ISite
from zope.event import notify
from zope.i18nmessageid import MessageFactory
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


_ = MessageFactory('collective.lineage')


class LineageTool(BrowserView):

    def __init__(self, context, request):

        def _get_context(ctx, req):
            if not ctx:
                return None
            if isDefaultPage(ctx, req):
                return _get_context(aq_parent(ctx), req)
            return ctx

        # we don't want to enable/disable a childsite on a default page.
        # bend context to suitable parent.
        self.context = _get_context(context, request)
        self.request = request

    @property
    def available(self):
        """True, if the context can become a lineage subsite.
        """
        return IFolder.providedBy(self.context)

    @property
    def disabled(self):
        """True, if context is not a lineage subsite but could possibly be one.
        """
        return self.available and not self.enabled

    @property
    def enabled(self):
        """True, if context is a lineage subsite.
        """
        return IChildSite.providedBy(self.context)

    def enable(self):
        """Enable a lineage subsite on this context.
        """
        ctx = self.context
        notify(ChildSiteWillBeCreatedEvent(ctx))

        # enable site
        if not ISite.providedBy(ctx):
            make_objectmanager_site(ctx)

        # provide IChildSite
        alsoProvides(ctx, IChildSite)

        ctx.reindexObject(idxs=('object_provides'))
        notify(ChildSiteCreatedEvent(ctx))

        # redirect
        self.request.response.redirect(ctx.absolute_url())

    def disable(self):
        """Disable a lineage subsite on this context.
        """
        ctx = self.context
        notify(ChildSiteWillBeRemovedEvent(ctx))

        # remove local site components
        disableSite(ctx)

        # remove IChildSite
        noLongerProvides(ctx, IChildSite)

        ctx.reindexObject(idxs=('object_provides'))
        notify(ChildSiteRemovedEvent(ctx))

        # redirect
        self.request.response.redirect(ctx.absolute_url())


class LineageSwitcherViewlet(BrowserView):
    render = ViewPageTemplateFile('switcher.pt')

    def __init__(self, context, request, view, manager):
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

    def update(self):
        pass

    def sites(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        sites = [
            dict(title=c.Title, description=c.Description, url=c.getURL())
            for c in catalog(path='/',
                             object_provides=IChildSite.__identifier__,
                             sort_on='sortable_title')]
        if not sites:
            return []
        portal_url = getToolByName(self.context, 'portal_url')
        root_url = portal_url()
        if root_url not in [s['url'] for s in sites]:
            portal_object = portal_url.getPortalObject()
            sites.insert(0, dict(title=portal_object.Title(),
                                 description=portal_object.Description(),
                                 url=root_url))
        if len(sites) <= 1:
            return []
        return sites


class LineageUtils(BrowserView):

    def isChildSite(self):
        context = self.context
        request = self.request
        portal_state = getMultiAdapter((context, request), name="plone_portal_state")  # noqa
        root_path = portal_state.navigation_root_path()
        nav_root = self.context.restrictedTraverse(root_path)
        return IChildSite.providedBy(nav_root)

    @property
    def current_childsite(self):
        childsite = None
        context = self.context
        request = self.request
        portal_state = getMultiAdapter((context, request), name="plone_portal_state")  # noqa
        root_path = portal_state.navigation_root_path()
        nav_root = self.context.restrictedTraverse(root_path)
        if IChildSite.providedBy(nav_root):
            childsite = nav_root
        return childsite
