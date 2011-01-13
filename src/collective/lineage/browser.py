from zope.interface import implements
from zope.component import adapts
from zope.formlib import form
from zope.schema.fieldproperty import FieldProperty
from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from OFS.SimpleItem import SimpleItem
from plone.app.controlpanel.form import ControlPanelForm

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFCore.interfaces import IPropertiesTool
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFDefault.formlib.schema import ProxyFieldProperty

from collective.lineage.interfaces import IChildSite
from collective.lineage.interfaces import ILineageConfiguration

_ = MessageFactory('collective.lineage')


class LineageConfiguration(SimpleItem):
    implements(ILineageConfiguration)

    menu_text = FieldProperty(ILineageConfiguration['menu_text'])


class LineageConfigurationForm(ControlPanelForm):
    form_fields = form.Fields(ILineageConfiguration)

    label = _(u"Lineage Configuration Panel")
    description = _(u"You can define the text that will appear\
                    under the 'Sub-types' tab. Default is 'Child Site'")
    form_name = _(u'settings')


class LineageConfigurationFormAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(ILineageConfiguration)
    def __init__(self, context):
        super(LineageConfigurationFormAdapter, self).__init__(context)
        self.context = getUtility(IPropertiesTool).lineage_properties

    menu_text = ProxyFieldProperty(
        ILineageConfiguration['menu_text']
    )


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
                             sort_on='sortable_title')
        ]
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

        ptool = getToolByName(self, 'portal_properties')
        if "lineage_properties" in ptool:
            return ptool.lineage_properties.getProperty('menu_text')
        return "Jump to Child Site"

