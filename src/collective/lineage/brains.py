from Acquisition import aq_parent

from collective.lineage.absoluteurl import map_url


def getURL(self, relative=0):
    parent = aq_parent(self)
    mapped_url = map_url(self.getPath(), parent.REQUEST)
    if mapped_url is None:
        # Didn't find any defined maps for this brain
        return self._getURL()
    else:
        return mapped_url
