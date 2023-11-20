from plone.browserlayer import layer


def mark_layer(site, event):
    """
    Support re-marking an already marked request.
    """
    if hasattr(event.request, "_plonebrowserlayer_"):
        del event.request._plonebrowserlayer_
    return layer.mark_layer(site, event)
