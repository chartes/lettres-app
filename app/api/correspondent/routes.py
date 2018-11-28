from app.api.correspondent.facade import CorrespondentFacade
from app.models import Correspondent


def register_correspondent_api_urls(app):
    registrar = app.api_url_registrar
    registrar.register_get_routes(Correspondent, CorrespondentFacade)
    registrar.register_post_routes(Correspondent, CorrespondentFacade)

    registrar.register_relationship_get_route(CorrespondentFacade, 'documents')

    registrar.register_relationship_get_route(CorrespondentFacade, 'roles-within-documents')
    #registrar.register_relationship_post_route(CorrespondentFacade, 'roles-within-documents')
