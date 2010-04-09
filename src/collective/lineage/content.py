from zope.interface import implements

from zope.deprecation import deprecated

from zope.component.factory import Factory
from zope.app.component.interfaces import ISite
from zope.app.component.interfaces import IPossibleSite

from plone.app.content.interfaces import INameFromTitle
from plone.app.content.container import Container
from plone.app.layout.navigation.interfaces import INavigationRoot

from collective.lineage.interfaces import IChildSite
from collective.lineage import MessageFactory as _

from OFS.OrderSupport import OrderSupport
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from five.localsitemanager import make_objectmanager_site

deprecated("ChildFolder", "The Child Folder type is deprecated and will be removed "
           "in the next lineage release. Use the Folder type instead "
           "and activate it with subtyper.")

class ChildFolder(OrderSupport, BrowserDefaultMixin, Container):
    implements(IChildSite,
               INavigationRoot,     # make this a navigation root
               IPloneSiteRoot,      # pretend to be the Plone site root so that we can get views that are
                                    # registered for this
               INameFromTitle,      # title-to-id renaming
               IPossibleSite,       # support local component registries - see enable_site() below.
               )

    portal_type = "Child Folder"

    title = u""
    description = u""

factory = Factory(ChildFolder, title=_(u"Create a new lineage folder"))
def enable_site(object, event):
    """When a lineage folder is created, turn it into a component site
    """
    folder = event.object
    if not ISite.providedBy(folder):
        make_objectmanager_site(folder)
