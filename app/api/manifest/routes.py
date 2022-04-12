
import json
from flask import current_app, request, Response, url_for


from app import api_bp, JSONAPIResponseFactory
from app.models import Document

CONTENT_TYPE = "application/json; charset=utf-8"
HEADERS = {"Access-Control-Allow-Origin": "*",
           "Access-Control-Allow-Methods": ["GET"]}


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


#def upload_manifest(filename, manifest, upload=True):
#    SFTP_CONFIG = {
#        "host": current_app.config.get("SFTP_IIIF_HOST", ""),
#        "username": current_app.config.get("SFTP_IIIF_USERNAME", ""),
#        "password": current_app.config.get("SFTP_IIIF_PASSWORD", ""),
#        "default_path": current_app.config.get("SFTP_IIIF_DEFAULT_MANIFEST_PATH", "/srv/manifests")
#    }
#    # write to the temp folder first
#    with open(filename, 'w') as f:
#        f.write(json.dumps(manifest, indent=2, ensure_ascii=False))
#        f.flush()
#    if upload:
#        # upload the file
#        with pysftp.Connection(**SFTP_CONFIG) as srv:
#            srv.put(filename)
#
#
#def upload_collection(filename, collection, upload=True):
#    SFTP_CONFIG = {
#        "host": current_app.config.get("SFTP_IIIF_HOST", ""),
#        "username": current_app.config.get("SFTP_IIIF_USERNAME", ""),
#        "password": current_app.config.get("SFTP_IIIF_PASSWORD", ""),
#        "default_path": current_app.config.get("SFTP_IIIF_DEFAULT_COLLECTION_PATH", "/srv/collections")
#    }
#    # write to the temp folder first
#    with open(filename, 'w') as f:
#        f.write(json.dumps(collection, indent=2, ensure_ascii=False))
#        f.flush()
#
#    if upload:
#        with pysftp.Connection(**SFTP_CONFIG) as srv:
#            srv.put(filename)


#def rework_manifest_data(data, witness):
#    manifest = json.loads(data)
#    if manifest["label"] == "Manifest":
#        manifest["label"] = witness.content
#    manifest["@id"] = "{0}/manifest{1}.json".format(current_app.config["IIIF_MANIFEST_ENDPOINT"], witness.id)
#    manifest["related"] = request.host_url[:-1] + url_for('app_bp.index', doc_id=witness.document_id)
#    manifest["sequences"][0]["@id"] = manifest["sequences"][0]["@id"].replace("template.json",
#                                                                              "manifest%s.json" % witness.id)
#    current_img_num = 1
#    for i, canvas in enumerate(manifest["sequences"][0]["canvases"]):
#        canvas["@id"] = "{0}/canvas/f{1}".format(manifest["@id"], i+1)
#        for img in canvas["images"]:
#            img["@id"] = "{0}/f{1}.img".format(manifest["@id"], current_img_num)
#            img["on"] = canvas["@id"]
#            current_img_num += 1
#
#    tmp = current_app.config.get('LOCAL_TMP_FOLDER')
#    tmp_filename = os.path.join(tmp, "manifest%s.json" % witness.id)
#    upload_manifest(tmp_filename, manifest)
#
#    return manifest
#
#
#def rework_collection_data(doc_id=None):
#    doc = Document.query.filter(Document.id == doc_id).first()
#    collection, collection_url = current_app.manifest_factory.make_collection(doc)
#
#    tmp = current_app.config.get('LOCAL_TMP_FOLDER')
#    tmp_filename = os.path.join(tmp, "document%s.json" % doc_id)
#    upload_collection(tmp_filename, collection)
#
#    return collection, collection_url
#
#
#@api_require_roles("contributor")
#@api_bp.route("/api/<api_version>/iiif/editor/manifests", methods=('GET', 'POST'))
#@api_bp.route("/api/<api_version>/iiif/editor/manifests/<manifest_id>", methods=('GET', 'POST'))
#def iiif_editor_manifest(api_version, manifest_id=None):
#    if manifest_id is None:
#        manifest_id = request.referrer.rsplit('/', maxsplit=1)[-1]
#
#    witness = Witness.query.filter(Witness.id == manifest_id).first()
#    if witness is None:
#        code = 403
#        data = {"message": "Wrong witness"}
#        return JSONAPIResponseFactory.make_errors_response({
#            "status": code,
#            "title": data
#        }), code
#
#    if request.method == 'POST':
#        # rework the manifest data to make sure the ids match the witness
#        manifest = rework_manifest_data(request.data, witness)
#        # rework the collection (add/update the new manifest)
#        collection, collection_url = rework_collection_data(witness.document_id)
#
#        data = {
#            #"{0}/manifest{1}.json".format(current_app.config["IIIF_MANIFEST_ENDPOINT"], manifest_id)
#            "uri": request.host_url[:-1] + url_for('api_bp.put_manifest', manifest_id=manifest_id, api_version=1.0)
#        }
#        code = 200
#    else:
#        code = 200
#        if manifest_id is None:
#            data = {
#                "manifests": [
#                    {"uri": "{0}/manifest{1}.json".format(current_app.config["IIIF_MANIFEST_ENDPOINT"], manifest_id) },
#                ]
#            }
#        else:
#            data = {
#                       "@context": "http://iiif.io/api/presentation/2/context.json",
#                       "@id": "example-manifest",
#                       "@type": "sc:Manifest",
#                       "label": "Example Manifest",
#                       "metadata": [],
#                       "description": [
#                           {
#                               "@value": "Example Description",
#                               "@language": "en"
#                           }
#                       ],
#                       "license": "https://creativecommons.org/licenses/by/3.0/",
#                       "attribution": "Example Attribution",
#                       "sequences": [
#                           {
#                               "@id": "example-sequence",
#                               "@type": "sc:Sequence",
#                               "label": [
#                                   {
#                                       "@value": "Example Sequence Label",
#                                       "@language": "en"
#                                   }
#                               ],
#                               "canvases": []
#                           }
#                       ],
#                       "structures": []
#                   },
#
#    return JSONAPIResponseFactory.make_response(data), code
#
#
#@api_require_roles("contributor")
#@api_bp.route("/api/<api_version>/iiif/editor/manifests/<manifest_id>", methods=['PUT'])
#def put_manifest(api_version, manifest_id):
#    witness = Witness.query.filter(Witness.id == manifest_id).first()
#    if witness is None:
#        code = 403
#        data = {"message": "Wrong witness"}
#        return JSONAPIResponseFactory.make_errors_response({
#            "status": code,
#            "title": data
#        }), code
#    else:
#        try:
#            # rework the manifest data to make sure the ids match the witness
#            manifest = rework_manifest_data(request.data, witness)
#            # rework the collection (add/update the new manifest)
#            collection, collection_url = rework_collection_data(witness.document_id)
#
#            data = {"message": "Manifest successfully updated"}
#            code = 201
#
#            return JSONAPIResponseFactory.make_response(data), code
#        except Exception as e:
#            print(e)
#            code = 403
#            return JSONAPIResponseFactory.make_errors_response({
#                "status": code,
#                "title": str(e)
#            }), code




