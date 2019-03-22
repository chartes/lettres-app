import os

import json
import pprint
from flask import current_app, request, Response
import pysftp
import sys


from app import api_bp, JSONAPIResponseFactory
from app.api.decorators import api_require_roles
from app.models import Witness, Document

CONTENT_TYPE = "application/json; charset=utf-8"
HEADERS = {"Access-Control-Allow-Origin": "*",
           "Access-Control-Allow-Methods": ["GET"]}


#@api_bp.route("/api/<api_version>/iiif/witnesses/<witness_id>/manifest")
#def get_manifest(api_version, witness_id):
#    witness = Witness.query.filter(Witness.id == witness_id).first()
#    if witness:
#        #if witness.images and len(witness.images) > 0:
#        #try:
#        #    manifest = current_app.manifest_factory.make_manifest(request.url, witness)
#        #    if len(manifest["sequences"][0]["canvases"]) == 0:
#        #        raise Exception("Cannot fetch canvases")
#        #except Exception as e:
#        #    return JSONAPIResponseFactory.make_errors_response(
#        #        {
#        #            "status": 403,
#        #            "title": "Cannot build manifest for Witness %s" % witness_id,
#        #            "details": str(e)
#        #        }, status=403
#        #    )
#        manifest = current_app.manifest_factory.make_manifest(request.url, witness)
#        response = Response(
#            json.dumps(manifest, indent=2, ensure_ascii=False),
#            content_type=CONTENT_TYPE,
#            headers=HEADERS,
#        )
#        return response, 200
#        #else:
#        #    return JSONAPIResponseFactory.make_errors_response(
#        #        {"status": 404, "title": "Witness %s does not have any images" % witness_id}, status=404
#        #    )
#
#    else:
#        return JSONAPIResponseFactory.make_errors_response(
#               {"status": 404, "title": "Witness %s does not exist" % witness_id}, status=404
#        )
#

@api_bp.route("/api/<api_version>/iiif/editor/manifests/<witness_id>/template")
def get_manifest_template(api_version, witness_id):
    witness = Witness.query.filter(Witness.id == witness_id).first()
    host = request.host_url
    # TODO : faire un manifest template (avec les bonnes urls dedans quand même)
    manifest, manifest_url = current_app.manifest_factory.make_manifest(host, witness)

    response = Response(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        content_type=CONTENT_TYPE,
        headers=HEADERS,
    )
    return response, 200

@api_bp.route("/api/<api_version>/iiif/documents/<doc_id>/collection/default")
def get_collection(api_version, doc_id):
    document = Document.query.filter(Document.id == doc_id).first()
    if document:
        collection, collection_url = current_app.manifest_factory.make_collection(document)
        response = Response(
            json.dumps(collection, indent=2, ensure_ascii=False),
            content_type=CONTENT_TYPE,
            headers=HEADERS,
        )
        return response, 200
    else:
        return JSONAPIResponseFactory.make_errors_response(
            {"status": 404, "title": "Document %s does not exist" % doc_id}, status=404
        )

def upload_manifest(filename):
    SFTP_CONFIG = {
        "host": current_app.config.get("SFTP_IIIF_HOST", ""),
        "username": current_app.config.get("SFTP_IIIF_USERNAME", ""),
        "password": current_app.config.get("SFTP_IIIF_PASSWORD", ""),
        "default_path": current_app.config.get("SFTP_IIIF_DEFAULT_MANIFEST_PATH", "/srv/manifests")
    }
    # print(SFTP_CONFIG)
    with pysftp.Connection(**SFTP_CONFIG) as srv:
        srv.put(filename)


def upload_collection(filename):
    SFTP_CONFIG = {
        "host": current_app.config.get("SFTP_IIIF_HOST", ""),
        "username": current_app.config.get("SFTP_IIIF_USERNAME", ""),
        "password": current_app.config.get("SFTP_IIIF_PASSWORD", ""),
        "default_path": current_app.config.get("SFTP_IIIF_DEFAULT_COLLECTION_PATH", "/srv/collections")
    }
    # print(SFTP_CONFIG)
    with pysftp.Connection(**SFTP_CONFIG) as srv:
        srv.put(filename)


@api_require_roles("contributor")
@api_bp.route("/api/<api_version>/iiif/editor/manifests", methods=('GET', 'POST'))
@api_bp.route("/api/<api_version>/iiif/editor/manifests/<manifest_id>", methods=('GET', 'POST'))
def iiif_editor_manifest(api_version, manifest_id=None):
    if manifest_id is None:
        manifest_id = request.referrer.rsplit('/', maxsplit=1)[-1]

    if request.method == 'POST':

        #tmp_filename = os.path.join(current_app.config.get('LOCAL_TMP_FOLDER'), "manifest{0}.json".format(manifest_id.id))
        #print(tmp_filename, manifest_url, end="... ", flush=False)
        #with open(tmp_filename, 'w') as f:
        #    f.write(json.dumps(manifest))
        #    f.flush()
        #    if upload:
        #        upload_manifest(tmp_filename)
        #        print('uploaded', end="... ", flush=True)
        #    print('OK')


        data = {
            "uri": "http://localhost:5004/lettres/api/1.0/iiif/witnesses/%s/manifest" % manifest_id
        }
        code = 200
    else:
        code = 200
        if manifest_id is None:
            data = {
                "manifests": [
                    {"uri": "http://localhost:5004/lettres/api/1.0/iiif/witnesses/%s/manifest" % manifest_id},
                ]
            }
        else:
            data = {
                       "@context": "http://iiif.io/api/presentation/2/context.json",
                       "@id": "example-manifest",
                       "@type": "sc:Manifest",
                       "label": "Example Manifest",
                       "metadata": [],
                       "description": [
                           {
                               "@value": "Example Description",
                               "@language": "en"
                           }
                       ],
                       "license": "https://creativecommons.org/licenses/by/3.0/",
                       "attribution": "Example Attribution",
                       "sequences": [
                           {
                               "@id": "example-sequence",
                               "@type": "sc:Sequence",
                               "label": [
                                   {
                                       "@value": "Example Sequence Label",
                                       "@language": "en"
                                   }
                               ],
                               "canvases": []
                           }
                       ],
                       "structures": []
                   },

    return JSONAPIResponseFactory.make_response(data), code


@api_require_roles("contributor")
@api_bp.route("/api/<api_version>/iiif/witnesses/<witness_id>/manifest", methods=('PUT', ))
def put_manifest(api_version, witness_id):
    if witness_id is None:
        code = 403
        data = {
            "message": "Wrong witness"
        }
    else:
        data = {
            "message": "Manifest successfully updated"
        }
        code = 201

        tmp_filename = os.path.join(current_app.config.get('LOCAL_TMP_FOLDER'), "manifest%s.json" % witness_id)
        print(tmp_filename)
        with open(tmp_filename, 'wb') as f:
            f.write(request.data)
            f.flush()
            upload_manifest(tmp_filename)

    return JSONAPIResponseFactory.make_response(data), code


