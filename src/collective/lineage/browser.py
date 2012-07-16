from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from collective.lineage.interfaces import IChildSite
from collective.lineage.interfaces import ILineageSettings

_ = MessageFactory('collective.lineage')


class LineageSwitcherViewlet(BrowserView):

    def __init__(self, context, request, view, manager):
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

    def update(self):
        pass

    render = ViewPageTemplateFile('switcher.pt')

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

    def getSwitcherDefault(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ILineageSettings)
        if settings.menu_text:
            return settings.menu_text
        return "Jump to Child Site"

    def isChildSite(self):
        portal_state = self.context.restrictedTraverse('plone_portal_state')
        root_path = portal_state.navigation_root_path()
        nav_root = self.context.restrictedTraverse(root_path)
        return IChildSite.providedBy(nav_root)
