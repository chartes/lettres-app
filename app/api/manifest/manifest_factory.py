import datetime
import json
import pathlib
import re
from html.parser import HTMLParser

class HTMLToTextWithLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.current_href = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr, value in attrs:
                if attr == "href":
                    self.current_href = value

    def handle_endtag(self, tag):
        if tag == "a" and self.current_href:
            # Ajouter l'URL après le texte du lien
            self.result.append(f" ({self.current_href})")
            self.current_href = None

    def handle_data(self, data):
        self.result.append(data)

    def get_text(self):
        text = ''.join(self.result)
        # Nettoyage des espaces
        text = re.sub(r'\s+,', ',', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text


def html_to_text_with_links(html):
    parser = HTMLToTextWithLinks()
    parser.feed(html)
    return parser.get_text()

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
        from app.api.document.facade import DocumentFacade
        f_obj, errors, kwargs = DocumentFacade.get_resource_facade('', witness.document_id)
        manifest["label"] = f_obj.resource["attributes"]["title"]
        manifest["metadata"] = [{"label":"Citation","value": witness.content}]

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
        """
            Récupère le manifeste IIIF depuis Gallica en utilisant pyGallica.
        """
        match = re.search(r"(ark:/\d+/[a-z0-9]+)", manifest_url)
        if match:
            ark = match.group(1)
            print("\n_fetch manifest_url / ark : ", manifest_url, ark)

            try:
                # create required headers, in particular a referer
                referer = request.host_url[:-1]
                headers = {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                                  "(KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
                    "referer": referer,
                    "Accept": "application/json"
                }

                r = requests.get(manifest_url, headers=headers)
                manifest = r.json()
                print("fetching... %s manifest_url, response status \n" % manifest_url, r.status_code)

                # security : create sequences key if missing
                if "sequences" not in manifest:
                    manifest["sequences"] = [{"@id": f"{manifest_url}/sequence/normal", "canvases": []}]
                return manifest

            except Exception as e:
                print("Error fetching manifest manifest_url / error : ", manifest_url, e)
                return {"@id": manifest_url, "sequences": [{"@id": f"{manifest_url}/sequence/normal", "canvases": []}]}

        else:
            print("\n_fetch no ark found for manifest_url : ", manifest_url)
            return {"@id": manifest_url, "sequences": [{"@id": f"{manifest_url}/sequence/normal", "canvases": []}]}


        #r = requests.get(manifest_url)
        #print("fetching... %s \n" % manifest_url, end=" ", flush=True)
        #manifest = r.json()
        #print("fetching... %s manifest \n" % manifest_url, manifest, r)
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
                print("_get_from_cache try manifest_url : ", manifest_url)
            except Exception as e:
                print("_get_from_cache try cannot get manifest_url, error : ", manifest_url, e)
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
            try:
                width = int(manifest["sequences"][0]["canvases"][0]["width"])
                height = int(manifest["sequences"][0]["canvases"][0]["height"])
            except (KeyError, IndexError, TypeError, ValueError):
                width = height = 0
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
                if "[" not in canvas["label"]:
                    canvas["label"] = f'[f. {canvas["label"]}]'
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
