from zope.component import createObject
from zope.formlib import form

from plone.app.form import base

from Products.Five.browser import BrowserView

from collective.lineage.interfaces import IChildFolder
from collective.lineage import MessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class ChildFolderAddForm(base.AddForm):
    
    form_fields = form.Fields(IChildFolder)
    title = _(u"Add Child Folder")
    label = _(u"Add Child Folder")
    description = _(u"Please fill in the details below")
    form_name = _(u"Details")
    
    def create(self, data):
        folder = createObject(u"collective.lineage.ChildFolder")
        form.applyChanges(folder, self.form_fields, data)
        return folder
    
class ChildFolderEditForm(base.EditForm):
    
    form_fields = form.Fields(IChildFolder)
    label = _(u"Edit Child Folder")
    form_name = _(u"Details")

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
        
        sites = [dict(title=c.Title, description=c.Description, url=c.getURL())
                    for c in catalog(path='/',
                                     object_provides=IChildFolder.__identifier__,
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

