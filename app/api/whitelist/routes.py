from app.api.whitelist.facade import WhitelistFacade
from app.models import Whitelist


def register_whitelist_api_urls(app):
    registrar = app.api_url_registrar
    registrar.register_get_routes(Whitelist, WhitelistFacade)
    registrar.register_relationship_get_route(WhitelistFacade, 'documents')
    registrar.register_relationship_get_route(WhitelistFacade, 'users')

    #registrar.register_post_routes(Correspondent, DocumentFacade)
