from app.api.person_role.facade import PersonRoleFacade
from app.models import PersonRole


def register_person_role_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(PersonRole, PersonRoleFacade)
    registrar.register_post_routes(PersonRole, PersonRoleFacade)
    registrar.register_patch_routes(PersonRole, PersonRoleFacade)
    registrar.register_delete_routes(PersonRole, PersonRoleFacade)

    registrar.register_relationship_post_route(PersonRoleFacade, 'changes')
    registrar.register_relationship_get_route(PersonRoleFacade, 'changes')

