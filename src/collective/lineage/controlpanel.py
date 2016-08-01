from plone.app.registry.browser import controlpanel

from collective.lineage.interfaces import ILineageSettings, _


class LineageSettingsEditForm(controlpanel.RegistryEditForm):

    schema = ILineageSettings
    label = _(u"Lineage settings")
    description = _(u"""""")

    def updateFields(self):
        super(LineageSettingsEditForm, self).updateFields()
        # There isn't a widget to nicely edit a Dict schema field yet
        # see: https://dev.plone.org/ticket/11932
        self.fields = self.fields.omit('vhm_map')

    def updateWidgets(self):
        super(LineageSettingsEditForm, self).updateWidgets()


class LineageSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = LineageSettingsEditForm
