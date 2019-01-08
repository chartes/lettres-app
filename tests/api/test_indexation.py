import pprint
import unittest

from tests.base_server import TestBaseServer
from app import db

class TestIndexation(TestBaseServer):

    DOC_INDEX_NAME = "lettres__testing__document"

    def load_fixtures(self):
        from ..data.fixtures.dataset001 import load_fixtures as load_dataset001
        with self.app.app_context():
            load_dataset001(db)

    def test_doc_attribute_change(self):
        r, s, res = self.api_patch("documents/1", data={
            "data": {
                "id": 1,
                "type": "document",
                "attributes": {
                    "title": "Document TestIndexation"
                }
            }
        })
        self.assert200(r)

        r, status, resource = self.api_get("documents/1")
        self.assert200(r)
        self.assertEqual("Document TestIndexation", resource["data"]["attributes"]["title"])

        resource = self.search(self.DOC_INDEX_NAME, "*")
        self.assertEqual(1, resource["meta"]["total-count"])
        self.assertEqual(1, resource["data"][0]["id"])

    def test_language_attribute_change(self):
        # add a new language
        r, status, res = self.api_post("languages", data={
            "data": {
                "id": 99,
                "type": "language",
                "attributes": {
                    "code": "TST",
                    "label": "Test"
                }
            }
        })
        self.assertEqual('201 CREATED', status)

        r, s, res = self.api_post("documents/1/relationships/languages", data={
            "data": [
                {"type": "language", "id": 99},
             ]
        })
        self.assert200(r)

        resource = self.search(self.DOC_INDEX_NAME, "TST")
        pprint.pprint(resource)
        self.assertEqual(1, resource["meta"]["total-count"])
        self.assertEqual(1, resource["data"][0]["id"])