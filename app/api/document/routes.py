from app.api.decorators import api_require_roles
from app.api.document.facade import DocumentFacade
from app.models import Document


def register_document_api_urls(app):
    registrar = app.api_url_registrar

    registrar.register_get_routes(Document, DocumentFacade, [api_require_roles("contributor")])
    registrar.register_post_routes(Document, DocumentFacade, [api_require_roles("admin")])
    registrar.register_patch_routes(Document, DocumentFacade, [api_require_roles("contributor")])
    registrar.register_delete_routes(Document, DocumentFacade, [api_require_roles("admin")])

    for rel in ('notes', 'languages', 'witnesses', 'images', 'locks', 'changes',
                'correspondents-having-roles', 'roles', 'correspondents', 'collections',
                'prev-document', 'next-document'):
        registrar.register_relationship_get_route(DocumentFacade, rel)

    for rel in ('notes', 'languages', 'witnesses', 'collections', 'locks', 'changes',
                'correspondents-having-roles',
                'whitelist', 'next-document'):
        registrar.register_relationship_post_route(DocumentFacade, rel)

    for rel in ('notes', 'languages', 'witnesses', 'collections',
                'correspondents-having-roles',
                'whitelist', 'next-document'):
        registrar.register_relationship_patch_route(DocumentFacade, rel)
