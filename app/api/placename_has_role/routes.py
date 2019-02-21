from app.api.placename_has_role.facade import PlacenameHasRoleFacade
from app.models import PlacenameHasRole


def register_placename_has_role_api_urls(app):
    registrar = app.api_url_registrar
    registrar.register_get_routes(PlacenameHasRole, PlacenameHasRoleFacade)
    registrar.register_post_routes(PlacenameHasRole, PlacenameHasRoleFacade)
    registrar.register_patch_routes(PlacenameHasRole, PlacenameHasRoleFacade)
    registrar.register_delete_routes(PlacenameHasRole, PlacenameHasRoleFacade)

    registrar.register_relationship_post_route(PlacenameHasRoleFacade, 'document')
    registrar.register_relationship_patch_route(PlacenameHasRoleFacade, 'placename')
    registrar.register_relationship_get_route(PlacenameHasRoleFacade, 'placename-role')

