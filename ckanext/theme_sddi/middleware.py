import cgi
import logging
import json
import re
from datetime import datetime, timedelta

import ckan.plugins.toolkit as tk
from ckan.common import request, current_user


log = logging.getLogger(__name__)
_INTERVAL = int(tk.config.get("ckanext.sddi.last_attempt_time_interval", 60))


def user_cannot_send_reset(plugin_extras):
    if plugin_extras and "last_attempt_time" in plugin_extras["sddi"]:
        lst_att = json.loads(plugin_extras["sddi"]["last_attempt_time"])
        lst_att_obj = datetime.strptime(
            lst_att, "%Y-%m-%d %H:%M:%S.%f"
        )

        if datetime.now() - lst_att_obj < timedelta(seconds=_INTERVAL):
            return True

        return False


_RESOURCE_NEW_RE = re.compile(r'^/[^/]+/([^/]+)/resource/new$')


def _optional_resource_finish():
    """Allow finishing dataset creation without adding any resource."""
    if request.method != 'POST':
        return
    match = _RESOURCE_NEW_RE.match(request.path)
    log.warning('SDDI resource/new check: method=%s path=%s match=%s', request.method, request.path, match)
    if not match:
        return
    save_action = request.form.get('save')
    log.warning('SDDI resource/new: save_action=%s form_keys=%s files=%s', save_action, list(request.form.keys()), list(request.files.keys()))
    if save_action in ('go-dataset', 'go-dataset-complete'):
        return

    _skip = {'save', 'id', 'resource_type', '_csrf_token'}
    data_provided = any(
        (v or isinstance(v, cgi.FieldStorage)) and k not in _skip
        for k, v in request.form.items()
    ) or any(f.filename for f in request.files.values())
    log.warning('SDDI resource/new: data_provided=%s', data_provided)
    if data_provided:
        return

    import ckan.model as model
    from ckan.types import Context
    from flask import redirect

    dataset_id = match.group(1)
    context = Context(
        model=model,
        session=model.Session,
        user=current_user.name,
        auth_user_obj=current_user,
    )
    try:
        pkg = tk.get_action('package_show')(context, {'id': dataset_id})
        pkg_type = pkg.get('type', 'dataset')
        tk.get_action('package_update')(
            Context(context, allow_state_change=True),
            dict(pkg, state='active'),
        )
        url = tk.h.url_for('{}.read'.format(pkg_type), id=dataset_id)
        log.warning('SDDI resource/new: redirecting to %s', url)
        return redirect(url)
    except Exception as e:
        log.warning('SDDI resource/new: exception %s', e, exc_info=True)
        return


def ckanext_before_request():

    early = _optional_resource_finish()
    if early is not None:
        return early

    if request.endpoint == "user.request_reset" and request.method == "POST":
        id = request.form.get("user")
        site_user = tk.get_action("get_site_user")({"ignore_auth": True}, {})
        context = {"user": site_user["name"]}
        data_dict = {"id": id}

        if "@" in id:
            user_list = tk.get_action(u'user_list')(context, {
                u'email': id, "all_fields": False
            })
            if len(user_list) == 1:
                data_dict = {"id": user_list[0]}

        try:
            user_dict = tk.get_action("user_show")(
                context, dict(data_dict, include_plugin_extras=True)
            )
            if user_cannot_send_reset(user_dict["plugin_extras"]):
                return tk.abort(429)

            last_attempt_time = datetime.now()
            tk.get_action("user_update")(
                context, dict(user_dict, last_attempt_time=last_attempt_time)
            )
        except tk.ObjectNotFound:
            tk.abort(404, tk._("User not found"))


def ckanext_after_request(response):
    if hasattr(request, 'view_args') and request.view_args:
        if request.view_args.get('logic_function') == 'status_show':
            data = response.json
            del data['result']['ckan_version']
            response.set_data(json.dumps(data))

    return response
