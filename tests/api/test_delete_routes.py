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
        # self.assert200(r)
        self.assertEqual(10, resource["meta"]["total-count"])
        print('Nbr of docs before test : ', resource["meta"]["total-count"])

        self.assertEqual(2, Lock.query.count())
        # print('Nbr of locked docs = ', Lock.query.count())

        # check that you cannot delete documents if you are not logged in
        r, status, resource = self.api_delete("documents/1")
        self.assertEqual('401 UNAUTHORIZED', status)
        # print('Check that you cannot delete documents if you are not logged in', status)

        # check that you cannot delete locked documents
        r, status, resource = self.api_delete("documents/1", auth_username=User.query.first().username)
        self.assertEqual('404 NOT FOUND', status)
        print('Cannot delete a locked doc')

        # check that you can delete documents (no longer locked) if you are logged in
        Lock.query.filter(Lock.object_id == 1).delete()
        db.session.commit()
        r, status, resource = self.api_delete("documents/1", auth_username=User.query.first().username)
        self.assertEqual('204 NO CONTENT', status)
        print('Deleted as admin with user = ', User.query.first().username)

        # check that number of docs is total (10) - 1 = 9
        r, status, resource = self.api_get("documents")
        # self.assert200(r)
        self.assertEqual(9, resource["meta"]["total-count"])
        print('Nbr of docs after delete test : ', resource["meta"]["total-count"])

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
        self.assertEqual(0, Lock.query.filter(Lock.object_id == 1).count())
        self.assertEqual(0, Note.query.filter(Note.document_id == 1).count())
        self.assertEqual(0, Witness.query.filter(Witness.document_id == 1).count())
        self.assertEqual(0, PlacenameHasRole.query.filter(PlacenameHasRole.document_id == 1).count())
        self.assertEqual(0, PersonHasRole.query.filter(PersonHasRole.document_id == 1).count())
        self.assertEqual(0, Changelog.query.filter(Changelog.id == 1).count())

        # Assess the same from the api

        # check witness / images associated with deleted doc are also removed (via api)
        for i in range(1, 16): # count images before deletion instead of hard coding number ?
            r, status, resource = self.api_get("images/"+str(i)+"/witness")
            self.assertEqual(0, resource["meta"]["total-count"])
            # print('Test run with api URL = ', r.request.url)
            # print('Test returned resource = ', resource)

        r, status, resource = self.api_get("locks", auth_username=User.query.first().username)
        self.assertEqual(1, resource["meta"]["total-count"])
        r, status, resource = self.api_get("witnesses?filter[document_id]=1", auth_username=User.query.first().username)
        self.assertEqual(0, resource["meta"]["total-count"])
        #r, status, resource = self.api_get("persons?filter[document_id]=2", auth_username=User.query.first().username)
        #self.assertEqual(3, resource["meta"]["total-count"])

        # check that the object has been removed from the ES index
        # /!\ this test cannot be done with the current dataset because entities are only added to the index
        # when they are created/updated/deleted from the API
        # Indexation tests should be done
