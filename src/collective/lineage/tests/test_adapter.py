from collective.lineage.testing import LINEAGE_INTEGRATION_TESTING
from plone.app.imaging.interfaces import IImagingSchema
from plone.app.imaging.traverse import ImageTraverser
from plone.testing import z2
from zope.component import getGlobalSiteManager
import p4a.subtyper
import unittest2 as unittest
import zope.component

PROJECTNAME = 'collective.lineage'


class AdapterTestCase(unittest.TestCase):

    layer = LINEAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        z2.login(self.portal['acl_users'], 'contributor')
        self.portal.invokeFactory('Folder', 'site1')
        zope.component.provideUtility(p4a.subtyper.engine.Subtyper())
        self.subtyper = zope.component.getUtility(
            p4a.subtyper.interfaces.ISubtyper)
        self.subtyper.change_type(
            self.portal.site1,
            u'collective.lineage.childsite')

    def test_adapter_registered_correctly(self):
        sm = getGlobalSiteManager()
        registrations = [a for a in sm.registeredAdapters()
                         if a.provided == IImagingSchema]
        self.assertEqual(len(registrations), 1)

    def test_childsite_is_image_traverser(self):
        child_site = IImagingSchema(self.portal.site1)
        self.assertIs(child_site, ImageTraverser)
