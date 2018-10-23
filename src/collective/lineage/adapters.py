# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import queryUtility
from plone.app.imaging import scaling

from plone.browserlayer import layer


def mark_layer(site, event):
    """
    Support re-marking an already marked request.
    """
    if hasattr(event.request, "_plonebrowserlayer_"):
        del event.request._plonebrowserlayer_
    return layer.mark_layer(site, event)


def get_image_traverser(context):
    siteroot = queryUtility(IPloneSiteRoot)
    return scaling.IImagingSchema(siteroot)
