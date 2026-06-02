from collective.lineage import utils
from collective.lineage.testing import LineageTestCase
from plone.browserlayer import utils as layer_utils
from zope.component import getSiteManager
from zope.interface import Interface

PROJECTNAME = "collective.lineage"


class IChildSiteLayer(Interface):
    """
    An example browser layer for a child site.
    """


class UtilsTestCase(LineageTestCase):
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
            "collective.lineage.childsite.layer",
            site_manager=getSiteManager(self.childsite),
        )

        self.assertFalse(
            IChildSiteLayer.providedBy(self.portal.REQUEST),
            "Child site browser layer applied prior to traversing",
        )
        self.portal.REQUEST.traverse("/".join(self.childsite.getPhysicalPath()))
        self.assertTrue(
            IChildSiteLayer.providedBy(self.portal.REQUEST),
            "Child site browser layer not applied to the request",
        )
