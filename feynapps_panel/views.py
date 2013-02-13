# vim: tabstop=4 shiftwidth=4 softtabstop=4

from horizon import workflows
from .workflows import CustomizeInstance

class CustomizeInstanceView(workflows.WorkflowView):
    workflow_class = CustomizeInstance
    template_name = "feynapps_panel/launch.html"

    def get_initial(self):
        initial = super(CustomizeInstanceView, self).get_initial()
        initial['project_id'] = self.request.user.tenant_id
        initial['user_id'] = self.request.user.id
        return initial


