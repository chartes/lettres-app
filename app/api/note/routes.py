from app.api.note.facade import NoteFacade
from app.models import Note


def register_note_api_urls(app):
    registrar = app.api_url_registrar
    registrar.register_get_routes(Note, NoteFacade)
    #registrar.register_relationship_get_route(CorrespondentRoleFacade, 'roles-within-document')

    #registrar.register_post_routes(CorrespondentRole, CorrespondentRoleFacade)
