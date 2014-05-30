from Products.CMFCore.utils import getToolByName
from collective.lineage.interfaces import IChildSite
from collective.lineage.testing import LINEAGE_INTEGRATION_TESTING
from plone.testing import z2
import p4a.subtyper
import unittest2 as unittest
import zope.component
import zope.interface

try:
    # Plone < 4.3
    from zope.app.component.interfaces import ISite
except ImportError:
    # Plone >= 4.3
    from zope.component.interfaces import ISite


PROJECTNAME = 'collective.lineage'


class ChildSiteSubscriberTest(unittest.TestCase):

    layer = LINEAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        z2.login(self.portal['acl_users'], 'contributor')
        self.portal.invokeFactory('Folder', 'site1')
        zope.component.provideUtility(p4a.subtyper.engine.Subtyper())
        self.subtyper = zope.component.getUtility(
            p4a.subtyper.interfaces.ISubtyper)
        self.catalog = getToolByName(self.portal, 'portal_catalog')

    def test_enabling_child_site(self):
        self.subtyper.change_type(
            self.portal.site1,
            u'collective.lineage.childsite')
        res = self.catalog(object_provides=IChildSite.__identifier__)
        rids = [r.getRID() for r in res]
        rid = self.catalog.getrid('/plone/site1')
        self.assertIn(rid, rids)
        self.assertTrue(ISite.providedBy(self.portal.site1))

    def test_disabling_child_site(self):
        self.subtyper.change_type(
            self.portal.site1,
            u'collective.lineage.childsite')
        self.subtyper.remove_type(
            self.portal.site1)
        res = self.catalog(object_provides=IChildSite.__identifier__)
        rids = [r.getRID() for r in res]
        rid = self.catalog.getrid('/plone/site1')
        self.assertNotIn(rid, rids)
        self.assertFalse(ISite.providedBy(self.portal.site1))
