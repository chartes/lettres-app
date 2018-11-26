from app.api.correspondent_has_role.facade import CorrespondentHasRoleFacade
from app.models import CorrespondentHasRole


def register_correspondent_has_role_api_urls(app):
    registrar = app.api_url_registrar
    registrar.register_get_routes(CorrespondentHasRole, CorrespondentHasRoleFacade)
    registrar.register_relationship_get_route(CorrespondentHasRoleFacade, 'roles-within-document')

    #registrar.register_post_routes(CorrespondentHasRole, CorrespondentHasRoleFacade)
