# -*- coding: utf-8 -*-
from collective.lineage.testing import LINEAGE_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

try:
    # BBB
    import unittest2 as unittest
except ImportError:
    import unittest

PROJECTNAME = 'collective.lineage'


class UtilsTestCase(unittest.TestCase):

    layer = LINEAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Site Administrator'])

        self.portal.invokeFactory(id='childsite', type_name='Folder')
        self.childsite = self.portal['childsite']

    def test_enable(self):
        from collective.lineage.interfaces import IChildSite
        from collective.lineage.utils import enable_childsite
        self.assertFalse(IChildSite.providedBy(self.childsite))
        enable_childsite(self.childsite)
        self.assertTrue(IChildSite.providedBy(self.childsite))

    def test_disable(self):
        from collective.lineage.interfaces import IChildSite
        from collective.lineage.utils import disable_childsite
        from collective.lineage.utils import enable_childsite

        enable_childsite(self.childsite)
        self.assertTrue(IChildSite.providedBy(self.childsite))
        disable_childsite(self.childsite)
        self.assertFalse(IChildSite.providedBy(self.childsite))
