from zope.interface import Interface
from plone.app.layout.navigation.interfaces import INavigationRoot
#from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope import schema
from zope.app.component.interfaces import IPossibleSite
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.lineage')

class ILineageBrowserLayer(Interface):
    """Browser layer marker interface
    """

class ILineageConfiguration(Interface):
  """This interface defines the lineage configlet."""

  menu_text = schema.TextLine(title=_(u"Sub-types dropdown display: "),
                                  required=False)

class IChildSite(INavigationRoot, IPossibleSite):
    """A marker interface for a Child Site.  This is comprised of
    several other marker interfaces.

    INavigationRoot
      make this a navigation root

    IPloneSiteRoot
      pretend to be the Plone site root so that we can get views
      that are registered for this

    IPossibleSite
      support local component registries
    """


class IChildSiteCreatedEvent(Interface):
    """An event that is fired after a child site is created
    """


class IChildSiteRemovedEvent(Interface):
    """An event that is fired after a child site is removed
    """

