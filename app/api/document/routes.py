from app.api.document.facade import DocumentFacade
from app.models import Document


def register_document_api_urls(app):
    registrar = app.api_url_registrar
    registrar.register_get_routes(Document, DocumentFacade)

    registrar.register_relationship_get_route(DocumentFacade, 'images')
    registrar.register_relationship_get_route(DocumentFacade, 'notes')

    registrar.register_relationship_get_route(DocumentFacade, 'languages')
    registrar.register_relationship_get_route(DocumentFacade, 'institution')
    registrar.register_relationship_get_route(DocumentFacade, 'tradition')

    registrar.register_relationship_get_route(DocumentFacade, 'correspondents-having-roles')
    registrar.register_relationship_get_route(DocumentFacade, 'roles')
    registrar.register_relationship_get_route(DocumentFacade, 'correspondents')

    registrar.register_relationship_get_route(DocumentFacade, 'owner')
    registrar.register_relationship_get_route(DocumentFacade, 'whitelist')

    registrar.register_relationship_get_route(DocumentFacade, 'prev-document')
    registrar.register_relationship_get_route(DocumentFacade, 'next-document')

    #registrar.register_post_routes(Document, DocumentFacade)
