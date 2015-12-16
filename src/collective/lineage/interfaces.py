# -*- coding: utf-8 -*-
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.component.interfaces import IPossibleSite
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface

_ = MessageFactory('collective.lineage')


class ILineageBrowserLayer(Interface):
    """Browser layer marker interface
    """


class IChildSite(INavigationRoot, IPossibleSite):
    """A marker interface for a Child Site. This is comprised of
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
