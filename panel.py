# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.utils.translation import ugettext_lazy as _

import horizon
# XXX This may change!
from openstack_dashboard.dashboards.project import dashboard

class Contextualizer(horizon.Panel):
    name = _("Contextualizer")
    slug = 'contextualizer'

class FeynAppsPanels(horizon.PanelGroup):
    name = _("FeynApps")
    slug = 'feynapps'
    panels = ('contextualizer', )

dashboard.Project.register(Contextualizer)
dashboard.Project.panels = dashboard.Project.panels + (FeynAppsPanels, )
