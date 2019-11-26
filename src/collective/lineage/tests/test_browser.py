"""
Test Lineage in the test browser.
"""

import transaction

try:
    from plone.testing import zope
except ImportError:
    # BBB Plone 5.1
    from plone.testing import z2 as zope
from plone.app import testing as pa_testing

from .. import testing


class TestLineageInBrowser(testing.LineageTestCase):
    """
    Test Lineage in the test browser.
    """

    layer = testing.LINEAGE_SERVER_TESTING

    def setUpBrowser(
            self, login=True,
            username=pa_testing.SITE_OWNER_NAME,
            password=pa_testing.SITE_OWNER_PASSWORD):
        """
        Start a logged in browser session.
        """
        app = self.layer['app']
        browser = zope.Browser(app)
        browser.handleErrors = False  # Don't get HTTP 500 pages
        # Make ZODB changes accessible in the browser
        transaction.commit()

        if login:
            portal = self.layer['portal']
            portal_url = portal.absolute_url()

            browser.open(portal_url + '/failsafe_login_form')
            browser.getControl(
                name='__ac_name').value = username
            browser.getControl(
                name='__ac_password').value = password
            browser.getControl('Log in').click()
            self.assertIn(
                "You are now logged in", browser.contents,
                'Missing login confirmation message')

        return browser

    def test_browser_add_content(self):
        """
        Content can be added to child sites.
        """
        browser = self.setUpBrowser()

        browser.open(self.childsite.absolute_url())
        browser.getLink('Enable Subsite').click()
        # Check that the site was successfully enabled
        browser.getLink('Disable Subsite')

        browser.getLink('Page').click()
        add_form = browser.getForm(index=-1)

        self.assertNotIn(
            'foo-page-title', self.childsite.objectIds(),
            'Document present in child site before submitting add form')

        add_form.getControl('Title').value = 'Foo Page Title'
        add_form.getControl('Save').click()
        self.assertIn(
            'foo-page-title', self.childsite.objectIds(),
            'Document not present in child site after submitting add form')
