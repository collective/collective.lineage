"""
Test Lineage in the test browser.
"""

from .. import testing
from collective.lineage import utils
from plone.app import testing as pa_testing
from plone.testing import zope

import transaction


class TestLineageInBrowser(testing.LineageTestCase):
    """
    Test Lineage in the test browser.
    """

    layer = testing.LINEAGE_SERVER_TESTING

    def setUpBrowser(
        self,
        login=True,
        username=pa_testing.SITE_OWNER_NAME,
        password=pa_testing.SITE_OWNER_PASSWORD,
    ):
        """
        Start a logged in browser session.
        """
        app = self.layer["app"]
        browser = zope.Browser(app)
        browser.handleErrors = False  # Don't get HTTP 500 pages
        # Make ZODB changes accessible in the browser
        transaction.commit()

        if login:
            portal = self.layer["portal"]
            portal_url = portal.absolute_url()

            browser.open(portal_url + "/failsafe_login_form")
            browser.getControl(name="__ac_name").value = username
            browser.getControl(name="__ac_password").value = password
            browser.getControl("Log in").click()
            self.assertIn(
                "You are now logged in",
                browser.contents,
                "Missing login confirmation message",
            )

        return browser

    def test_browser_add_content(self):
        """
        Content can be added to child sites.
        """
        browser = self.setUpBrowser()

        browser.open(self.childsite.absolute_url())
        browser.getLink("Enable Subsite").click()
        # Check that the site was successfully enabled
        browser.getLink("Disable Subsite")

        browser.getLink("Page").click()
        add_form = browser.getForm(index=-1)

        self.assertNotIn(
            "foo-page-title",
            self.childsite.objectIds(),
            "Document present in child site before submitting add form",
        )

        add_form.getControl("Title").value = "Foo Page Title"
        add_form.getControl("Save").click()
        self.assertIn(
            "foo-page-title",
            self.childsite.objectIds(),
            "Document not present in child site after submitting add form",
        )

    def test_browser_disable_subsite(self):
        """
        Child site can be disabled.
        """
        utils.enable_childsite(self.childsite)
        transaction.commit()
        browser = self.setUpBrowser()
        browser.open(self.childsite.absolute_url())
        browser.getLink("Disable Subsite").click()
        self.assertIsNotNone(browser.getLink("Enable Subsite"))


class TestLinageUtilsView(testing.LineageTestCase):

    def setUp(self):
        super().setUp()
        utils.enable_childsite(self.childsite)

    def test_on_siteroot(self):
        view = self.portal.restrictedTraverse("lineageutils")
        self.assertFalse(view.isChildSite())
        self.assertIsNone(view.current_childsite)

    def test_on_childsite(self):
        view = self.childsite.restrictedTraverse("lineageutils")
        self.assertTrue(view.isChildSite())
        self.assertEqual(view.current_childsite, self.childsite)

    def test_on_childsite_content(self):
        doc_id = self.childsite.invokeFactory("Document", "d1", title="Test")
        document = self.childsite[doc_id]
        view = document.restrictedTraverse("lineageutils")
        self.assertTrue(view.isChildSite())
        self.assertEqual(view.current_childsite, self.childsite)
