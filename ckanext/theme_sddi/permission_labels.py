import ckan.plugins as p
from ckan import model
from ckan.lib.plugins import DefaultPermissionLabels
import ckan.plugins.toolkit as toolkit


class PermissionLabels(p.SingletonPlugin, DefaultPermissionLabels):
    p.implements(p.IPermissionLabels)


    # IPermissionLabels
    def get_dataset_labels(self, dataset_obj):
        labels = []
        if not dataset_obj.type == u'showcase':
            return super(PermissionLabels, self).get_dataset_labels(dataset_obj)

        extras = dataset_obj.extras
        breakpoint()
        if extras["showcase_restricted"] in ("public", "registered"):
            labels.append("public")
        elif extras["showcase_restricted"] == "same_organization":
            labels.append(f"org-{dataset_obj.owner_org}")
        else:
            labels.append("creator-%s" % dataset_obj.creator_user_id)
            labels.append(f"org-admin-{dataset_obj.owner_org}")

        return labels

    def get_user_dataset_labels(self, user_obj):
        endpoint = toolkit.request.endpoint
        breakpoint()
        if not endpoint in ("showcase_blueprint.index", "showcase_blueprint.read"):
            return super(PermissionLabels, self).get_user_dataset_labels(user_obj)

        labels = ['public']
        if not user_obj:
            return labels

        labels.append(u'creator-%s' % user_obj.id)

        organisation_query = (
            model.Session.query(model.Member, model.Group)
            .join(model.Group, model.Group.id == model.Member.group_id)
            .filter(model.Member.table_id == user_obj.id)
            .filter(model.Member.state == "active")
            .filter(model.Group.type == "organization")
        )

        for member, group in organisation_query:
            labels.append(f"org-{group.id}")

            if member.capacity == "admin":
                labels.append(f"org-admin-{group.id}")

        # orgs = toolkit.get_action(u'organization_list_for_user')(
        #     {u'user': user_obj.id}, {u'permission': u'read'})
        # labels.extend(u'member-%s' % o[u'id'] for o in orgs)

        # if authz.check_config_permission('allow_dataset_collaborators'):
        #     # Add a label for each dataset this user is a collaborator of
        #     datasets = toolkit.get_action('package_collaborator_list_for_user')(
        #         {'ignore_auth': True}, {'id': user_obj.id})

        #     labels.extend('collaborator-%s' % d['package_id'] for d in datasets)

        return labels
