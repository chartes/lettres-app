import json
import pprint
from flask import current_app, request, Response

from app import api_bp, JSONAPIResponseFactory
from app.models import Witness, Document

CONTENT_TYPE = "application/json; charset=utf-8"
HEADERS = {"Access-Control-Allow-Origin": "*",
           "Access-Control-Allow-Methods": ["GET"]}


@api_bp.route("/api/<api_version>/witnesses/<witness_id>/manifest")
def get_manifest(api_version, witness_id):
    witness = Witness.query.filter(Witness.id == witness_id).first()
    if witness:
        if witness.images and len(witness.images) > 0:
            try:
                manifest = current_app.manifest_factory.make_manifest(request.url, witness)
                if len(manifest["sequences"][0]["canvases"]) == 0:
                    raise Exception("Cannot fetch canvases")
            except Exception as e:
                return JSONAPIResponseFactory.make_errors_response(
                    {
                        "status": 403,
                        "title": "Cannot build manifest for Witness %s" % witness_id,
                        "details": str(e)
                    }, status=403
                )

            response = Response(
                json.dumps(manifest, indent=2, ensure_ascii=False),
                content_type=CONTENT_TYPE,
                headers=HEADERS,
            )
            return response, 200
        else:
            return JSONAPIResponseFactory.make_errors_response(
                {"status": 404, "title": "Witness %s does not have any images" % witness_id}, status=404
            )

    else:
        return JSONAPIResponseFactory.make_errors_response(
               {"status": 404, "title": "Witness %s does not exist" % witness_id}, status=404
        )


@api_bp.route("/api/<api_version>/documents/<doc_id>/collection")
def get_collection(api_version, doc_id):
    document = Document.query.filter(Document.id == doc_id).first()
    if document:
        if document.witnesses and len(document.witnesses) > 0:
            manifest = current_app.manifest_factory.make_collection(request.url, document)
            response = Response(
                json.dumps(manifest, indent=2, ensure_ascii=False),
                content_type=CONTENT_TYPE,
                headers=HEADERS,
            )
            return response, 200
        else:
            return JSONAPIResponseFactory.make_errors_response(
                {"status": 404, "title": "Document %s does not have any witnesses" % doc_id}, status=404
            )

    else:
        return JSONAPIResponseFactory.make_errors_response(
               {"status": 404, "title": "Document %s does not exist" % doc_id}, status=404
        )
