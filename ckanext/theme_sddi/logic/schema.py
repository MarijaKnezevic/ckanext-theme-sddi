import ckan.plugins.toolkit as tk
from ckan.logic.schema import validator_args

from ckanext.showcase.logic.schema import (
    showcase_create_schema,
    showcase_update_schema,
    showcase_show_schema,
)


def theme_sddi_get_sum():
    not_empty = tk.get_validator("not_empty")
    convert_int = tk.get_validator("convert_int")

    return {"left": [not_empty, convert_int], "right": [not_empty, convert_int]}


@validator_args
def tum_showcase_create_schema(
    not_empty,
    OneOf,
    convert_to_extras,
    owner_org_validator,
    unicode_safe,
    ignore_missing,
    boolean_validator,
    json_list_or_string,
    validate_restricted_field
):
    schema = showcase_create_schema()
    schema["showcase_restricted"] = [
        not_empty,
        OneOf(["registered", "same_organization", "only_allowed_users"]),
        validate_restricted_field, convert_to_extras,
    ]
    schema["owner_org"] = [owner_org_validator, unicode_safe]
    schema["private"] = [ignore_missing, boolean_validator]
    schema["allowed_users"] = [ignore_missing, json_list_or_string, unicode_safe, convert_to_extras]
    return schema


@validator_args
def tum_showcase_update_schema(
    ignore_missing,
    OneOf,
    convert_to_extras,
    owner_org_validator,
    unicode_safe,
    boolean_validator,
    json_list_or_string,
    validate_restricted_field
):
    schema = showcase_update_schema()
    schema["showcase_restricted"] = [
        ignore_missing,
        OneOf(["registered", "same_organization", "only_allowed_users"]),
        validate_restricted_field,
        convert_to_extras,
    ]
    schema["owner_org"] = [ignore_missing, owner_org_validator, unicode_safe]
    schema["private"] = [ignore_missing, boolean_validator]
    schema["allowed_users"] = [ignore_missing, json_list_or_string, unicode_safe, convert_to_extras]
    return schema


@validator_args
def tum_showcase_show_schema(ignore_empty, convert_from_extras, json_list_or_string):
    schema = showcase_show_schema()
    schema["showcase_restricted"] = [convert_from_extras]
    schema["owner_org"] = []
    schema["private"] = []
    schema["allowed_users"] = [convert_from_extras, json_list_or_string, ignore_empty]
    return schema
