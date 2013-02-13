# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.utils.translation import ugettext_lazy as _

import horizon

class Contextualizer(horizon.Panel):
    name = _("Contextualizer")
    slug = 'contextualizer'

class FeynAppsPanels(horizon.PanelGroup):
    name = _("FeynApps")
    slug = 'feynapps'
    panels = ('contextualizer', )

# XXX enolfc: This is Folsom specific!!
from horizon.dashboards.nova import dashboard
dashboard.Nova.register(Contextualizer)
dashboard.Nova.panels = dashboard.Nova.panels + (FeynAppsPanels, )
