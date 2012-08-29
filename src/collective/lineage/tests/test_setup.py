# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from collective.lineage.testing import LINEAGE_INTEGRATION_TESTING

PROJECTNAME = 'collective.lineage'


class InstallTestCase(unittest.TestCase):

    layer = LINEAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal.portal_quickinstaller

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_dependencies_installed(self):
        self.assertTrue(self.qi.isProductInstalled('p4a.subtyper'))

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
        self.qi = self.portal.portal_quickinstaller
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertFalse('ILineageBrowserLayer' in layers,
                         'add-on layer was not removed')
