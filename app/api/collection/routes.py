from app.api.decorators import api_require_roles
from app.api.collection.facade import CollectionFacade
from app.models import Collection


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

    registrar.register_relationship_get_route(CollectionFacade, 'documents')
    registrar.register_relationship_post_route(CollectionFacade, 'documents')
    registrar.register_relationship_patch_route(CollectionFacade, 'documents')

    registrar.register_relationship_get_route(CollectionFacade, 'admin')
    registrar.register_relationship_post_route(CollectionFacade, 'admin')
    registrar.register_relationship_patch_route(CollectionFacade, 'admin')

    registrar.register_relationship_get_route(CollectionFacade, 'changes')
    registrar.register_relationship_post_route(CollectionFacade, 'changes')
