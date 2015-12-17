# -*- coding: utf-8 -*-
from logging import getLogger

logger = getLogger('collective.lineage.upgrades')


def upgradeToTwoZero(context):
    """ going from pre-2.X to 2.X needs to have the default profile run
        so that it can pick up the new actions
    """
    context.portal_setup.runAllImportStepsFromProfile(
        'profile-collective.lineage:default'
    )
    logger.info("Re-ran Lineage default profile to add 2.0 actions")
