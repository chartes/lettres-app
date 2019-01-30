from app.api.changelog.facade import ChangelogFacade
from app.api.decorators import api_require_roles
from app.models import Changelog


def register_changelog_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(Changelog, ChangelogFacade)
    registrar.register_post_routes(Changelog, ChangelogFacade, [api_require_roles("contributor")])
    registrar.register_patch_routes(Changelog, ChangelogFacade, [api_require_roles("contributor")])
    registrar.register_delete_routes(Changelog, ChangelogFacade, [api_require_roles("contributor")])

    registrar.register_relationship_get_route(ChangelogFacade, 'user')
