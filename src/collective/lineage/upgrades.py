from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

import zope.component
import transaction

from p4a.subtyper import engine
from p4a.subtyper import interfaces

def migrateChildFolders(context):
    """Migrates Child Folder objects to normal Folder objects
    that are subtyped"""
    # allow the Child Folder type to be addable
    pt = getToolByName(context, "portal_types")
    pw = getToolByName(context, "portal_workflow")
    cf_type = pt["Child Folder"]
    cf_type.global_allow = True

    pc = getToolByName(context, 'portal_catalog')
    brains = pc.searchResults(portal_type="Child Folder")
    while brains:
        child_folder = brains[0].getObject()
        parent = child_folder.getParentNode()
        children_ids = child_folder.objectIds()

        # we will keep the same state, title, description, id
        # and display
        cf_state = pw.getInfoFor(child_folder, "review_state")
        cf_wf = pw.getDefaultChainFor(child_folder)
        cf_wf = cf_wf and cf_wf[0]
        cf_title = child_folder.Title()
        cf_desc = child_folder.Description()
        cf_id = child_folder.getId()
        has_layout = hasattr(child_folder, "layout")
        if has_layout:
            cf_display = child_folder.layout
        cf_new_id = "%s-old" % cf_id
        parent.manage_renameObjects([cf_id], [cf_new_id])

        parent.invokeFactory("Folder", cf_id)
        new_folder = parent[cf_id]
        new_folder.setTitle(cf_title)
        new_folder.setDescription(cf_desc)
        if has_layout:
            new_folder.layout = cf_display
        new_folder.processForm()
        zope.component.provideUtility(engine.Subtyper())
        subtyper = zope.component.getUtility(interfaces.ISubtyper)
        subtyper.change_type(new_folder, u'collective.lineage.childsite')

        if cf_wf:
            new_state = {
                'actor': 'Administrator',
                'action': None,
                'review_state':cf_state,
                'time': DateTime(),
                'comments': 'setting up the workflow of the item correctly',
                }
            pw.setStatusOf(cf_wf, new_folder, new_state)
            new_folder.reindexObject()


        if children_ids:
            cut_items = child_folder.manage_cutObjects(ids=children_ids)
            new_folder.manage_pasteObjects(cut_items)

        parent.manage_delObjects([cf_new_id])
        transaction.savepoint()

        brains = pc.searchResults(portal_type="Child Folder")

    pw.updateRoleMappings()
    cf_type.global_allow = False

