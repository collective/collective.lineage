import urlparse

from zope.component import getUtility

from OFS.absoluteurl import AbsoluteURL

from plone.registry.interfaces import IRegistry

from collective.lineage.interfaces import ILineageSettings


class LineageAbsoluteURL(AbsoluteURL):
    """An absolute_url adapter for generic objects in Zope 2 that
    checks if the context is inside an IChildSite with a customized
    URL.
    """
    def __str__(self):
        mapped_url = map_url('/'.join(self.context.getPhysicalPath()),
                             self.request)
        if mapped_url is None:
            return super(LineageAbsoluteURL, self).__str__()
        else:
            return mapped_url


def map_url(path, request):
    """Given a path in the site, apply any URL transforms
    stored in the registry. Returns None if no map exists for the given path.
    """
    # Be careful to not try to retrieve the object
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ILineageSettings)
    vhm_map = getattr(settings, 'vhm_map', {})
    child_site_netloc = ''
    scheme = urlparse.urlparse(request.getURL())[0]

    # We want to sort by descending path distance,
    # so that deeper child sites don't get incorrectly swallowed
    # by parent child sites
    roots = sorted(vhm_map.keys(), key=lambda x: -len(x.split('/')))
    for site_mgr_root in roots:
        child_site_netloc = urlparse.urlparse(vhm_map[site_mgr_root])[1]
        if path.startswith(site_mgr_root):
            break

    if not child_site_netloc or not site_mgr_root:
        # Didn't find any defined maps for this path
        return None

    my_relative_path = path.partition(site_mgr_root)[-1]

    url = urlparse.urlunsplit([
        scheme,
        child_site_netloc,
        my_relative_path,
        '',
        ''
    ])
    return url
