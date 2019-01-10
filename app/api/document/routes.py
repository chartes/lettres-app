from app.api.document.facade import DocumentFacade
from app.models import Document


def register_document_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(Document, DocumentFacade)
    registrar.register_post_routes(Document, DocumentFacade)
    registrar.register_patch_routes(Document, DocumentFacade)
    registrar.register_delete_routes(Document, DocumentFacade)

    for rel in ('notes', 'languages', 'witnesses',
                'correspondents-having-roles', 'roles', 'correspondents', 'collections',
                'owner', 'whitelist', 'prev-document', 'next-document'):
        registrar.register_relationship_get_route(DocumentFacade, rel)

    for rel in ( 'notes', 'languages', 'witnesses', 'collections',
                'correspondents-having-roles',  # 'roles', 'correspondents',
                'owner', 'whitelist', 'next-document'):  # , 'prev-document':
        registrar.register_relationship_post_route(DocumentFacade, rel)
        registrar.register_relationship_patch_route(DocumentFacade, rel)
