import zope.interface
import zope.component

#for plone3-plone4 compatibility purposes
try:
    import zope.app.annotation.attribute as zaa
except:
    import zope.annotation.attribute as zaa
try:
    import zope.app.annotation.interfaces as zai
except:
    import zope.annotation.interfaces as zai


from p4a.subtyper import interfaces
from p4a.subtyper import default
from p4a.subtyper import engine
import Products.Archetypes.interfaces

from zope.app.component.interfaces import ISite

from Products.CMFCore.utils import getToolByName

from Products.GenericSetup.upgrade import _upgrade_registry

import unittest
from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Testing import ZopeTestCase as ztc

@onsetup
def setup_package():
    fiveconfigure.debug_mode = True
    import collective.lineage
    zcml.load_config('configure.zcml', collective.lineage)
    fiveconfigure.debug_mode = False
    ztc.installPackage('collective.lineage')

setup_package()
ptc.setupPloneSite(products=['collective.lineage'])


class IntegrationTests(ptc.PloneTestCase):

    def afterSetUp(self):
        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor',
                                                'secret',
                                                roles, [])

    def test_folder_is_activatable(self):
        zope.component.provideAdapter(zaa.AttributeAnnotations)
        zope.component.provideAdapter(default.folderish_possible_descriptors)
        class SimpleFolder(object):
            zope.interface.implements(Products.Archetypes.interfaces.IBaseFolder)
            portal_type = 'Folder'
        zope.interface.classImplements(SimpleFolder,
                                       zai.IAttributeAnnotatable)

        adapted = interfaces.IPossibleDescriptors(SimpleFolder())
        self.failUnless(u'collective.lineage.childsite' in \
                            dict(adapted.possible).keys())

    def test_component_registry(self):
        self.login('contributor')
        self.portal.invokeFactory('Folder', 'site1')
        zope.component.provideUtility(engine.Subtyper())
        subtyper = zope.component.getUtility(interfaces.ISubtyper)
        subtyper.change_type(self.portal.site1, u'collective.lineage.childsite')
        self.failUnless(ISite.providedBy(self.portal.site1))

    def test_migration(self):
        """we are going to test the migration from 0.1 to >0.1"""
        roles = ('Member', 'Manager')
        self.portal.portal_membership.addMember('manager',
                                                'secret',
                                                roles, [])
        self.login('manager')
        pw = getToolByName(self.portal, "portal_workflow")

        # allow the Child Folder type to be addable
        pt = getToolByName(self.portal, "portal_types")
        cf_type = pt["Child Folder"]
        cf_type.global_allow = True

        # cf1
        self.portal.invokeFactory("Child Folder", "cf1")
        cf1 = self.portal.cf1
        cf1.setTitle("CF 1")
        cf1.setDescription("Description of CF 1")
        pw.doActionFor(cf1, "publish")
        self.failUnless(cf1.Title() == "CF 1")
        self.failUnless(cf1.Description() == "Description of CF 1")
        self.failUnless(pw.getInfoFor(cf1, "review_state") == "published")

        cf1.invokeFactory("Document", "doc1")
        cf1.invokeFactory("Document", "doc2")
        doc1 = cf1["doc1"]
        doc1.setTitle("Doc 1")
        doc1.setDescription("Description of Doc 1")
        doc1.setText("<p>Some Text here</p>")

        # cf2
        self.portal.invokeFactory("Child Folder", "cf2")
        cf2 = self.portal.cf2

        #cf3
        cf2.invokeFactory("Child Folder", "cf3")
        cf3 = cf2.cf3
        cf3.setTitle("CF 3")
        cf3.setDescription("Description of CF 3")
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

        import transaction; transaction.savepoint();
        # Now run the migration step
        profile_id = "collective.lineage:default"
        setup_tool = getToolByName(self.portal, 'portal_setup')
        steps_to_run = _upgrade_registry.getUpgradeStepsForProfile(profile_id)

        for step_id in steps_to_run:
            step = _upgrade_registry.getUpgradeStep(profile_id, step_id)
            if step is not None:
                if step.title == "Migrate the Child Folder objects":
                    step.doStep(setup_tool)

        # then we test if cf1-3 are still existing
        # but are just normal folder that are subtyped
        # also check they still have the correct title
        # description and content
        cf1 = self.portal.cf1
        cf2 = self.portal.cf2
        cf3 = cf2.cf3
        doc1 = cf3.doc1
        self.failUnless(cf1.Title() == "CF 1")
        self.failUnless(pw.getInfoFor(cf1, "review_state") == "published")
        self.failUnless(cf3.Title() == "CF 3")
        self.failUnless(cf3.Description() == "Description of CF 3")
        self.failUnless(pw.getInfoFor(cf3, "review_state") == "published")
        self.failUnless(cf1.portal_type == "Folder")
        self.failUnless(cf3.portal_type == "Folder")
        self.failUnless(doc1.getRawText() == "<p>Some Text here</p>")

    def test_uninstall(self):
        """testing the uninstall of collective.lineage"""
        roles = ('Member', 'Manager')
        self.portal.portal_membership.addMember('manager',
                                                'secret',
                                                roles, [])
        self.login('manager')
        pq = getToolByName(self.portal, "portal_quickinstaller")
        pq.uninstallProducts(["collective.lineage"])

        zope.component.provideAdapter(zaa.AttributeAnnotations)
        zope.component.provideAdapter(default.folderish_possible_descriptors)
        class SimpleFolder(object):
            zope.interface.implements(Products.Archetypes.interfaces.IBaseFolder)
            portal_type = 'Folder'

        zope.interface.classImplements(SimpleFolder,
                                       zai.IAttributeAnnotatable)

        adapted = interfaces.IPossibleDescriptors(SimpleFolder())
        self.failUnless(u'collective.lineage.childsite' not in \
                            dict(adapted.possible).keys())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IntegrationTests))
    return suite

