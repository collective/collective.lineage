# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import queryUtility
from plone.app.imaging.interfaces import IImagingSchema


def get_image_traverser(context):
    siteroot = queryUtility(IPloneSiteRoot)
    return IImagingSchema(siteroot)
