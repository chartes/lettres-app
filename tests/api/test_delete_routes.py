import pprint
import unittest

from app.models import TRADITION_VALUES, WITNESS_STATUS_VALUES, User
from tests.base_server import TestBaseServer
from app import db


class TestDeleteRoutes(TestBaseServer):

    def load_fixtures(self):
        from tests.data.fixtures.dataset001 import load_fixtures as load_dataset001
        with self.app.app_context():
            load_dataset001(db)

    def test_delete_document(self):
        # check that you cannot delete documents if you are not logged in
        r, status, resource = self.api_delete("documents/1")
        self.assertEqual('401 UNAUTHORIZED', status)

        r, status, resource = self.api_delete("documents/1", auth_username=User.query.first().username)
        self.assertEqual('204 NO CONTENT', status)
        # check that cascade deletions are correct

        # check that the object has been removed from the ES index
        # /!\ this test cannot be done with the current dataset because entities are only added to the index
        # when they are created/updated/deleted from the API
        # Indexation tests should be done
