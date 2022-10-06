import pprint
import unittest

from tests.base_server import TestBaseServer
from app import db


class TestGetRoutes(TestBaseServer):

    def load_fixtures(self):
        from tests.data.fixtures.dataset001 import load_fixtures as load_dataset001
        with self.app.app_context():
            load_dataset001(db)

    def test_documents(self):
        r, status, resource = self.api_get("documents")
        self.assert200(r)
        self.assertEqual(10, resource["meta"]["total-count"])

    def test_documents_relationships(self):

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

        # ------ persons -------
        r, status, resource = self.api_get("documents/1/persons")
        self.assertEqual(3, resource["meta"]["total-count"])
        self.assertEqual("correspondent", set([d["type"] for d in resource["data"]]).pop())
        r, status, resource = self.api_get("documents/1/relationships/persons")
        self.assertEqual(3, resource["meta"]["total-count"])
        self.assertEqual("correspondent", set([d["type"] for d in resource["data"]]).pop())

        # ------ persons-having-roles -------
        r, status, resource = self.api_get("documents/1/persons-having-roles")
        self.assertEqual(3, resource["meta"]["total-count"])
        self.assertEqual("correspondent-has-role", set([d["type"] for d in resource["data"]]).pop())
        r, status, resource = self.api_get("documents/1/relationships/persons-having-roles")
        self.assertEqual(3, resource["meta"]["total-count"])
        self.assertEqual("correspondent-has-role", set([d["type"] for d in resource["data"]]).pop())

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

        # ------ witnesses -------
        r, status, resource = self.api_get("documents/1/relationships/witnesses")
        self.assertEqual(3, resource["meta"]["total-count"])

    def test_pagination(self):
        self._test_pagination_links("documents")
        self._test_pagination_links("documents/1")
        self._test_pagination_links("documents?page[size]=5")
        self._test_pagination_links("documents?page[size]=5&page[number]=2")
        self._test_pagination_links("documents?page[size]=10&page[number]=1")
        self._test_pagination_links("documents?page[number]=2")

        self._test_pagination_links("documents/10/witnesses")
        self._test_pagination_links("documents/10/witnesses?page[size]=2")
        self._test_pagination_links("documents/10/witnesses?page[size]=2&page[number]=2")
        self._test_pagination_links("documents/10/witnesses?page[size]=2&page[number]=1")
        self._test_pagination_links("documents/10/witnesses?page[number]=2")
