import zope.interface
import zope.component
import zope.app.annotation.attribute

from p4a.subtyper import interfaces
from p4a.subtyper import default
from p4a.subtyper import engine
import Products.Archetypes.interfaces

from zope.app.component.interfaces import ISite
from zope.event import notify
from zope.app.publication.interfaces import BeforeTraverseEvent

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

import unittest
from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Testing import ZopeTestCase as ztc

from zope.app.component.hooks import getSite

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
        zope.component.provideAdapter(zope.app.annotation.attribute.AttributeAnnotations)
        zope.component.provideAdapter(default.folderish_possible_descriptors)
        class SimpleFolder(object):
            zope.interface.implements(Products.Archetypes.interfaces.IBaseFolder)
            portal_type = 'Folder'
        zope.interface.classImplements(SimpleFolder, zope.app.annotation.interfaces.IAttributeAnnotatable)

        adapted = interfaces.IPossibleDescriptors(SimpleFolder())
        self.failUnless(u'collective.lineage.childsite' in dict(adapted.possible).keys())

    def test_component_registry(self):
        self.login('contributor')
        self.portal.invokeFactory('Folder', 'site1')
        zope.component.provideUtility(engine.Subtyper())
        subtyper = zope.component.getUtility(interfaces.ISubtyper)
        subtyper.change_type(self.portal.site1, u'collective.lineage.childsite')
        self.failUnless(ISite.providedBy(self.portal.site1))

    def test_migration(self):
        """we are going to test the migration from 0.1 to >0.1"""
        # first create 3 old child folders
        # then run the migration upgrade step
        # we should end up with 3 activated folders containing the
        # same stuff as before
        roles = ('Member', 'Manager')
        self.portal.portal_membership.addMember('manager',
                                                'secret',
                                                roles, [])
        self.login('manager')

        # cf1
        self.portal.invokeFactory("Child Folder", "cf1")
        cf1 = self.portal.cf1
        cf1.setTitle("CF 1")
        cf1.setDescription("Description of CF 1")
        self.failUnless(cf1.Title() == "CF 1")
        self.failUnless(cf1.Description() == "Description of CF 1")

        cf1.invokeFactory("Document", "doc1")
        # add some text in the doc1 and a title
        cf1.invokeFactory("Document", "doc2")

        # cf2
        self.portal.invokeFactory("Child Folder", "cf2")
        cf2 = self.portal.cf2
        #cf3
        cf2.invokeFactory("Child Folder", "cf3")
        cf3 = cf2.cf3
        cf3.setTitle("CF 3")
        cf3.setDescription("Description of CF 3")
        self.failUnless(cf3.Title() == "CF 3")
        self.failUnless(cf3.Description() == "Description of CF 3")

        # Now run the migration step
        # then we test if cf1-3 are still existing
        # but are just normal folder that are subtyped
        # also check they still have the correct title
        # description and content


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IntegrationTests))
    return suite
