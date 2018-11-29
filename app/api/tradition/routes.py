from app.api.tradition.facade import TraditionFacade
from app.models import Tradition


def register_tradition_role_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(Tradition, TraditionFacade)
    registrar.register_post_routes(Tradition, TraditionFacade)
    registrar.register_patch_routes(Tradition, TraditionFacade)
    registrar.register_delete_routes(Tradition, TraditionFacade)

    registrar.register_relationship_get_route(TraditionFacade, 'documents')
    registrar.register_relationship_post_route(TraditionFacade, 'documents')
    registrar.register_relationship_patch_route(TraditionFacade, 'documents')

