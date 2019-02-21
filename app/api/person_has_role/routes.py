from app.api.person_has_role.facade import PersonHasRoleFacade
from app.models import PersonHasRole


def register_person_has_role_api_urls(app):
    registrar = app.api_url_registrar
    registrar.register_get_routes(PersonHasRole, PersonHasRoleFacade)
    registrar.register_post_routes(PersonHasRole, PersonHasRoleFacade)
    registrar.register_patch_routes(PersonHasRole, PersonHasRoleFacade)
    registrar.register_delete_routes(PersonHasRole, PersonHasRoleFacade)

    registrar.register_relationship_post_route(PersonHasRoleFacade, 'document')
    registrar.register_relationship_patch_route(PersonHasRoleFacade, 'person')
    registrar.register_relationship_get_route(PersonHasRoleFacade, 'person-role')

