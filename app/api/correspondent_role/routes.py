from app.api.correspondent_role.facade import CorrespondentRoleFacade
from app.models import CorrespondentRole


def register_correspondent_role_api_urls(app):
    registrar = app.api_url_registrar
    registrar.register_get_routes(CorrespondentRole, CorrespondentRoleFacade)
    registrar.register_post_routes(CorrespondentRole, CorrespondentRoleFacade)
    registrar.register_patch_routes(CorrespondentRole, CorrespondentRoleFacade)

    #registrar.register_relationship_get_route(CorrespondentRoleFacade, 'roles-within-document')
    #registrar.register_post_routes(CorrespondentRole, CorrespondentRoleFacade)
