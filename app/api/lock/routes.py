from app.api.lock.facade import LockFacade
from app.models import Lock


def register_lock_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(Lock, LockFacade)
    registrar.register_post_routes(Lock, LockFacade)
    registrar.register_patch_routes(Lock, LockFacade)
    registrar.register_delete_routes(Lock, LockFacade)

