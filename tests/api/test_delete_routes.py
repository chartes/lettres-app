import pprint
import unittest

from app.models import *
from tests.base_server import TestBaseServer
from app import db


class TestDeleteRoutes(TestBaseServer):

    def load_fixtures(self):
        from tests.data.fixtures.dataset001 import load_fixtures as load_dataset001
        with self.app.app_context():
            load_dataset001(db)

    def test_delete_document(self):
        r, status, resource = self.api_get("documents")
        self.assert200(r)
        self.assertEqual(10, resource["meta"]["total-count"])
        # print('Nbr of docs before test : ', resource["meta"]["total-count"])

        # check that you cannot delete documents if you are not logged in
        r, status, resource = self.api_delete("documents/1")
        self.assertEqual('401 UNAUTHORIZED', status)
        # print('Check that you cannot delete documents if you are not logged in', status)

        r, status, resource = self.api_delete("documents/1", auth_username=User.query.first().username)
        self.assertEqual('204 NO CONTENT', status)
        # print('Deletion test as admin run with user = ', User.query.first().username)

        # check that number of docs is total (10) - 1 = 9
        r, status, resource = self.api_get("documents")
        self.assert200(r)
        self.assertEqual(9, resource["meta"]["total-count"])
        # print('Deletion test as admin run with GET status = ', status)

        # check that cascade deletions are correct
        document_has_collection = Document.query.with_entities(Document.id).join(association_document_has_collection).join(Collection)
        # print('check ', document_has_collection.filter(association_document_has_collection.c.document_id == 1).count())
        self.assertEqual(0, document_has_collection.filter(association_document_has_collection.c.document_id == 1).count())
        document_has_language = Document.query.with_entities(Document.id).join(
            association_document_has_language).join(Language)
        self.assertEqual(0,
                         document_has_language.filter(association_document_has_language.c.document_id == 1).count())
        user_has_bookmark = Document.query.with_entities(Document.id).join(
            association_user_has_bookmark)
        self.assertEqual(0,
                         user_has_bookmark.filter(association_user_has_bookmark.c.doc_id == 1).count())
        self.assertEqual(0, Lock.query.filter(Lock.id == 1).count())
        self.assertEqual(0, Note.query.filter(Note.document_id == 1).count())
        self.assertEqual(0, Witness.query.filter(Witness.document_id == 1).count())
        self.assertEqual(0, PlacenameHasRole.query.filter(PlacenameHasRole.document_id == 1).count())
        self.assertEqual(0, PersonHasRole.query.filter(PersonHasRole.document_id == 1).count())
        self.assertEqual(0, Changelog.query.filter(Changelog.id == 1).count())

        # check witness / images associated with deleted doc are also removed (via api)
        for i in range(1, 16): # count images before deletion instead of hard coding number ?
            r, status, resource = self.api_get("images/"+str(i)+"/witness")
            self.assertEqual(0, resource["meta"]["total-count"])
            # print(r.request.url)
            # print(resource)


        # check that the object has been removed from the ES index
        # /!\ this test cannot be done with the current dataset because entities are only added to the index
        # when they are created/updated/deleted from the API
        # Indexation tests should be done
