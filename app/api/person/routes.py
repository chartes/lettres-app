from flask import jsonify

from app import api_bp
from app.api.person.facade import PersonFacade
from app.models import Person


def register_person_api_urls(app):
    registrar = app.api_url_registrar
    registrar.register_get_routes(Person, PersonFacade)
    registrar.register_post_routes(Person, PersonFacade)
    registrar.register_patch_routes(Person, PersonFacade)
    registrar.register_delete_routes(Person, PersonFacade)

    registrar.register_relationship_get_route(PersonFacade, 'documents')
    registrar.register_relationship_post_route(PersonFacade, 'documents')
    registrar.register_relationship_patch_route(PersonFacade, 'documents')

    registrar.register_relationship_get_route(PersonFacade, 'roles-within-documents')
    registrar.register_relationship_post_route(PersonFacade, 'roles-within-documents')
    registrar.register_relationship_patch_route(PersonFacade, 'roles-within-documents')

    registrar.register_relationship_get_route(PersonFacade, 'changes')
    registrar.register_relationship_post_route(PersonFacade, 'changes')

    @api_bp.route('/api/<api_version>/all-persons')
    def all_persons(api_version):
        persons = Person.query.with_entities(Person.label).distinct().order_by(Person.label).all()
        response = jsonify({"data": [p[0] for p in persons]})
        return response, 200

