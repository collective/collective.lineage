# -*- coding: utf-8 -*-
from collective.lineage.testing import LINEAGE_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.browserlayer.utils import registered_layers


try:
    # BBB
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    # BBB for Plone 5.0 and lower.
    get_installer = None


PROJECTNAME = 'collective.lineage'


class InstallTestCase(unittest.TestCase):

    layer = LINEAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer is None:
            self.qi = self.portal.portal_quickinstaller
        else:
            self.qi = get_installer(self.portal)

    def test_installed(self):
        if get_installer is None:
            self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))
        else:
            self.assertTrue(self.qi.is_product_installed(PROJECTNAME))

    def test_addon_layer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('ILineageBrowserLayer' in layers,
                        'add-on layer was not installed')

    # TODO: test propertiestool and viewlets


class UninstallTest(unittest.TestCase):

    layer = LINEAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        if get_installer is None:
            self.qi = self.portal.portal_quickinstaller
            self.qi.uninstallProducts(products=[PROJECTNAME])
        else:
            self.qi = get_installer(self.portal)
            self.qi.uninstall_product(PROJECTNAME)

    def test_uninstalled(self):
        """
        The Lineage Add-on is uninstalled by default.
        """
        if get_installer is None:
            is_installed = self.qi.isProductInstalled(PROJECTNAME)
        else:
            is_installed = self.qi.is_product_installed(PROJECTNAME)
        self.assertFalse(is_installed, 'Lineage installed by default')

    def test_addon_layer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertFalse('ILineageBrowserLayer' in layers,
                         'add-on layer was not removed')
