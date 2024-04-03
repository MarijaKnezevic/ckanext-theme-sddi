import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan import authz, model

# import ckanext.theme_sddi.cli as cli
# import ckanext.theme_sddi.helpers as helpers
# import ckanext.theme_sddi.views as views
import ckanext.theme_sddi.logic.action as action
import ckanext.theme_sddi.logic.auth as auth
import ckanext.theme_sddi.logic.validators as validators
#from ckanext.theme_sddi.logic import action, auth, validators
from ckanext.theme_sddi.permission_labels import PermissionLabels


class ThemeSddiPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)
    # plugins.implements(plugins.IPackageController, inherit=True)
    # plugins.implements(plugins.IBlueprint)
    # plugins.implements(plugins.IClick)
    # plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "theme_sddi")

    # IAuthFunctions

    # def get_auth_functions(self):
    #     return auth.get_auth_functions()

    # IActions

    def get_actions(self):
        return action.get_actions()

    # def after_search(self, search_results, search_params):
    #     breakpoint()
    #     if toolkit.g.user and toolkit.g.userobj.sysadmin:
    #         return search_results

    #     count = search_results["count"]
    #     for idx, pkg in enumerate(search_results["results"]):
    #         if pkg["type"] == "dataset":
    #             return search_results
    #         extras = pkg.get("extras", {})
    #         showcase_restricted = [
    #             item["value"] for item in extras if item["key"] == "showcase_restricted"
    #         ]
    #         breakpoint()
    #         if "same_organization" in showcase_restricted:
    #             creator = model.User.get(pkg["creator_user_id"])
    #             group_ids = creator.get_group_ids()
    #             is_same_org = authz.users_role_for_group_or_org(
    #                 group_ids[0], toolkit.g.user
    #             )
    #             if not is_same_org:
    #                 del search_results["results"][idx]
    #                 search_results["count"] = count - 1

    #         elif "registered" in showcase_restricted:
    #             return search_results
    #     breakpoint()
    #     return search_results

    # IBlueprint

    # def get_blueprint(self):
    #     return views.get_blueprints()

    # IClick

    # def get_commands(self):
    #     return cli.get_commands()

    # ITemplateHelpers

    # def get_helpers(self):
    #     return helpers.get_helpers()

    # IValidators

    def get_validators(self):
        return validators.get_validators()
