# -*- coding: utf-8 -*-
from plone.browserlayer import layer
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import queryUtility


try:
    from plone.app.imaging import scaling
except ImportError:
    scaling = None


def mark_layer(site, event):
    """
    Support re-marking an already marked request.
    """
    if hasattr(event.request, "_plonebrowserlayer_"):
        del event.request._plonebrowserlayer_
    return layer.mark_layer(site, event)


if scaling:
    def get_image_traverser(context):
        siteroot = queryUtility(IPloneSiteRoot)
        return scaling.IImagingSchema(siteroot)
