from zope.interface import Interface
from zope import schema

from collective.lineage import MessageFactory as _

class ILineageBrowserLayer(Interface):
    """Browser layer marker interface
    """ 

class ISearchRoot(Interface):
    """Marker interface for items that are search roots
    """

class IChildFolder(Interface):
    """Content type interface for lineage folders
    """
    
    title = schema.TextLine(title=_(u"Title"),
                            description=_(u"Site title"),
                            required=True)
    
    description = schema.Text(title=_(u"Description"),
                              description=_(u"Short summary of the site's purpose"),
                              required=False,
                              missing_value=u'',)

