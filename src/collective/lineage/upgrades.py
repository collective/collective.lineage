from DateTime import DateTime

from logging import getLogger

from p4a.subtyper import engine
from p4a.subtyper import interfaces

from plone.app.layout.navigation.defaultpage import getDefaultPage
from plone.portlets.interfaces import ILocalPortletAssignable
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.constants import GROUP_CATEGORY
from plone.portlets.constants import CONTENT_TYPE_CATEGORY

from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr

from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import getUtilitiesFor
from zope.component import queryUtility
from zope.component import provideUtility
from zope.app.component.hooks import getSite

from collective.lineage.interfaces import ILineageConfiguration
from collective.lineage.interfaces import ILineageSettings

import transaction

logger = getLogger('collective.lineage.upgrades')


def migrateChildFolders(context):
    """Migrates Child Folder objects to normal Folder objects
    that are subtyped"""
    logger.info('Migrating child folder objects to normal folder objects')
    # allow the Child Folder type to be addable
    pt = getToolByName(context, "portal_types")
    pw = getToolByName(context, "portal_workflow")
    cf_type = pt["Child Folder"]
    cf_type.global_allow = True

    pc = getToolByName(context, 'portal_catalog')
    brains = pc.searchResults(portal_type="Child Folder")
    while brains:
        child_folder = brains[0].getObject()
        logger.info('Migrating child folder %s' % child_folder.getId())
        parent = child_folder.getParentNode()
        # we will keep the same state, title, description, id
        # and display
        cf_state = pw.getInfoFor(child_folder, "review_state")
        cf_wf = pw.getDefaultChainFor(child_folder)
        cf_wf = cf_wf and cf_wf[0]
        cf_title = child_folder.Title()
        cf_desc = child_folder.Description()
        cf_orig_id = child_folder.getId()
        has_layout = base_hasattr(child_folder, "layout")
        if has_layout:
            cf_display = child_folder.layout
        cf_default_page = getDefaultPage(child_folder)
        f_temp_id = '%s-temp' % cf_orig_id

        parent.invokeFactory("Folder", f_temp_id)
        new_folder = parent[f_temp_id]
        new_folder.setTitle(cf_title)
        new_folder.setDescription(cf_desc)
        if has_layout:
            new_folder.layout = cf_display
        new_folder.processForm()
        provideUtility(engine.Subtyper())
        subtyper = getUtility(interfaces.ISubtyper)
        subtyper.change_type(new_folder, u'collective.lineage.childsite')

        if cf_wf:
            new_state = {
                'actor': 'Administrator',
                'action': None,
                'review_state': cf_state,
                'time': DateTime(),
                'comments': 'setting up the workflow of the item correctly',
                }
            pw.setStatusOf(cf_wf, new_folder, new_state)
            new_folder.reindexObject()

        children_ids = child_folder.objectIds()
        if children_ids:
            cut_items = child_folder.manage_cutObjects(ids=children_ids)
            new_folder.manage_pasteObjects(cut_items)
        if cf_default_page:
            new_folder.setDefaultPage(cf_default_page)
        copy_portlet_assignments_and_settings(child_folder, new_folder)
        copy_sharing_settings(child_folder, new_folder)

        parent.manage_delObjects([cf_orig_id])
        transaction.savepoint()
        parent.manage_renameObjects([f_temp_id], [cf_orig_id])
        transaction.savepoint()
        brains = pc.searchResults(portal_type="Child Folder")

    pw.updateRoleMappings()
    cf_type.global_allow = False
    logger.info('Finished migrating child folders')


def copy_sharing_settings(src, target):
    # copying the sharing roles
    sharing_view = getMultiAdapter((src, src.REQUEST), name="sharing")
    sharing_settings = sharing_view.existing_role_settings()
    for user_sharing_setting in sharing_settings:
        # may equally be a group but doesn't matter
        user_id = user_sharing_setting['id']
        user_roles_set_here = [role_id
                        for role_id, explicitly_set in \
                               user_sharing_setting['roles'].items()
                        if explicitly_set]
        if user_roles_set_here:
            target.manage_setLocalRoles(user_id, user_roles_set_here)
    # copying the inheritance
    target_sharing_view = getMultiAdapter((target, target.REQUEST),
                                           name="sharing")
    target_sharing_view.update_inherit(sharing_view.inherited())


def copy_portlet_assignments_and_settings(src, target):
    if not ILocalPortletAssignable.providedBy(src):
        alsoProvides(src, ILocalPortletAssignable)
    src_utilities = getUtilitiesFor(IPortletManager, context=src)
    for manager_name, src_manager in src_utilities:
        src_manager_assignments = getMultiAdapter(
            (src, src_manager),
            IPortletAssignmentMapping)
        target_manager = queryUtility(
            IPortletManager,
            name=manager_name,
            context=target)
        if target_manager is None:
            logger.warning('New folder %s does not have portlet manager %s' %
                           (target.getId(), target_manager))
        else:
            target_manager_assignments = getMultiAdapter(
                (target, target_manager),
                IPortletAssignmentMapping)
            for id, assignment in src_manager_assignments.items():
                target_manager_assignments[id] = assignment
            src_assignment_manager = getMultiAdapter(
                (src, src_manager),
                ILocalPortletAssignmentManager)
            target_assignment_manager = getMultiAdapter(
                (target, target_manager),
                ILocalPortletAssignmentManager)
            #
            # In lineage 0.1 child folders did not inherit their parent's
            # portlets no matter what porlet block settings were set.
            #
            target_assignment_manager.setBlacklistStatus(
                CONTEXT_CATEGORY, True)
            for category in (GROUP_CATEGORY, CONTENT_TYPE_CATEGORY):
                target_assignment_manager.setBlacklistStatus(
                    category,
                    src_assignment_manager.getBlacklistStatus(category))


def migrateControlPanel(context):
    """keep existing settings for 'menu_text' intact,
       delete the lineage_properties from portal_properties,
       un-register/remove the 'lineage_config' utility,
       remove the ILineageConfiguration interface
    """
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
