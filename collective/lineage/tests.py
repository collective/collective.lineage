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
    
    def test_add_childfolder(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Child Folder', 'site1')
        self.failUnless('site1' in self.portal.objectIds())
    
    def test_component_registry(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Child Folder', 'site1')
        self.failUnless(ISite.providedBy(self.portal.site1))
        
        # Simulate traversal
        notify(BeforeTraverseEvent(self.portal.site1, self.portal.REQUEST))
        self.assertEqual(getSite().getPhysicalPath(), self.portal.site1.getPhysicalPath())
    
    def test_search_root(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Child Folder', 'site1')
        
        self.portal.invokeFactory('Document', 'd1')
        self.portal.site1.invokeFactory('Document', 'd2')

        catalog = getToolByName(self.portal, 'portal_catalog')

        lazy = catalog(portal_type='Document')
        results = [x.getId for x in lazy]
        self.failUnless('d1' in results)
        self.failUnless('d2' in results)

        # Simulate traversal
        notify(BeforeTraverseEvent(self.portal.site1, self.portal.REQUEST))
        
        lazy = catalog(portal_type='Document')
        results = [x.getId for x in lazy]
        self.failIf('d1' in results)
        self.failUnless('d2' in results)
    
    def test_search_root_with_explicit_path(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Child Folder', 'site1')
        
        self.portal.invokeFactory('Document', 'd1')
        self.portal.site1.invokeFactory('Document', 'd2')

        catalog = getToolByName(self.portal, 'portal_catalog')

        lazy = catalog(portal_type='Document', path='/'.join(self.portal.getPhysicalPath()))
        results = [x.getId for x in lazy]
        self.failUnless('d1' in results)
        self.failUnless('d2' in results)

        # Simulate traversal
        notify(BeforeTraverseEvent(self.portal.site1, self.portal.REQUEST))
        
        lazy = catalog(portal_type='Document', path='/'.join(self.portal.getPhysicalPath()))
        results = [x.getId for x in lazy]
        self.failUnless('d1' in results)
        self.failUnless('d2' in results)
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IntegrationTests))
    return suite
