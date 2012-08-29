import unittest2 as unittest
import zope.interface
import zope.component
from zope.component.interfaces import ISite
import zope.annotation.attribute as zaa
import zope.annotation.interfaces as zai
from AccessControl import Unauthorized
from Products.GenericSetup.upgrade import _upgrade_registry
import Products.Archetypes.interfaces
from five.localsitemanager import make_objectmanager_site
from plone.portlets.constants import (
    CONTEXT_CATEGORY,
    GROUP_CATEGORY,
    CONTENT_TYPE_CATEGORY,
)
from plone.portlets.interfaces import (
    ILocalPortletAssignable,
    ILocalPortletAssignmentManager,
    IPortletManager,
    IPortletType,
)
from p4a.subtyper import (
    interfaces,
    default,
    engine,
)
from plone.testing import z2
from collective.lineage.testing import (
    LINEAGE_INTEGRATION_TESTING,
    LINEAGE_MIGRATION_INTEGRATION_TESTING,
)


# TODO: move this case test to other modules
class IntegrationTests(unittest.TestCase):

    layer = LINEAGE_INTEGRATION_TESTING

    def test_folder_is_activatable(self):
        zope.component.provideAdapter(zaa.AttributeAnnotations)
        zope.component.provideAdapter(default.folderish_possible_descriptors)

        class SimpleFolder(object):
            zope.interface.implements(
                Products.Archetypes.interfaces.IBaseFolder)
            portal_type = 'Folder'

        zope.interface.classImplements(SimpleFolder,
                                       zai.IAttributeAnnotatable)

        adapted = interfaces.IPossibleDescriptors(SimpleFolder())
        self.failUnless(u'collective.lineage.childsite' in \
                            dict(adapted.possible).keys())

    def test_component_registry(self):
        portal = self.layer['portal']
        z2.login(portal['acl_users'], 'contributor')
        portal.invokeFactory('Folder', 'site1')
        zope.component.provideUtility(engine.Subtyper())
        subtyper = zope.component.getUtility(interfaces.ISubtyper)
        subtyper.change_type(
            portal.site1,
            u'collective.lineage.childsite')
        self.failUnless(ISite.providedBy(portal.site1))

    # TODO: this should be moved to test_setup.py
    def test_uninstall(self):
        """testing the uninstall of collective.lineage"""
        portal = self.layer['portal']
        z2.login(portal['acl_users'], 'manager')
        portal.portal_quickinstaller.uninstallProducts(["collective.lineage"])
        zope.component.provideAdapter(zaa.AttributeAnnotations)
        zope.component.provideAdapter(default.folderish_possible_descriptors)

        class SimpleFolder(object):
            zope.interface.implements(
                Products.Archetypes.interfaces.IBaseFolder)
            portal_type = 'Folder'

        zope.interface.classImplements(SimpleFolder,
                                       zai.IAttributeAnnotatable)

        adapted = interfaces.IPossibleDescriptors(SimpleFolder())
        self.failUnless(u'collective.lineage.childsite' not in \
                            dict(adapted.possible).keys())


class MigrationTests(unittest.TestCase):
    """we are going to test the migration from 0.1 to >0.1"""

    layer = LINEAGE_MIGRATION_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        wf = self.portal.portal_workflow
        wf.setDefaultChain('simple_publication_workflow')
        self.portal.portal_types["Child Folder"].global_allow = True

    def run_migration_step(self):
        import transaction
        transaction.savepoint()
        # Now run the migration step
        profile_id = "collective.lineage:default"
        setup_tool = self.layer['portal'].portal_setup
        steps_to_run = _upgrade_registry.getUpgradeStepsForProfile(profile_id)
        for step_id in steps_to_run:
            step = _upgrade_registry.getUpgradeStep(profile_id, step_id)
            if step is not None:
                if step.title == "Migrate the Child Folder objects":
                    step.doStep(setup_tool)

    def test_migration(self):
        # cf1
        portal = self.layer['portal']
        z2.login(portal['acl_users'], 'manager')
        portal.invokeFactory("Child Folder", "cf1")
        cf1 = portal.cf1
        cf1.setTitle("CF 1")
        cf1.setDescription("Description of CF 1")
        cf1.layout = "layout1"
        pw = portal.portal_workflow
        pw.doActionFor(cf1, "publish")
        self.failUnless(cf1.Title() == "CF 1")
        self.failUnless(cf1.Description() == "Description of CF 1")
        self.failUnless(pw.getInfoFor(cf1, "review_state") == "published")
        self.failUnless(cf1.layout == "layout1")

        cf1.invokeFactory("Document", "doc1")
        cf1.invokeFactory("Document", "doc2")
        doc1 = cf1["doc1"]
        doc1.setTitle("Doc 1")
        doc1.setDescription("Description of Doc 1")
        doc1.setText("<p>Some Text here</p>")

        # cf2
        portal.invokeFactory("Child Folder", "cf2")
        cf2 = portal.cf2

        #cf3
        cf2.invokeFactory("Child Folder", "cf3")
        cf3 = cf2.cf3
        cf3.setTitle("CF 3")
        cf3.setDescription("Description of CF 3")
        cf3.layout = "3layout"
        pw.doActionFor(cf3, "publish")
        self.failUnless(cf3.Title() == "CF 3")
        self.failUnless(cf3.Description() == "Description of CF 3")
        self.failUnless(pw.getInfoFor(cf3, "review_state") == "published")

        cf3.invokeFactory("Document", "doc1")
        cf3.invokeFactory("Document", "doc2")
        doc1 = cf3["doc1"]
        doc1.setTitle("Doc 1")
        doc1.setDescription("Description of Doc 1")
        doc1.setText("<p>Some Text here</p>")

        self.run_migration_step()

        # then we test if cf1-3 are still existing
        # but are just normal folder that are subtyped
        # also check they still have the correct title
        # description, content, state and layout
        cf1 = portal.cf1
        cf2 = portal.cf2
        cf3 = cf2.cf3
        doc1 = cf3.doc1
        self.failUnless(cf1.Title() == "CF 1")
        self.failUnless(pw.getInfoFor(cf1, "review_state") == "published")
        self.failUnless(cf1.layout == "layout1")
        self.failUnless(cf3.Title() == "CF 3")
        self.failUnless(cf3.Description() == "Description of CF 3")
        self.failUnless(cf3.layout == "3layout")
        self.failUnless(pw.getInfoFor(cf3, "review_state") == "published")
        self.failUnless(cf1.portal_type == "Folder")
        self.failUnless(cf3.portal_type == "Folder")
        self.failUnless(doc1.getRawText() == "<p>Some Text here</p>")

        #check that anonymous can see the published items
        z2.logout()
        try:
            cf1_item = portal.restrictedTraverse("cf1")
        except Unauthorized:
            cf1_item = None
        self.failUnless(cf1_item != None)

    def test_migration_preserves_default_view(self):
        portal = self.layer['portal']
        z2.login(portal['acl_users'], 'manager')
        portal.invokeFactory("Child Folder", "cf1")
        cf1 = portal.cf1
        cf1.setTitle("CF 1")
        pw = portal.portal_workflow
        pw.doActionFor(cf1, "publish")
        self.failUnless(cf1.Title() == "CF 1")
        self.failUnless(pw.getInfoFor(cf1, "review_state") == "published")
        cf1.invokeFactory("Document", "doc1")
        doc1 = cf1["doc1"]
        doc1.setTitle("Doc 1")
        cf1.setDefaultPage("doc1")
        self.run_migration_step()
        cf1 = portal.cf1
        self.assertEquals(cf1.getDefaultPage(), "doc1")

    def test_migration_preserves_portlets(self):
        portal = self.layer['portal']
        z2.login(portal['acl_users'], 'manager')
        portal.invokeFactory("Child Folder", "cf1")
        cf1 = portal.cf1
        cf1.setTitle("CF 1")
        make_objectmanager_site(cf1)
        pw = portal.portal_workflow
        pw.doActionFor(cf1, "publish")
        self.failUnless(cf1.Title() == "CF 1")
        self.failUnless(pw.getInfoFor(cf1, "review_state") == "published")
        self.failUnless(ISite.providedBy(cf1))
        # Child folders in 0.1 seemed to provide ILocalPortletAssignable but
        # not in 0.6
        if not ILocalPortletAssignable.providedBy(cf1):
            zope.interface.alsoProvides(cf1, ILocalPortletAssignable)
            added_portlet_assignable_interace = True
        else:
            added_portlet_assignable_interace = False

        mapping = cf1.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        portlet = zope.component.getUtility(IPortletType,
                                            name='plone.portlet.static.Static')
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={
            'header': u"test title",
            'text': u"test text"})
        self.assertEquals(len(mapping), 1)

        left_col_manager = zope.component.getUtility(
            IPortletManager,
            name='plone.leftcolumn',
            context=cf1)
        assignment_manager = zope.component.getMultiAdapter(
            (cf1, left_col_manager),
            ILocalPortletAssignmentManager)
        assignment_manager.setBlacklistStatus(GROUP_CATEGORY, None)
        assignment_manager.setBlacklistStatus(CONTENT_TYPE_CATEGORY, False)

        if added_portlet_assignable_interace:
            zope.interface.noLongerProvides(cf1, ILocalPortletAssignable)

        self.run_migration_step()

        cf1 = portal.cf1
        mapping = cf1.restrictedTraverse('++contextportlets++plone.leftcolumn')
        self.assertEquals(len(mapping), 1)

        left_col_manager = zope.component.getUtility(
            IPortletManager,
            name='plone.leftcolumn',
            context=cf1)
        assignment_manager = zope.component.getMultiAdapter(
            (cf1, left_col_manager),
            ILocalPortletAssignmentManager)
        self.assertTrue(
            assignment_manager.getBlacklistStatus(CONTEXT_CATEGORY))
        self.assertTrue(
            assignment_manager.getBlacklistStatus(GROUP_CATEGORY) is None)
        self.assertFalse(
            assignment_manager.getBlacklistStatus(CONTENT_TYPE_CATEGORY))

    def test_migration_preserves_references(self):
        portal = self.layer['portal']
        z2.login(portal['acl_users'], 'manager')
        portal.invokeFactory("Child Folder", "cf1")
        cf1 = portal.cf1
        cf1.setTitle("CF 1")
        make_objectmanager_site(cf1)
        pw = portal.portal_workflow
        pw.doActionFor(cf1, "publish")
        self.failUnless(cf1.Title() == "CF 1")
        self.failUnless(pw.getInfoFor(cf1, "review_state") == "published")
        self.failUnless(ISite.providedBy(cf1))

        cf1.invokeFactory("Document", "doc1", Title="Doc 1")
        doc1 = cf1["doc1"]
        cf1.setDefaultPage("doc1")

        doc2_text = (
            '<p><a href="resolveuid/%s" class="internal">Link to doc 1'
            '</a></p>') % doc1.UID()
        cf1.invokeFactory("Document", "doc2", Title="Doc 2", text=doc2_text)
        doc2 = cf1["doc2"]
        # I'm not sure what layer of Plone code adds these
        doc2.addReference(doc1, 'isReferencing', updateReferences=True)
        self.assertEquals(
            len(doc2._getReferenceAnnotations().objectItems()), 1)

        self.run_migration_step()

        cf1 = portal.cf1
        doc2 = cf1["doc2"]
        self.assertEquals(
            len(doc2._getReferenceAnnotations().objectItems()), 1)

    def test_migration_preserves_sharing_settings(self):
        portal = self.layer['portal']
        z2.login(portal['acl_users'], 'manager')
        portal.invokeFactory("Child Folder", "cf1")
        cf1 = portal.cf1
        cf1.setTitle("CF 1")
        make_objectmanager_site(cf1)
        pw = portal.portal_workflow
        pw.doActionFor(cf1, "publish")
        self.failUnless(cf1.Title() == "CF 1")
        self.failUnless(pw.getInfoFor(cf1, "review_state") == "published")
        self.failUnless(ISite.providedBy(cf1))

        cf1.manage_setLocalRoles('testuser', ['Contributor'])

        self.run_migration_step()

        cf1 = portal.cf1
        self.assertEquals(
            ('Contributor',), cf1.get_local_roles_for_userid('testuser'))
