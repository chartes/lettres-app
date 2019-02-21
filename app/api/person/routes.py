from app.api.person.facade import PersonFacade
from app.models import Person


def register_person_api_urls(app):
    registrar = app.api_url_registrar
    registrar.register_get_routes(Person, PersonFacade)
    registrar.register_post_routes(Person, PersonFacade)
    registrar.register_patch_routes(Person, PersonFacade)
    registrar.register_delete_routes(Person, PersonFacade)

    registrar.register_relationship_get_route(PersonFacade, 'documents')
    registrar.register_relationship_post_route(PersonFacade, 'documents')
    registrar.register_relationship_patch_route(PersonFacade, 'documents')

    registrar.register_relationship_get_route(PersonFacade, 'roles-within-documents')
    registrar.register_relationship_post_route(PersonFacade, 'roles-within-documents')
    registrar.register_relationship_patch_route(PersonFacade, 'roles-within-documents')

    registrar.register_relationship_get_route(PersonFacade, 'changes')
    registrar.register_relationship_post_route(PersonFacade, 'changes')
