from Products.CMFCore.utils import getToolByName

import zope.component
import transaction

from p4a.subtyper import engine
from p4a.subtyper import interfaces

def migrateChildFolders(context):
    """Migrates Child Folder objects to normal Folder objects
    that are subtyped"""
    # allow the Child Folder type to be addable
    pt = getToolByName(context, "portal_types")
    cf_type = pt["Child Folder"]
    cf_type.global_allow = True

    pc = getToolByName(context, 'portal_catalog')
    brains = pc.searchResults(portal_type="Child Folder")
    while brains:
        child_folder = brains[0].getObject()
        parent = child_folder.getParentNode()
        children_ids = child_folder.objectIds()

        cf_title = child_folder.Title()
        cf_desc = child_folder.Description()
        cf_id = child_folder.getId()
        cf_new_id = "%s-old" % cf_id
        parent.manage_renameObjects([cf_id], [cf_new_id])

        parent.invokeFactory("Folder", cf_id)
        new_folder = parent[cf_id]
        new_folder.setTitle(cf_title)
        new_folder.setDescription(cf_desc)
        new_folder.processForm()
        zope.component.provideUtility(engine.Subtyper())
        subtyper = zope.component.getUtility(interfaces.ISubtyper)
        subtyper.change_type(new_folder, u'collective.lineage.childsite')

        if children_ids:
            cut_items = child_folder.manage_cutObjects(ids=children_ids)
            new_folder.manage_pasteObjects(cut_items)

        parent.manage_delObjects([cf_new_id])
        transaction.savepoint()

        brains = pc.searchResults(portal_type="Child Folder")

    cf_type.global_allow = False

