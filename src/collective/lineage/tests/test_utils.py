# -*- coding: utf-8 -*-
from collective.lineage import utils
from .. import testing

from plone.browserlayer import utils as layer_utils
from zope import component
from zope import interface

PROJECTNAME = 'collective.lineage'


class IChildSiteLayer(interface.Interface):
    """
    An example browser layer for a child site.
    """


class UtilsTestCase(testing.LineageTestCase):
    """
    Test the Lineage utility functions.
    """

    def test_enable(self):
        from collective.lineage.interfaces import IChildSite
        self.assertFalse(IChildSite.providedBy(self.childsite))
        utils.enable_childsite(self.childsite)
        self.assertTrue(IChildSite.providedBy(self.childsite))

    def test_disable(self):
        from collective.lineage.interfaces import IChildSite

        utils.enable_childsite(self.childsite)
        self.assertTrue(IChildSite.providedBy(self.childsite))
        utils.disable_childsite(self.childsite)
        self.assertFalse(IChildSite.providedBy(self.childsite))

    def test_childsite_browserlayer(self):
        """
        Child sites can have their own browser layer.
        """
        utils.enable_childsite(self.childsite)
        layer_utils.register_layer(
            IChildSiteLayer,
            'collective.lineage.childsite.layer',
            site_manager=component.getSiteManager((self.childsite)))

        self.assertFalse(
            IChildSiteLayer.providedBy(self.portal.REQUEST),
            'Child site browser layer applied prior to traversing')
        self.portal.REQUEST.traverse(
            '/'.join(self.childsite.getPhysicalPath()))
        self.assertTrue(
            IChildSiteLayer.providedBy(self.portal.REQUEST),
            'Child site browser layer not applied to the request')
