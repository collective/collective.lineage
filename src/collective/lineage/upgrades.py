from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from collective.lineage.interfaces import ILineageConfiguration
from collective.lineage.interfaces import ILineageSettings
from logging import getLogger
from p4a.subtyper import engine
from p4a.subtyper import interfaces
from plone.app.layout.navigation.defaultpage import getDefaultPage
from plone.portlets.constants import CONTENT_TYPE_CATEGORY
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.constants import GROUP_CATEGORY
from plone.portlets.interfaces import ILocalPortletAssignable
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor
from zope.component import getUtility
from zope.component import provideUtility
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

import transaction


try:
    # Plone < 4.3
    from zope.app.component.hooks import getSite
except ImportError:
    # Plone >= 4.3
    from zope.component.hooks import getSite  # NOQA


logger = getLogger('collective.lineage.upgrades')


def migrateControlPanel(context):
    """keep existing settings for 'menu_text' intact,
       delete the lineage_properties from portal_properties,
       un-register/remove the 'lineage_config' utility,
       remove the ILineageConfiguration interface
    """
    # being sure that the registry is ready to be used (see #11)
    context.portal_setup.runAllImportStepsFromProfile('profile-plone.app.registry:default')
    context.portal_setup.runImportStepFromProfile('profile-collective.lineage:default', 'plone.app.registry')
    migrate_settings(context)
    remove_controlpanel_action(context)
    remove_utility(context)
    remove_interface(context)


def migrate_settings(context):
    """keep existing settings for menu_text
    """
    ptool = getToolByName(context, 'portal_properties')
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ILineageSettings)
    if "lineage_properties" in ptool:
        settings.menu_text = ptool.lineage_properties.getProperty(
            'menu_text').decode('utf-8')
        logger.info("Menu Text set to %s" % settings.menu_text)
        ptool.manage_delObjects(['lineage_properties'])
        logger.info("removed lineage_properties from portal_properties")


def remove_controlpanel_action(context):
    """remove control panel action
    """
    cp = getToolByName(context, 'portal_controlpanel')
    actions = cp.listActions()
    index = 0
    for action in actions:
        if action.id == "LineageConfiguration":
            cp.deleteActions([index])
            logger.info(
                "removed LineageConfiguration from portal_controlpanel")
            break
        index += 1


def remove_utility(context):
    """unregister lineage utility
    """
    site = getSite()
    sm = site.getSiteManager()
    util = sm.queryUtility(ILineageConfiguration, name='lineage_config')
    sm.unregisterUtility(util, ILineageConfiguration, name='lineage_config')
    del util
    logger.info("removed utility 'lineage_config'")


def remove_interface(context):
    """remove ILineageConfiguration interface
    """
    pc = getToolByName(context, 'portal_catalog')
    brains = pc.searchResults()
    for b in brains:
        try:
            obj = b.getObject()
            noLongerProvides(obj, ILineageConfiguration)
        except:
            logger.error(
                "Could not remove ILineageConfiguration from %s" % obj.id)
            continue
