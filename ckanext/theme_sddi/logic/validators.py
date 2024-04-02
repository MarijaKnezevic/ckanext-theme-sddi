import json

import ckan.plugins.toolkit as tk


def theme_sddi_required(value):
    if not value or value is tk.missing:
        raise tk.Invalid(tk._("Required"))
    return value


def validate_restricted_field(key, data, errors, context):
    restricted = data.get(key)
    owner_org_key = ('owner_org',)
    allowed_users_key = ('allowed_users',)

    allowed_users_list = json.loads(data[allowed_users_key]) if data.get(allowed_users_key) else []

    if restricted == 'registered':
        if data.get(owner_org_key):
            data[owner_org_key] = ""
        if allowed_users_list and any(allowed_users_list):
            data[allowed_users_key] = ""
    elif restricted == 'same_organization':
        if allowed_users_list and any(allowed_users_list):
            data[allowed_users_key] = ""
    elif restricted == 'only_allowed_users':
        if data.get(owner_org_key):
            data[owner_org_key] = ""


def get_validators():
    return {
        "theme_sddi_required": theme_sddi_required,
        "validate_restricted_field": validate_restricted_field,
    }
