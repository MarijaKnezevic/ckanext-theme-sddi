import os
import json
import click
import urllib.request
import urllib.error

import ckan.lib.navl.dictization_functions as dict_fns
import ckan.plugins.toolkit as tk
import ckan.model as model

from ckan.cli import error_shout

from ckanext.theme_sddi.helpers import get_init_data


NotFound = tk.ObjectNotFound
NotAuthorized = tk.NotAuthorized
ValidationError = tk.ValidationError

HERE = os.path.dirname(__file__)
_site_url = tk.config.get('ckan.site_url')


@click.group("theme-sddi", short_help="SDDI commands")
def theme_sddi():
    pass


def create_org_or_group(group, is_org=False):
    user = tk.get_action('get_site_user')({'ignore_auth': True})
    context = {
            "model": model,
            "session": model.Session,
            "user": user['name'],
            "return_id_only": False
        }

    grp_or_org = 'organization_create' if is_org else 'group_create'
    if group.get('image_url'):
        group['image_url'] = _site_url + group.get('image_url')

    try:
        tk.get_action(grp_or_org)(context, group)
    except (NotFound, NotAuthorized) as e:
        error_shout(e)
        raise click.Abort()
    except dict_fns.DataError:
        error_shout('Integrity Error')
        raise click.Abort()
    except ValidationError as e:
        error_shout(e)
        raise click.Abort()


@theme_sddi.command("init_data")
def init_data():

    data = get_init_data()

    for group in data.get('groups'):
        create_org_or_group(group)
    for org in data.get('organizations'):
        create_org_or_group(org, is_org=True)

    click.secho(
        "Successfully created the initial Orgs/Groups",
        fg="green",
        bold=True
    )


@theme_sddi.command("setup-solr")
@click.option("--solr-url", default=None, help="Solr URL (default: read from ckan.ini)")
def setup_solr(solr_url):
    """Add required multiValued Solr fields for SDDI (topic, main)."""
    if solr_url is None:
        solr_url = tk.config.get("solr_url", "http://localhost:8983/solr/ckan")

    fields = [
        {"name": "topic", "type": "string", "indexed": True, "stored": True, "multiValued": True},
        {"name": "main",  "type": "string", "indexed": True, "stored": True, "multiValued": False},
    ]

    schema_url = solr_url.rstrip("/") + "/schema"

    for field in fields:
        payload = json.dumps({"add-field": field}).encode("utf-8")
        req = urllib.request.Request(
            schema_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read())
                if result.get("responseHeader", {}).get("status") == 0:
                    click.secho(f"  ✓ Field '{field['name']}' added.", fg="green")
                else:
                    click.secho(f"  ! Unexpected response for '{field['name']}': {result}", fg="yellow")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            if "already exists" in body:
                click.secho(f"  ✓ Field '{field['name']}' already exists, skipping.", fg="cyan")
            else:
                click.secho(f"  ✗ Failed to add field '{field['name']}': {body}", fg="red")
                raise click.Abort()

    click.secho("\nSolr schema setup complete.", fg="green", bold=True)


def get_commands():
    return [theme_sddi]
