import pprint
import unittest

from app.api.document.facade import DocumentFacade
from tests.base_server import TestBaseServer


@unittest.skip
class TestIndexation(TestBaseServer):

    DOC_INDEX_NAME = "lettres__testing__document"

    def load_fixtures(self):
        from ..data.fixtures.dataset001 import load_fixtures as load_dataset001
        with self.app.app_context():
            from app import db
            load_dataset001(db)
            index_name = DocumentFacade.get_index_name()
            print("Reindexing", index_name)
            self.app.elasticsearch.indices.delete(index=index_name, ignore=[400, 404])  # remove all records

            from app.models import Document
            from app.api.search import SearchIndexManager
            for doc in Document.query.all():
                f_obj = DocumentFacade("", doc)
                for data in f_obj.get_data_to_index_when_added():
                    SearchIndexManager.add_to_index(index=index_name, id=doc.id, payload=data)

    def reindex_document(self, id):
        from app.api.search import SearchIndexManager
        f_obj, errors, kwargs = DocumentFacade.get_resource_facade("", id)
        index_name = DocumentFacade.get_index_name()
        for data in f_obj.get_data_to_index_when_added():
            SearchIndexManager.add_to_index(index=index_name, id=id, payload=data)

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
        self.reindex_document(1)

        r, status, resource = self.api_get("documents/1")
        self.assert200(r)
        self.assertEqual("Document TestIndexation", resource["data"]["attributes"]["title"])

        resource = self.search(DocumentFacade.get_index_name(), "TestIndexation")
        pprint.pprint(resource)
        self.assertEqual(1, resource["meta"]["total-count"])
        self.assertEqual(1, resource["data"][0]["id"])

    @unittest.skip
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

        self.assertEqual(1, resource["meta"]["total-count"])
        self.assertEqual(1, resource["data"][0]["id"])
