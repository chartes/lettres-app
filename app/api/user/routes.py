from app.api.user.facade import UserFacade
from app.models import User


def register_user_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(User, UserFacade)

    registrar.register_relationship_get_route(UserFacade, 'role')
    registrar.register_relationship_get_route(UserFacade, 'owned-documents')

    #registrar.register_relationship_get_route(CorrespondentRoleFacade, 'roles-within-document')
    #registrar.register_post_routes(CorrespondentRole, CorrespondentRoleFacade)
