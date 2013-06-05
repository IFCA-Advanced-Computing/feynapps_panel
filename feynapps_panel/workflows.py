# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import logging
import urllib2

from django.utils.text import normalize_newlines
from django.utils.translation import ugettext as _

from django.conf import settings

from horizon import exceptions
from horizon import forms
from horizon import workflows

from openstack_dashboard import api

import openstack_dashboard.dashboards.project.instances.workflows as wf

LOG = logging.getLogger(__name__)

APPS_URL = getattr(settings, 'FEYNAPPS_URL',
                   'https://raw.github.com/enolfc/feynapps/master/apps.json')
REPO_URL = getattr(settings, 'FEYNAPPS_REPO',
                   'http://github.com/enolfc/feynapps.git')
IMG_ATTR = getattr(settings, 'FEYNAPPS_IMG_ATTR', 'feynapps')


def get_apps():
    config = {}
    try:
        config = json.loads(urllib2.urlopen(APPS_URL).read())
    except Exception, e:
        LOG.warn("Unable to load app config: %s" % e)
    return config


class SetInstanceDetailsAction(wf.SetInstanceDetailsAction):
    class Meta:
        name = _("Details")
        help_text_template = ("project/instances/"
                              "_launch_details_help.html")

    def _get_available_images(self, request, context):
        project_id = context.get('project_id', None)
        if not hasattr(self, "_public_images"):
            public = {"is_public": True,
                      "status": "active",
                      "property-%s" % IMG_ATTR: True,
                      }
            try:
                public_images, _more = api.glance.image_list_detailed(request,
                                                                      filters=public)
            except:
                public_images = []
                exceptions.handle(request,
                                  _("Unable to retrieve public images."))
            self._public_images = public_images

        # Preempt if we don't have a project_id yet.
        if project_id is None:
            setattr(self, "_images_for_%s" % project_id, [])

        if not hasattr(self, "_images_for_%s" % project_id):
            owner = {"property-owner_id": project_id,
                     "status": "active",
                     "property-%s" % IMG_ATTR: True, }
            try:
                owned_images, _more = api.glance.image_list_detailed(request,
                                                                     filters=owner)
            except:
                exceptions.handle(request,
                                  _("Unable to retrieve images for "
                                    "the current project."))
            setattr(self, "_images_for_%s" % project_id, owned_images)

        owned_images = getattr(self, "_images_for_%s" % project_id)
        images = owned_images + self._public_images

        # Remove duplicate images
        image_ids = []
        final_images = []
        for image in images:
            if image.id not in image_ids:
                image_ids.append(image.id)
                final_images.append(image)
        return [image for image in final_images
                if image.container_format not in ('aki', 'ari')]


class SetInstanceDetails(wf.SetInstanceDetails):
    action_class = SetInstanceDetailsAction
    contributes = ("source_type", "source_id", "name", "count", "flavor")


class CustomizeAction(workflows.Action):
    def __init__(self, request, context, *args, **kwargs):
        super(CustomizeAction, self).__init__(request,
                                              context,
                                              *args,
                                              **kwargs)

        feynapps = get_apps()
        for a in feynapps:
            fname = 'feynapp_context_%s' % a
            versions = feynapps[a]['versions'].keys()
            # first higher versions
            versions.sort()
            versions.reverse()
            choices = (
                ('', _("Don't install.")),
            ) + tuple([(v, v) for v in versions])
            self.fields[fname] = forms.ChoiceField(label=_(a),
                                                   choices=choices,
                                                   required=False)

    class Meta:
        name = _("Contextualize!")
        help_text_template = ("feynapps_panel/"
                              "_launch_customize_help.html")


class PostCreationStep(workflows.Step):
    action_class = CustomizeAction
    t = ['feynapp_context_%s' % a for a in get_apps()]
    contributes = tuple(t)


class CustomizeInstance(wf.LaunchInstance):
    slug = "customize_instance"
    name = _("Customize Instance")
    finalize_button_name = _("Launch")
    success_message = _('Launched %(count)s named "%(name)s".')
    failure_message = _('Unable to launch %(count)s named "%(name)s".')
    default_steps = (wf.SelectProjectUser,
                     SetInstanceDetails,
                     wf.SetAccessControls,
                     wf.SetNetwork,
                     wf.VolumeOptions,
                     PostCreationStep)

    def handle(self, request, context):
        extra_soft = {'repo': REPO_URL,
                      'apps': {}, }
        feynapps = get_apps()
        for a in feynapps:
            version = context.get('feynapp_context_%s' % a, '')
            if version:
                extra_soft['apps'][a] = version
        extra_data = json.dumps(extra_soft)

        # Determine volume mapping options
        if context.get('volume_type', None):
            if(context['delete_on_terminate']):
                del_on_terminate = 1
            else:
                del_on_terminate = 0
            mapping_opts = ("%s::%s"
                            % (context['volume_id'], del_on_terminate))
            dev_mapping = {context['device_name']: mapping_opts}
        else:
            dev_mapping = None

        netids = context.get('network_id', None)
        if netids:
            nics = [{"net-id": netid, "v4-fixed-ip": ""}
                    for netid in netids]
        else:
            nics = None

        try:
            api.nova.server_create(request,
                                   context['name'],
                                   context['source_id'],
                                   context['flavor'],
                                   context['keypair_id'],
                                   #normalize_newlines(custom_script),
                                   normalize_newlines(extra_data),
                                   context['security_group_ids'],
                                   dev_mapping,
                                   nics=nics,
                                   instance_count=int(context['count']))
            return True
        except:
            exceptions.handle(request)
            return False
