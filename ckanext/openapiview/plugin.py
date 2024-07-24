# encoding: utf-8

import logging
from typing import Any

from ckan.common import CKANConfig, json
import ckan.plugins as p
import ckanext.resourceproxy.plugin as proxy
import ckan.lib.datapreview as datapreview

log = logging.getLogger(__name__)

def resource_openapi_url(resource):
    url = resource.get('openapi_spec')
    if url:
        return url

    if resource.get('format', '').lower() == 'openapi-json':
        return resource['url']

class OpenAPIViewPlugin(p.SingletonPlugin):
    '''This extension previews JSON(P).'''

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IResourceView, inherit=True)
    p.implements(p.ITemplateHelpers)


    def update_config(self, config):
        if not p.toolkit.check_ckan_version('2.9'):
            p.toolkit.add_template_directory(config, '2.8_templates')
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_resource('assets', 'ckanext-openapiview')

    def get_helpers(self):
        return {
            'openapiview_resource_openapi_url': resource_openapi_url
        }

    def info(self):
        return {'name': 'openapi_view',
                'title': p.toolkit._('OpenAPI'),
                'icon': 'file-text-o',
                'default_title': p.toolkit._('OpenAPI'),
                }

    def can_view(self, data_dict):
        return resource_openapi_url(data_dict['resource']) is not None

    def view_template(self, context, data_dict):
        return 'openapiview/openapi_view.html'

    def form_template(self, context, data_dict):
        return 'openapiview/openapi_form.html'
