from app.api.placename_role.facade import PlacenameRoleFacade
from app.models import PlacenameRole


def register_placename_role_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(PlacenameRole, PlacenameRoleFacade)
    registrar.register_post_routes(PlacenameRole, PlacenameRoleFacade)
    registrar.register_patch_routes(PlacenameRole, PlacenameRoleFacade)
    registrar.register_delete_routes(PlacenameRole, PlacenameRoleFacade)

