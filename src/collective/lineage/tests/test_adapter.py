# -*- coding: utf-8 -*-
from collective.lineage.testing import LINEAGE_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getGlobalSiteManager

try:
    # BBB
    import unittest2 as unittest
except ImportError:
    import unittest

PROJECTNAME = 'collective.lineage'


class AdapterTestCase(unittest.TestCase):

    layer = LINEAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Site Administrator'])
        self.portal.invokeFactory('Folder', 'site1')

    def test_adapter_registered_correctly(self):
        """this test is ATCT only"""
        if self.layer['has_pact']:
            return
        from plone.app.imaging.interfaces import IImagingSchema

        sm = getGlobalSiteManager()
        registrations = [a for a in sm.registeredAdapters()
                         if a.provided == IImagingSchema]
        self.assertEqual(len(registrations), 1)

    def test_childsite_is_image_traverser(self):
        """this test is ATCT only"""
        if self.layer['has_pact']:
            return
        from plone.app.imaging.interfaces import IImagingSchema
        from plone.app.imaging.configlet import ImagingControlPanelAdapter
        from collective.lineage.utils import enable_childsite
        enable_childsite(self.portal.site1)
        configuration = IImagingSchema(self.portal.site1)
        self.assertIsInstance(configuration, ImagingControlPanelAdapter)
