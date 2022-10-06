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
        r, status, resource = self.api_delete("documents/1", auth_username=User.query.first().username)
        self.assertEqual('204 NO CONTENT', status)
        # check that cascade deletions are correct

        # check that the object has been removed from the ES index

