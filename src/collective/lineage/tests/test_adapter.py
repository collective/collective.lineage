from .. import testing
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility
from zope.component.hooks import setSite

PROJECTNAME = "collective.lineage"


class AdapterTestCase(testing.LineageTestCase):
    """
    Test adapter lookup in a child site.
    """

    def test_childsite_query_utility(self):
        from collective.lineage.utils import enable_childsite

        enable_childsite(self.portal.site1)
        setSite(self.portal.site1)
        queryUtility(IDexterityFTI, name="File")
