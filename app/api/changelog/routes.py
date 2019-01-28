from app.api.changelog.facade import ChangelogFacade
from app.models import Changelog


def register_changelog_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(Changelog, ChangelogFacade)
    registrar.register_post_routes(Changelog, ChangelogFacade)
    registrar.register_patch_routes(Changelog, ChangelogFacade)
    registrar.register_delete_routes(Changelog, ChangelogFacade)

