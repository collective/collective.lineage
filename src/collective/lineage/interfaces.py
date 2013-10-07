from zope.interface import Interface
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.imaging.interfaces import IImagingSchema
from zope import schema
from zope.component.interfaces import IPossibleSite
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.lineage')


class ILineageBrowserLayer(Interface):
    """Browser layer marker interface
    """


class IChildSite(INavigationRoot, IPossibleSite, IImagingSchema):
    """A marker interface for a Child Site.  This is comprised of
    several other marker interfaces.

    INavigationRoot
      make this a navigation root

    IPossibleSite
      support local component registries
    """


class IChildSiteWillBeCreatedEvent(Interface):
    """An event that is fired before a child site is created
    """


class IChildSiteCreatedEvent(Interface):
    """An event that is fired after a child site is created
    """


class IChildSiteWillBeRemovedEvent(Interface):
    """An event that is fired before the child site is removed
    """


class IChildSiteRemovedEvent(Interface):
    """An event that is fired after a child site is removed
    """


class ILineageConfiguration(Interface):
    """This interface defines the lineage configlet."""


class ILineageSettings(Interface):
    """Global Lineage Settings
    """
    menu_text = schema.TextLine(
        title=_(u"Sub-type menu text"),
        description=_(
            u"help_subtype_text",
            default=(
                u"You can define the text that will appear under the "
                "'Sub-types' tab. Default is 'Child Site'"),
        ),
        required=False,
        default=u'',
    )
