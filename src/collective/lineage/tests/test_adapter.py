# -*- coding: utf-8 -*-

from zope.component import getGlobalSiteManager
from zope.component import queryUtility
from zope.component.hooks import setSite

from plone.dexterity.interfaces import IDexterityFTI

from .. import testing

PROJECTNAME = 'collective.lineage'


class AdapterTestCase(testing.LineageTestCase):
    """
    Test adapter lookup in a child site.
    """

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

    def test_childsite_query_utility(self):
        from collective.lineage.utils import enable_childsite
        enable_childsite(self.portal.site1)
        setSite(self.portal.site1)
        queryUtility(IDexterityFTI, name="File")
