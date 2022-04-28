from flask import jsonify

from app import api_bp
from app.api.placename.facade import PlacenameFacade
from app.models import Placename


def register_placename_api_urls(app):
    registrar = app.api_url_registrar
    registrar.register_get_routes(Placename, PlacenameFacade)
    registrar.register_post_routes(Placename, PlacenameFacade)
    registrar.register_patch_routes(Placename, PlacenameFacade)
    registrar.register_delete_routes(Placename, PlacenameFacade)

    registrar.register_relationship_get_route(PlacenameFacade, 'roles-within-documents')
    registrar.register_relationship_post_route(PlacenameFacade, 'roles-within-documents')
    registrar.register_relationship_patch_route(PlacenameFacade, 'roles-within-documents')

    registrar.register_relationship_get_route(PlacenameFacade, 'documents')
    registrar.register_relationship_post_route(PlacenameFacade, 'documents')
    registrar.register_relationship_patch_route(PlacenameFacade, 'documents')

    registrar.register_relationship_get_route(PlacenameFacade, 'changes')
    registrar.register_relationship_post_route(PlacenameFacade, 'changes')

    @api_bp.route('/api/<api_version>/all-placenames')
    def all_placenames(api_version):
        placenames = Placename.query.with_entities(Placename.label).distinct().order_by(Placename.label).all()
        response = jsonify({"data": [p[0] for p in placenames]})
        return response, 200

