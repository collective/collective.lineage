from collective.lineage import MessageFactory as _
from collective.lineage import interfaces
from p4a.subtyper import interfaces as stifaces
from zope import interface


class ChildSiteDescriptor(object):
    """A descriptor for the Child Site subtype.
    """
    interface.implements(stifaces.IFolderishContentTypeDescriptor)
    title = _(u'Child Site')
    description = _(u'A child site')
    type_interface = interfaces.IChildSite
