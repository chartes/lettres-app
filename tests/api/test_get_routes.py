import pprint
import unittest

from app.models import Document
from tests.base_server import TestBaseServer
from app import db


class TestGetRoutes(TestBaseServer):

    def load_fixtures(self):
        from ..data.fixtures.dataset001 import load_fixtures as load_dataset001
        with self.app.app_context():
            load_dataset001(db)

        pprint.pprint(Document.query.all())

    def test_documents(self):
        r, status, resource = self.api_get("documents")
        self.assert200(r)
        self.assertEqual(10, resource["meta"]["total-count"])

        r, status, resource = self.api_get("documents/1")
        pass

    def test_documents_relationships(self):
        # ------ images -------
        r, status, resource = self.api_get("documents/1/images")
        self.assertEqual(10, resource["meta"]["total-count"])
        self.assertEqual("image", set([d["type"] for d in resource["data"]]).pop())
        r, status, resource = self.api_get("documents/1/relationships/images")
        self.assertEqual(10, resource["meta"]["total-count"])
        self.assertEqual("image", set([d["type"] for d in resource["data"]]).pop())

        # ------ notes -------
        r, status, resource = self.api_get("documents/1/notes")
        self.assertEqual(50, resource["meta"]["total-count"])
        self.assertEqual("note", set([d["type"] for d in resource["data"]]).pop())
        r, status, resource = self.api_get("documents/1/relationships/notes")
        self.assertEqual(50, resource["meta"]["total-count"])
        self.assertEqual("note", set([d["type"] for d in resource["data"]]).pop())

        # ------ languages -------
        r, status, resource = self.api_get("documents/1/languages")
        self.assertEqual(2, resource["meta"]["total-count"])
        self.assertEqual("language", set([d["type"] for d in resource["data"]]).pop())
        r, status, resource = self.api_get("documents/1/relationships/languages")
        self.assertEqual(2, resource["meta"]["total-count"])
        self.assertEqual("language", set([d["type"] for d in resource["data"]]).pop())

        # ------ correspondents -------
        r, status, resource = self.api_get("documents/1/correspondents")
        self.assertEqual(3, resource["meta"]["total-count"])
        self.assertEqual("correspondent", set([d["type"] for d in resource["data"]]).pop())
        r, status, resource = self.api_get("documents/1/relationships/correspondents")
        self.assertEqual(3, resource["meta"]["total-count"])
        self.assertEqual("correspondent", set([d["type"] for d in resource["data"]]).pop())

        # ------ correspondents-having-roles -------
        r, status, resource = self.api_get("documents/1/correspondents-having-roles")
        self.assertEqual(3, resource["meta"]["total-count"])
        self.assertEqual("correspondent-has-role", set([d["type"] for d in resource["data"]]).pop())
        r, status, resource = self.api_get("documents/1/relationships/correspondents-having-roles")
        self.assertEqual(3, resource["meta"]["total-count"])
        self.assertEqual("correspondent-has-role", set([d["type"] for d in resource["data"]]).pop())

        # ------ institution -------
        r, status, resource = self.api_get("documents/1/institution")
        self.assertEqual(1, resource["data"]["id"])
        self.assertEqual("institution", resource["data"]["type"])
        r, status, resource = self.api_get("documents/1/relationships/institution")
        self.assertEqual(1, resource["data"]["id"])
        self.assertEqual("institution", resource["data"]["type"])

        # ------ tradition -------
        r, status, resource = self.api_get("documents/1/tradition")
        self.assertEqual(1, resource["data"]["id"])
        self.assertEqual("tradition", resource["data"]["type"])
        r, status, resource = self.api_get("documents/1/relationships/tradition")
        self.assertEqual(1, resource["data"]["id"])
        self.assertEqual("tradition", resource["data"]["type"])

        # ------ whitelist -------
        r, status, resource = self.api_get("documents/1/whitelist")
        self.assertEqual(1, resource["data"]["id"])
        self.assertEqual("whitelist", resource["data"]["type"])
        r, status, resource = self.api_get("documents/1/relationships/whitelist")
        self.assertEqual(1, resource["data"]["id"])
        self.assertEqual("whitelist", resource["data"]["type"])

        # ------ owner -------
        r, status, resource = self.api_get("documents/1/owner")
        self.assertEqual(1, resource["data"]["id"])
        self.assertEqual("user", resource["data"]["type"])
        r, status, resource = self.api_get("documents/1/relationships/owner")
        self.assertEqual(1, resource["data"]["id"])
        self.assertEqual("user", resource["data"]["type"])

    def test_pagination(self):
        self._test_pagination_links("documents")
        self._test_pagination_links("documents/1")
        self._test_pagination_links("documents?page[size]=5")
        self._test_pagination_links("documents?page[size]=5&page[number]=2")
        self._test_pagination_links("documents?page[size]=10&page[number]=1")
        self._test_pagination_links("documents?page[number]=2")

        self._test_pagination_links("documents/10/images")
        self._test_pagination_links("documents/10/images?page[size]=2")
        self._test_pagination_links("documents/10/images?page[size]=2&page[number]=2")
        self._test_pagination_links("documents/10/images?page[size]=2&page[number]=1")
        self._test_pagination_links("documents/10/images?page[number]=2")