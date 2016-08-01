import urlparse

from Acquisition import aq_acquire
from ZPublisher.BaseRequest import quote

from zope.component import getUtility

from OFS.absoluteurl import AbsoluteURL, OFSTraversableAbsoluteURL
from OFS.interfaces import ITraversable

from plone.registry.interfaces import IRegistry

from collective.lineage.interfaces import ILineageSettings, IChildSite


class LineageAbsoluteURL(OFSTraversableAbsoluteURL):
    """An absolute_url adapter for generic objects in Zope 2 that
    checks if the context is inside an IChildSite with a customized
    URL.
    """
    def __str__(self):
        mapped_url = map_url('/'.join(self.context.getPhysicalPath()),
                             self.request)
        if mapped_url is None:
            if ITraversable.providedBy(self.context):
                return super(LineageAbsoluteURL, self).__str__()
            else:
                return AbsoluteURL.__str__(self)
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
    site_mgr_root = ''
    scheme = urlparse.urlparse(request.getURL())[0]

    # We want to sort by descending path distance,
    # so that deeper child sites don't get incorrectly swallowed
    # by parent child sites
    roots = sorted(vhm_map.keys(), key=lambda x: -len(x.split('/')))
    for possible_site_mgr_root in roots:
        possible_site_url = vhm_map[possible_site_mgr_root]
        possible_site_netloc = urlparse.urlparse(possible_site_url)[1]
        if path.startswith(possible_site_mgr_root):
            site_mgr_root = possible_site_mgr_root
            child_site_netloc = possible_site_netloc
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
    return url.encode('UTF-8')


def absolute_url(self, relative=0):
    if not IChildSite.providedBy(self):
        return self._absolute_url(relative)
    elif relative:
        self.virtual_url_path()

    url = map_url('/'.join(self.getPhysicalPath()),
                  aq_acquire(self, 'REQUEST'))

    return url


def physicalPathToURL(self, path, relative=0):
    """ Convert a physical path into a URL in the current context,
    applying our stored mapping.
    """
    if type(path) is type(''):
        path_to_map = path.split( '/')
    elif path is None:
        path_to_map = []
    else:
        path_to_map = list(path)
    if path_to_map and path_to_map[0] != '':
        path_to_map.insert(0, '')
    mapped_url = map_url('/'.join(path_to_map), self)

    if relative or mapped_url is None:
        return self._physicalPathToURL(path or '', relative)
    else:
        return mapped_url
