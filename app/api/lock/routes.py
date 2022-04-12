from app.api.decorators import api_require_roles
from app.api.lock.decorators import manage_lock_removal, manage_lock_addition, manage_lock_update
from app.api.lock.facade import LockFacade
from app.models import Lock


def register_lock_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(Lock, LockFacade, [api_require_roles("contributor")])
    #registrar.register_post_routes(Lock, LockFacade, [api_require_roles("contributor"), manage_lock_addition()])
    #registrar.register_patch_routes(Lock, LockFacade, [api_require_roles("contributor"), manage_lock_update()])
    #registrar.register_delete_routes(Lock, LockFacade, [api_require_roles("contributor"), manage_lock_removal()])

    registrar.register_relationship_get_route(LockFacade, 'user', [api_require_roles("contributor")])
