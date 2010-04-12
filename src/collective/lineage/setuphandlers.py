from zope.app.component.hooks import getSite

from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.upgrade import _upgrade_registry
from Products.GenericSetup.registry import _profile_registry


def importVarious(context):
    """Run the setup handlers for the default profile"""
    if context.readDataFile('collective_lineage-default.txt') is None:
        return

    # run the upgrade steps for this package
    portal = getSite()
    setup_tool = getToolByName(portal, 'portal_setup')
    profile_id = "collective.lineage:default"
    upgrade_steps = setup_tool.listUpgrades(profile_id)
    steps_to_run = []
    for step in upgrade_steps:
        if isinstance(step, list):
            # this is a group of steps
            for new_step in step:
                steps_to_run.append(new_step['step'].id)
        else:
            steps_to_run.append(step['step'].id)

    #################
    # from GS tool...
    #################
    for step_id in steps_to_run:
        step = _upgrade_registry.getUpgradeStep(profile_id, step_id)
        if step is not None:
            step.doStep(setup_tool)

    # XXX should be a bit smarter about deciding when to up the
    #     profile version
    profile_info = _profile_registry.getProfileInfo(profile_id)
    version = profile_info.get('version', None)
    if version is not None:
        setup_tool.setLastVersionForProfile(profile_id, version)
