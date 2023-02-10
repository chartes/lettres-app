from flask import jsonify, current_app

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

    @current_app.route('/api/<api_version>/placenames-functions')
    def get_placename_functions(api_version):
        phr = PlacenameHasRole.query.with_entities(PlacenameHasRole.function).filter(
            PlacenameHasRole.function.isnot(None)
        ).distinct().order_by(PlacenameHasRole.function)
        print('PHR', phr)
        functions = [p[0] for p in phr] if phr else []
        return jsonify({'placename-functions': functions})


