from app.api.decorators import api_require_roles
from app.api.user.facade import UserFacade
from app.models import User


def register_user_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(User, UserFacade, [api_require_roles("contributor")])

    registrar.register_relationship_get_route(UserFacade, 'roles', [api_require_roles("contributor")])
    registrar.register_relationship_get_route(UserFacade, 'locks', [api_require_roles("contributor")])
    registrar.register_relationship_get_route(UserFacade, 'changes', [api_require_roles("contributor")])
    registrar.register_relationship_get_route(UserFacade, 'bookmarks', [api_require_roles("contributor")])

    registrar.register_relationship_patch_route(UserFacade, 'roles', [api_require_roles("admin")])
    registrar.register_relationship_post_route(UserFacade, 'roles', [api_require_roles("admin")])
    registrar.register_relationship_delete_route(UserFacade, 'roles', [api_require_roles("admin")])

    registrar.register_relationship_post_route(UserFacade, 'bookmarks', [api_require_roles("contributor")])
    registrar.register_relationship_patch_route(UserFacade, 'bookmarks', [api_require_roles("contributor")])
    registrar.register_relationship_delete_route(UserFacade, 'bookmarks', [api_require_roles("contributor")])

