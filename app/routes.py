from flask import current_app

from app import iiif_bp, JSONAPIResponseFactory
from app.models import Witness, Document

headers = {"Access-Control-Allow-Origin": "*"}

@iiif_bp.route("/iiif/witnesses/<witness_id>/manifest")
def get_witness_manifest(witness_id):
    witness = Witness.query.filter(Witness.id == witness_id).first()
    if witness is None:
        code = 400
        data = {"message": "Witness does not exist"}
        return JSONAPIResponseFactory.make_errors_response({
            "status": code,
            "title": data
        }), code

    manifest, manifest_url = current_app.manifest_factory.make_manifest(witness=witness)
    print('get manifest', manifest_url)

    return JSONAPIResponseFactory.make_response(manifest, headers=headers)


@iiif_bp.route("/iiif/documents/<doc_id>/collection")
def get_document_collection(doc_id):
    doc = Document.query.filter(Document.id == doc_id).first()
    if doc is None:
        code = 400
        data = {"message": "Document does not exist"}
        return JSONAPIResponseFactory.make_errors_response({
            "status": code,
            "title": data
        }), code

    collection, collection_url = current_app.manifest_factory.make_collection(doc)
    print('get collection', collection_url)

    return JSONAPIResponseFactory.make_response(collection, headers=headers)

