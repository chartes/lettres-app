from app.api.witness.facade import WitnessFacade
from app.models import Witness


def register_witness_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(Witness, WitnessFacade)
    registrar.register_post_routes(Witness, WitnessFacade)
    registrar.register_patch_routes(Witness, WitnessFacade)
    registrar.register_delete_routes(Witness, WitnessFacade)

    #registrar.register_relationship_get_route(WitnessFacade, 'images')
    registrar.register_relationship_get_route(WitnessFacade, 'institution')
    registrar.register_relationship_get_route(WitnessFacade, 'document')
    registrar.register_relationship_get_route(WitnessFacade, 'changes')

    #registrar.register_relationship_post_route(WitnessFacade, 'images')
    registrar.register_relationship_post_route(WitnessFacade, 'institution')
    registrar.register_relationship_post_route(WitnessFacade, 'changes')

    #registrar.register_relationship_patch_route(WitnessFacade, 'images')
    registrar.register_relationship_patch_route(WitnessFacade, 'institution')

