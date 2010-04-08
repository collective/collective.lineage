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
import unittest
from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from zope.app.component.hooks import getSite

@onsetup
def setup_package():
    fiveconfigure.debug_mode = True
    import collective.lineage
    zcml.load_config('configure.zcml', collective.lineage)
    fiveconfigure.debug_mode = False
    
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

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IntegrationTests))
    return suite
