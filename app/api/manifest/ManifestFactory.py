import json
import requests
from flask import current_app, request



class ManifestFactory(object):

    MANIFEST_TEMPLATE_FILENAME = "app/api/manifest/manifest_template.json"
    COLLECTION_TEMPLATE_FILENAME = "app/api/manifest/collection_template.json"

    def __init__(self):
        with open(ManifestFactory.MANIFEST_TEMPLATE_FILENAME, 'r') as f:
            self.manifest_template = json.load(f)
        with open(ManifestFactory.COLLECTION_TEMPLATE_FILENAME, 'r') as f:
            self.collection_template = json.load(f)

    def make_collection(self, collection_url, doc):
        collection = self.collection_template.copy()

        from app.api.witness.facade import WitnessFacade

        manifest_urls = []
        url_prefix = request.host_url[:-1] + current_app.config["API_URL_PREFIX"]

        for witness in doc.witnesses:
            f_obj, errors, kwargs = WitnessFacade.get_facade(url_prefix, witness)
            manifest_url = f_obj.resource["attributes"]["manifest-url"]
            if manifest_url is not None:
                manifest_urls.append(manifest_url)

        collection["@id"] = collection_url
        collection["manifests"] = manifest_urls

        #from app import db
        #from app.models import Image
        #for img in Image.query.all():
        #    _cid = img.canvas_id.replace("/full/full/0/native.jpg", "")
        #    url, name = _cid.rsplit("/", maxsplit=1)
        #    img.canvas_id = "{url}/canvas/{name}".format(url=url, name=name)
        #    db.session.add(img)
        #db.session.commit()

        return collection

    def make_manifest(self, manifest_url, witness):
        manifest = self.manifest_template.copy()

        # ==== manifest @id
        manifest["@id"] = manifest_url
        # ==== manifest related
        manifest["related"] = manifest_url.split("/witnesses")[0] + "/documents/%s" % witness.document_id

        # ==== sequence @id
        seq = manifest_url.replace("/manifest", "/sequence/normal")
        manifest["sequences"][0]["@id"] = seq

        # ==== canvases
        ordered_images = [i for i in witness.images]
        ordered_images.sort(key=lambda i: i.order_num)
        # group images by manifest url
        grouped_images = {}
        for img in ordered_images:
            url = img.canvas_id.rsplit("/", maxsplit=2)[0]
            orig_manifest_url = "{url}/manifest.json".format(url=url)

            if orig_manifest_url not in grouped_images:
                grouped_images[orig_manifest_url] = []

            grouped_images[orig_manifest_url].append(img.canvas_id)

        # fetching canvases from manifests
        canvases = []
        for orig_manifest_url, canvas_ids in grouped_images.items():
            new_canvases = ManifestFactory.fetch_canvas(orig_manifest_url, canvas_ids)
            canvases.extend(new_canvases)

        manifest["sequences"][0]["canvases"] = canvases

        return manifest

    @staticmethod
    def fetch_canvas(manifest_url, canvas_ids):
        r = requests.get(manifest_url)
        print("fetching... %s" % manifest_url, end=" ", flush=True)
        manifest = r.json()
        print(r.status_code)
        return [canvas for canvas in manifest["sequences"][0]["canvases"]
                if canvas["@id"] in canvas_ids]
