import ckan.plugins.toolkit as tk
import ckanext.theme_sddi.logic.schema as schema


@tk.side_effect_free
def theme_sddi_get_sum(context, data_dict):
    tk.check_access("theme_sddi_get_sum", context, data_dict)
    data, errors = tk.navl_validate(data_dict, schema.theme_sddi_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"],
    }


def get_actions():
    return {
        "theme_sddi_get_sum": theme_sddi_get_sum,
        "ckanext_showcase_create": tum_showcase_create,
        "ckanext_showcase_update": tum_showcase_update,
        "ckanext_showcase_package_list": tum_showcase_package_list,
        "package_show": tum_package_show,
    }


@tk.chained_action
def tum_showcase_create(next_action, context, data_dict):
    tk.check_access("ckanext_showcase_create", context)
    context["schema"] = schema.tum_showcase_create_schema()
    return next_action(context, data_dict)


@tk.chained_action
def tum_showcase_update(next_action, context, data_dict):
    tk.check_access("ckanext_showcase_update", context)
    context["schema"] = schema.tum_showcase_update_schema()
    breakpoint()
    restricted_value = data_dict.get("showcase_restricted")
    data_dict["private"] = restricted_value == "same_organization"
    return next_action(context, data_dict)


@tk.chained_action
@tk.side_effect_free
def tum_package_show(next_action, context, data_dict):
    tk.check_access("ckanext_showcase_show", context, data_dict)
    context["schema"] = schema.tum_showcase_show_schema()
    return next_action(context, data_dict)


@tk.chained_action
@tk.side_effect_free
def tum_showcase_package_list(next_action, context, data_dict):
    tk.check_access("ckanext_showcase_package_list", context, data_dict)
    # breakpoint()
    context.pop("schema", None)
    return next_action(context, data_dict)
