import datetime
import json
import pathlib

import requests
from flask import current_app, request
from operator import attrgetter

from app.api.document.facade import DocumentFacade
from app.api.witness.facade import WitnessFacade


dir = pathlib.Path(__file__).parent.resolve()

class ManifestFactory(object):

    MANIFEST_TEMPLATE_FILENAME = dir / "manifest_template.json"
    COLLECTION_TEMPLATE_FILENAME = dir / "collection_template.json"

    CACHED_MANIFESTS = {

    }

    CACHE_DURATION = 1800    # cache manifests (in seconds)
    CACHE_ENTRY_MAX = 150    # how many manifests to cache

    def __init__(self):
        with open(ManifestFactory.MANIFEST_TEMPLATE_FILENAME, 'r') as f:
            self.manifest_template = json.load(f)
        with open(ManifestFactory.COLLECTION_TEMPLATE_FILENAME, 'r') as f:
            self.collection_template = json.load(f)

    def make_collection(self, doc):
        f_obj, errors, kwargs = DocumentFacade.get_facade('', doc)
        collection_url = f_obj.get_iiif_collection_url()
        collection = dict(self.collection_template)

        manifest_urls = []
        for witness in sorted(doc.witnesses, key=attrgetter('num')):
            f_obj, errors, kwargs = WitnessFacade.get_facade('', witness)
            manifest_url = f_obj.get_iiif_manifest_url()
            if manifest_url is not None and (manifest_url, witness) not in manifest_urls:
                manifest_urls.append((manifest_url, witness))

        collection["@id"] = collection_url
        collection["manifests"] = []
        for i, (url, witness) in enumerate(manifest_urls):
            manifest = {
                "@id": url,
                "@type": "sc:Manifest",
                "label": witness.content
            }
            collection["manifests"].append(manifest)

        return collection, collection_url

    def make_manifest(self, witness):
        api_prefix_url = request.host_url[:-1] + current_app.config['API_URL_PREFIX']

        f_obj, errors, kwargs = WitnessFacade.get_facade('', witness)
        manifest_url = f_obj.get_iiif_manifest_url()

        manifest = dict(self.manifest_template)

        # ==== manifest @id
        manifest["@id"] = manifest_url
        # ==== manifest related
        manifest["related"] = f"{api_prefix_url}/documents/{witness.document_id}"

        # === manifest label
        manifest["label"] = witness.content

        # ==== sequence @id
        seq = f"{manifest_url}/sequence/normal"
        manifest["sequences"][0]["@id"] = seq

        # ==== canvases
        if witness.images is None:
            witness.images = []
        ordered_images = [i for i in witness.images]
        ordered_images.sort(key=lambda i: i.order_num)

        # group images by manifest url
        grouped_images = {}
        for img in ordered_images:
            # /!\ maybe tied to the manifest url naming scheme in Gallica
            url = img.canvas_id.rsplit("/", maxsplit=2)[0]
            orig_manifest_url = "{url}/manifest.json".format(url=url)#url=img.canvas_id
            print("orig_manifest_url", orig_manifest_url)

            if orig_manifest_url not in grouped_images:
                grouped_images[orig_manifest_url] = []

            grouped_images[orig_manifest_url].append(img.canvas_id)

        # fetching canvases from manifests
        canvases = []
        fetch_canvas = current_app.manifest_factory.fetch_canvas
        for orig_manifest_url, canvas_ids in grouped_images.items():
            new_canvases = fetch_canvas(orig_manifest_url, canvas_ids, cache=True)
            canvases.extend(new_canvases)

        manifest["sequences"][0]["canvases"] = canvases

        return manifest, manifest_url

    @classmethod
    def _fetch(cls, manifest_url):
        r = requests.get(manifest_url)
        #print("fetching... %s" % manifest_url, end=" ", flush=True)
        manifest = r.json()
        #print(r.status_code)
        # gallica returns incorrect canvases height and width now and then, they are accessed this way
        # width = int(manifest["sequences"][0]["canvases"][0]["width"])
        # height = int(manifest["sequences"][0]["canvases"][0]["height"])

        return manifest

    @classmethod
    def _get_from_cache(cls, manifest_url):
        #print("\n cls.CACHED_MANIFESTS.keys()", cls.CACHED_MANIFESTS.keys())
        if manifest_url not in cls.CACHED_MANIFESTS.keys():
            try:
                manifest = cls._fetch(manifest_url)
            except Exception as e:
                print("cannot get manifest", manifest_url)
                manifest = {}
            if len(cls.CACHED_MANIFESTS.keys()) >= cls.CACHE_ENTRY_MAX:
                l = [(dt, url) for url, (_, dt) in cls.CACHED_MANIFESTS.items()]
                l.sort(reverse=True)
                oldest_cached_url = l[0][1]
                cls.CACHED_MANIFESTS.pop(oldest_cached_url)
                #print("popped", oldest_cached_url)
            #print("caching", manifest_url)
            cls.CACHED_MANIFESTS[manifest_url] = (manifest, datetime.datetime.now())
            #print("nb cache entries:", len(cls.CACHED_MANIFESTS.keys()))
            return manifest
        else:
            manifest, dt = cls.CACHED_MANIFESTS[manifest_url]
            # gallica returns incorrect (-1) canvases height & width now and then, test before refreshing cache
            width = int(manifest["sequences"][0]["canvases"][0]["width"])
            height = int(manifest["sequences"][0]["canvases"][0]["height"])
            if (width > 0) and (height > 0):
                #print("get from cache")
                # refresh the cache entry
                duration = datetime.datetime.now() - dt
                if duration.total_seconds() > cls.CACHE_DURATION:
                    cls.CACHED_MANIFESTS.pop(manifest_url)
                    #print("refresh cache entry")
                    return cls._get_from_cache(manifest_url)
                else:
                    # extending cache duration
                    cls.CACHED_MANIFESTS[manifest_url] = (manifest, datetime.datetime.now())
                    return manifest
            else:
                # canvases height & width are incorrect, do not refresh cached manifest
                # extending cache duration
                cls.CACHED_MANIFESTS[manifest_url] = (manifest, datetime.datetime.now())
                return manifest

    @classmethod
    def fetch_canvas(cls, manifest_url, canvas_ids, cache=False):
        if cache:
            manifest = cls._get_from_cache(manifest_url)
            print("fetch_canvas if")
        else:
            print("fetch_canvas else")
            manifest = cls._fetch(manifest_url)

        try:
            canvases = [canvas for canvas in manifest["sequences"][0]["canvases"]
                    if canvas["@id"] in canvas_ids if "sequences" in manifest]

            for canvas in canvases:
                # gallica returns incorrect canvases height and width now and then, they are accessed this way
                width = int(canvas["width"])
                height = int(canvas["height"])

                # test if height and width are valid, otherwise fetch from folio info.json instead
                if (width < 0) or (height < 0):
                    folio = canvas["@id"].rsplit("/", maxsplit=2)[-1]
                    folio_url = manifest_url.rsplit("manifest.json")[0] + folio
                    folio_manifest_url = "{folio_url}/info.json".format(folio_url=folio_url)
                    rfolio = requests.get(folio_manifest_url)
                    correct_width = int(rfolio.json()["width"])
                    correct_height = int(rfolio.json()["height"])
                    canvas["width"] = correct_width
                    canvas["height"] = correct_height
                    canvas["images"][0]["resource"]["width"] = correct_width
                    canvas["images"][0]["resource"]["height"] = correct_height
        except KeyError as err:
            print("KeyError", err)
            canvases = []

        return canvases
