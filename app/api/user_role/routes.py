from app.api.user_role.facade import UserRoleFacade
from app.models import UserRole


def register_user_role_api_urls(app):
    registrar = app.api_url_registrar
    registrar.register_get_routes(UserRole, UserRoleFacade)
    registrar.register_relationship_get_route(UserRoleFacade, 'users')