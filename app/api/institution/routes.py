from app.api.institution.facade import InstitutionFacade
from app.models import Institution


def register_institution_role_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(Institution, InstitutionFacade)
    registrar.register_post_routes(Institution, InstitutionFacade)
    registrar.register_patch_routes(Institution, InstitutionFacade)
    registrar.register_delete_routes(Institution, InstitutionFacade)

    registrar.register_relationship_get_route(InstitutionFacade, 'witnesses')

    registrar.register_relationship_get_route(InstitutionFacade, 'changes')
    registrar.register_relationship_post_route(InstitutionFacade, 'changes')
