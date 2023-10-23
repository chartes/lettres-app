from flask import jsonify, current_app
from sqlalchemy import or_

from app.api.decorators import api_require_roles
from app.api.collection.facade import CollectionFacade
from app.models import Collection, Document


def register_collection_role_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(Collection, CollectionFacade)
    registrar.register_post_routes(
        Collection,
        CollectionFacade,
        [api_require_roles("admin")]
    )
    registrar.register_patch_routes(
        Collection,
        CollectionFacade,
        [api_require_roles("admin")]
    )
    registrar.register_delete_routes(
        Collection,
        CollectionFacade,
        [api_require_roles("admin")]
    )

    registrar.register_relationship_get_route(CollectionFacade, 'parents')
    registrar.register_relationship_get_route(CollectionFacade, 'children')
    registrar.register_relationship_get_route(CollectionFacade, 'documents-including-children')
    registrar.register_relationship_get_route(CollectionFacade, 'published-including-children')

    registrar.register_relationship_get_route(CollectionFacade, 'documents')
    registrar.register_relationship_post_route(CollectionFacade, 'documents')
    registrar.register_relationship_patch_route(CollectionFacade, 'documents')

    registrar.register_relationship_get_route(CollectionFacade, 'admin')
    registrar.register_relationship_post_route(CollectionFacade, 'admin')
    registrar.register_relationship_patch_route(CollectionFacade, 'admin')

    registrar.register_relationship_get_route(CollectionFacade, 'changes')
    registrar.register_relationship_post_route(CollectionFacade, 'changes')

    @current_app.route('/api/<api_version>/published-collections')
    def published_collections(api_version):
        published_collections = Collection.query.with_entities(Collection.title).distinct().order_by(Collection.title).filter(or_(Collection.documents.any(Document.is_published == True), Collection.children.any(Collection.documents.any(Document.is_published == True)))).all()
        response = jsonify({"data": [p[0] for p in published_collections]})
        return response, 200
    @current_app.route('/api/<api_version>/all-collections')
    def all_collections(api_version):
        all_collections = Collection.query.with_entities(Collection.title).distinct().order_by(Collection.title).all()
        response = jsonify({"data": [p[0] for p in all_collections]})
        return response, 200