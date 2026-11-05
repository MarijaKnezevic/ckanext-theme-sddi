import logging
import json
import threading

import ckan.plugins as plugins

import ckanext.theme_sddi.cli as cli
import ckanext.theme_sddi.logic.action as action
import ckanext.theme_sddi.logic.auth as auth
import ckanext.theme_sddi.helpers as h
from ckanext.theme_sddi import middleware
import ckanext.theme_sddi.logic as logic
from ckan.lib.plugins import DefaultTranslation

from flask import Blueprint
from ckan.plugins import toolkit as tk

log = logging.getLogger(__name__)

# Guard against re-entrant calls: resource_create triggers after_dataset_update
_placeholder_guard = threading.local()

# Per dataset_type: list of (schema_field_name, resource_name_to_create)
_TYPE_DIST_MAP = {
    'dataset_documents': [('has_distribution',       'Content URL')],
    'project':           [('has_distribution',       'Project URI')],
    'online-service':    [('has_linkage',             'Linkage'),
                          ('has_external_docs',       'External Documentation'),
                          ('has_open_api_document',   'OpenAPI Document')],
    'software':          [('has_software_help',       'Software Help'),
                          ('has_documentation_url',   'Documentation URL'),
                          ('has_code_repository_url', 'Code Repository URL')],
    'online-application':[('has_external_docs',       'External Documentation'),
                          ('has_service_doc',         'Service Documentation')],
}


def _field_value(pkg_dict, field_name):
    """Return field value from pkg_dict — checks top-level keys (scheming) and extras list."""
    val = pkg_dict.get(field_name)
    if val is not None:
        return val
    for extra in pkg_dict.get('extras', []):
        if extra.get('key') == field_name:
            return extra.get('value')
    return None


def _create_distribution_placeholders(context, pkg_dict):
    """Auto-create placeholder resources for every has_* field set to 'yes'."""
    if getattr(_placeholder_guard, 'active', False):
        return

    dataset_type = pkg_dict.get('type', '')
    dist_fields = _TYPE_DIST_MAP.get(dataset_type)
    if not dist_fields:
        return

    # Use a fresh package_show to get the real current resource list —
    # pkg_dict from the hook only reflects the submitted form, not existing resources.
    try:
        fresh = tk.get_action('package_show')(
            {'ignore_auth': True},
            {'id': pkg_dict['id']},
        )
    except Exception:
        return

    existing_names = {r.get('name', '') for r in fresh.get('resources', [])}

    _placeholder_guard.active = True
    try:
        for field_name, resource_name in dist_fields:
            if _field_value(pkg_dict, field_name) == 'yes' and resource_name not in existing_names:
                tk.get_action('resource_create')(
                    {'ignore_auth': True, 'user': context.get('user')},
                    {'package_id': pkg_dict['id'], 'name': resource_name},
                )
                existing_names.add(resource_name)
    finally:
        _placeholder_guard.active = False


class ThemeSddiPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IActions, inherit=True)
    plugins.implements(plugins.IAuthFunctions, inherit=True)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IResourceController, inherit=True)
    plugins.implements(plugins.IMiddleware, inherit=True)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer
    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "theme_sddi")

    # IBlueprint
    def get_blueprint(self):
        blueprint = Blueprint('theme_sddi_blueprint', __name__)

        @blueprint.route('/new-catalog-entry')
        def new_catalog_entry():
            return tk.render('package/new_type_select.html')

        return blueprint

    # IActions
    def get_actions(self):
        return {
            "group_tree_children_g": action.group_tree_children_g,
            "user_create": action.user_create,
            "user_update": action.user_update,
            "resource_view_list": action.resource_view_list,
            "resource_search": action.resource_search,
        }

    # IAuthFunctions
    def get_auth_functions(self):
        return {'resource_show': auth.restricted_resource_show,
                'resource_view_show': auth.restricted_resource_show}

    def update_config_schema(self, schema):
        ignore_missing = tk.get_validator(u'ignore_missing')
        unicode_safe = tk.get_validator(u'unicode_safe')

        schema.update({
            u'ckan.site_intro_paragraph': [ignore_missing, unicode_safe],
            u'ckan.background_image': [ignore_missing, unicode_safe],
            u'image_upload': [ignore_missing, unicode_safe],
            u'clear_image_upload': [ignore_missing, unicode_safe],
        })
        return schema

    # ITemplateHelpers
    def get_helpers(self):
        return {
            "get_selected_group": h.get_selected_group,
            "get_allowable_children_groups": h.get_allowable_children_groups,
            "get_group_image": h.get_group_image,
            "group_tree_crumbs": h.group_tree_crumbs,
            "group_tree_section_g": h.group_tree_section_g,
            "get_recently_modified_group": h.get_recently_modified_group,
            "is_spatial_enabled": h.is_spatial_enabled,
            "restricted_get_user_id": h.restricted_get_user_id,
            "render_markdown": h.render_markdown,
            "sddi_get_organizations": h.sddi_get_organizations,
        }

    # IClick
    def get_commands(self):
        return cli.get_commands()

    # IMiddleware
    def make_middleware(self, app, config):
        app.before_request(middleware.ckanext_before_request)
        app.after_request(middleware.ckanext_after_request)
        return app

    # IFacets
    def dataset_facets(self, facets_dict, package_type):
        del facets_dict['groups']
        facets_dict['main'] = tk._('Main Categories')
        facets_dict['topic'] = tk._('Topics')
        return facets_dict

    # IPackageController
    def before_dataset_index(self, pkg_dict):
        return self.before_index(pkg_dict)

    def before_index(self, pkg_dict):
        groups = pkg_dict.get("groups", [])

        topic_names = []
        if not groups:
            return pkg_dict
        for group in groups:
            group_dict = tk.get_action("group_show")({}, {"id": group})
            groups_data = group_dict.get("groups", [])
            if groups_data[0]["name"] == "main-categories":
                pkg_dict["main"] = group_dict.get("display_name")
            else:
                topic_names.append(group_dict.get("display_name"))

        pkg_dict["topic"] = topic_names
        return pkg_dict

    def after_dataset_search(self, search_results, search_params):
        context = {'with_capacity': False}
        restricted_package_search_result = {}
        for key, value in search_results.items():
            if key == 'results':
                restricted_package_search_result_list = []
                for package in value:
                    try:
                        pkg = tk.get_action('package_show')(context,
                                                            {'id': package.get('id')})
                    except tk.ObjectNotFound:
                        continue
                    restricted_package_search_result_list.append(pkg)
                restricted_package_search_result[key] = \
                    restricted_package_search_result_list
            else:
                restricted_package_search_result[key] = value
        return restricted_package_search_result

    def after_dataset_update(self, context, pkg_dict):
        _create_distribution_placeholders(context, pkg_dict)

    def before_dataset_view(self, data_dict):
        data_dict['resources'] = action._resource_list_hide_fields(
            data_dict.get('resources', []))
        return data_dict

    # IResourceController
    def before_resource_update(self, context, current, resource):
        context['__restricted_previous_value'] = current.get('restricted')

    def after_resource_update(self, context, resource):
        previous_value = context.get('__restricted_previous_value')
        logic.restricted_notify_allowed_users(previous_value, resource)
