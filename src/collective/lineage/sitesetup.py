from collective.lineage.interfaces import ILineageConfiguration
from collective.lineage.browser import LineageConfiguration


def setup_site(portal):
    sm = portal.getSiteManager()
    if not sm.queryUtility(ILineageConfiguration, name='lineage_config'):
        sm.registerUtility(
            LineageConfiguration(),
            ILineageConfiguration,
            'lineage_config')
