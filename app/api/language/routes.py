from app.api.language.facade import LanguageFacade
from app.models import Language


def register_language_role_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(Language, LanguageFacade)
    registrar.register_post_routes(Language, LanguageFacade)
    registrar.register_patch_routes(Language, LanguageFacade)

    registrar.register_relationship_get_route(LanguageFacade, 'documents')
    registrar.register_relationship_post_route(LanguageFacade, 'documents')

