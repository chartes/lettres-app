import pprint
import unittest

from app.models import TRADITION_VALUES, WITNESS_STATUS_VALUES
from tests.base_server import TestBaseServer
from app import db


@unittest.skip
class TestPostRoutes(TestBaseServer):

    def load_fixtures(self):
        from ..data.fixtures.dataset001 import load_fixtures as load_dataset001
        with self.app.app_context():
            load_dataset001(db)

    def test_post_document(self):
        r, status, resource = self.api_post("documents", data={
            "data": {
                "type": "document",
                "attributes": {
                    "title": "New Doc",
                    "transcription": "Lorem Ipsum"
                },
                "relationships": {
                    "witnesses": {
                        "data": [
                            {"id": 1, "type": "witness"},
                        ]
                    },
                    "languages": {
                        "data": [
                            {"id": 1, "type": "language"},
                        ]
                    },
                    "collections": {
                        "data": [
                            {"id": 1, "type": "collection"},
                            {"id": 2, "type": "collection"},
                        ]
                    },
                    "owner": {
                        "data": {"id": 2, "type": "user"}
                    }
                }
            }
        })
        self.assertEqual('201 CREATED', status)

        r, status, resource = self.api_get("documents")
        self.assert200(r)
        self.assertEqual(11, resource["meta"]["total-count"])

        # ID ALREADY EXISTS
        r, status, resource = self.api_post("documents", data={
            "data": {
                "id": 1,
                "type": "document",
                "attributes": {
                    "title": "New Doc"
                },
                "relationships": {
                    "witnesses": {
                        "data": [
                            {"id": 1, "type": "witness"},
                        ]
                    },
                    "institution": {
                        "data": {"id": 3, "type": "institution"}
                    },
                    "owner": {
                        "data": {"id": 1, "type": "user"}
                    }
                }
            }
        })
        self.assertEqual('409 CONFLICT', status)
        
        # NO OWNER
        r, status, resource = self.api_post("documents", data={
            "data": {
                "type": "document",
                "attributes": {
                    "title": "New Doc"
                },
                "relationships": {
                    "witnesses": {
                        "data": [
                            {"id": 1, "type": "witness"},
                        ]
                    },
                    "institution": {
                        "data": {"id": 3, "type": "institution"}
                    }
                }
            }
        })
        self.assertEqual('403 FORBIDDEN', status)

    def test_post_image(self):
        r, status, resource = self.api_post("images", data={
            "data": {
                "type": "image",
                "attributes": {
                    "canvas-idx": 1,
                    "manifest-url": "http://burgess.biz/"
                },
                "relationships": {
                    "witness": {
                        "data": {
                            "id": 1,
                            "type": "witness"
                        }
                    }
                }
            }
        })
        self.assertEqual('201 CREATED', status)

        # WITHOUT CANVAS-IDX
        r, status, resource = self.api_post("images", data={
            "data": {
                "type": "image",
                "attributes": {
                    "manifest-url": "http://burgess.biz/"
                },
                "relationships": {
                    "witness": {
                        "data": {
                            "id": 1,
                            "type": "witness"
                        }
                    }
                }
            }
        })
        self.assertEqual('403 FORBIDDEN', status)

        # WITNESS NOT FOUND
        r, status, resource = self.api_post("images", data={
            "data": {
                "type": "image",
                "attributes": {
                    "manifest-url": "http://burgess.biz/"
                },
                "relationships": {
                    "witness": {
                        "data": {
                            "id": 9999,
                            "type": "witness"
                        }
                    }
                }
            }
        })
        self.assertEqual('404 NOT FOUND', status)

    def test_post_institution(self):
        r, status, resource = self.api_post("institutions", data={
            "data": {
                "type": "institution",
                "attributes": {
                    "name": "ABC"
                },
            }
        })
        self.assertEqual('201 CREATED', status)

        # WITH WITNESS
        r, status, resource = self.api_post("institutions", data={
            "data": {
                "type": "institution",
                "attributes": {
                    "name": "ABC",
                    "ref": "DEF"
                },
                "relationships": {
                    "witnesses": {
                        "data": [
                            {
                                "id": 1,
                                "type": "witness"
                            },
                            {
                                "id": 2,
                                "type": "witness"
                            }
                        ]
                    }
                }
            }
        })
        self.assertEqual('201 CREATED', status)

    def test_post_language(self):
        r, status, resource = self.api_post("languages", data={
            "data": {
                "type": "language",
                "attributes": {
                    "code": "ABC"
                },
            }
        })
        self.assertEqual('201 CREATED', status)

        # WITH DOCUMENT
        r, status, resource = self.api_post("languages", data={
            "data": {
                "type": "language",
                "attributes": {
                    "label": "ABC",
                    "code": "ETESTSTTST"
                },
                "relationships": {
                    "documents": {
                        "data": [
                            {
                                "id": 3,
                                "type": "document"
                            },
                            {
                                "id": 2,
                                "type": "document"
                            }
                        ]
                    }
                }
            }
        })
        self.assertEqual('201 CREATED', status)
    
    def test_post_note(self):
        r, status, resource = self.api_post("notes", data={
            "data": {
                "type": "note",
                "attributes": {
                    "content": "NOTE CONTENT",
                    "label": "Note nb1"
                },
                "relationships": {
                    "document": {
                        "data":
                            {
                                "id": 1,
                                "type": "document"
                            }
                    }
                }
            }
        })
        self.assertEqual('201 CREATED', status)

        # WITHOUT DOCUMENT
        r, status, resource = self.api_post("notes", data={
            "data": {
                "type": "note",
                "attributes": {
                    "content": "NOTE CONTENT",
                }
            }
        })
        self.assertEqual('403 FORBIDDEN', status)

    def test_post_witness(self):
        r, status, resource = self.api_post("witnesses", data={
            "data": {
                "type": "witness",
                "attributes": {
                    "content": "NOTE CONTENT",
                    "classification-mark": "CLASS MARK",
                    "tradition": TRADITION_VALUES[0],
                    "status": WITNESS_STATUS_VALUES[0]
                },
                "relationships": {
                    "document": {
                        "data":
                            {
                                "id": 1,
                                "type": "document"
                            }
                    },
                    "institution": {
                        "data":
                            {
                                "id": 2,
                                "type": "institution"
                            }
                    },
                    "images": {
                        "data": [
                            {
                                "id": 1,
                                "type": "image"
                            },
                            {
                                "id": 2,
                                "type": "image"
                            },
                        ]
                    }
                }
            }
        })
        self.assertEqual('201 CREATED', status)

    def test_post_whitelist(self):
        r, status, resource = self.api_post("whitelists", data={
            "data": {
                "type": "whitelist",
                "attributes": {
                    "label": "new_whitelist"
                },
            }
        })
        self.assertEqual('201 CREATED', status)

        # WITH USERS
        r, status, resource = self.api_post("whitelists", data={
            "data": {
                "type": "whitelist",
                "attributes": {
                    "label": "new_whitelist",
                },
                "relationships": {
                    "users": {
                        "data": [
                            {
                                "id": 1,
                                "type": "user"
                            },
                            {
                                "id": 2,
                                "type": "user"
                            }
                        ]
                    }
                }
            }
        })
        self.assertEqual('201 CREATED', status)

        # WITH USERS
        r, status, resource = self.api_post("whitelists", data={
            "data": {
                "type": "whitelist",
                "attributes": {
                    "label": "new_whitelist",
                },
                "relationships": {
                    "users": {
                        "data": [
                            {
                                "id": 1,
                                "type": "user"
                            },
                            {
                                "id": 3,
                                "type": "user"
                            }
                        ]
                    }
                }
            }
        })
        self.assertEqual('201 CREATED', status)
    
    def test_post_correspondent_role(self):
        r, status, resource = self.api_post("correspondent-roles", data={
            "data": {
                "type": "correspondent-role",
                "attributes": {
                    "label": "lbl",
                    "description": "desc",
                }
            }
        })
        self.assertEqual('201 CREATED', status)
    
    def test_post_correspondent(self):
        r, status, resource = self.api_post("persons", data={
            "data": {
                "type": "correspondent",
                "attributes": {
                    "firstname": "CorrespondentFirstname",
                    "lastname": "CorrespondentLastname",
                    "key": "CorrespondentKey",
                    "ref": "CorrespondentRef",
                }
            }
        })
        self.assertEqual('201 CREATED', status)

        r, status, resource = self.api_post("documents", data={
            "data": {
                "type": "document",
                "attributes": {
                    "title": "New Doc"
                },
                "relationships": {
                    "witnesses": {
                        "data": [
                            {"id": 1, "type": "witness"},
                        ]
                    },
                    "institution": {
                        "data": {"id": 1, "type": "institution"}
                    },
                    "owner": {
                        "data": {"id": 1, "type": "user"}
                    }
                }
            }
        })
        self.assertEqual('201 CREATED', status)

        r, status, resource = self.api_post("persons-having-roles", data={
            "data": {
                "type": "correspondent-has-role",
                "relationships": {
                    "document": {
                        "data": {"type": "document", "id": 11}
                    },
                    "correspondent-role": {
                        "data": {"type": "correspondent-role", "id": 1}
                    },
                    "correspondent": {
                        "data": {"type": "correspondent", "id": 9}
                    }
                }
            }
        })
        self.assertEqual('201 CREATED', status)

        r, status, resource = self.api_get("documents/11/persons-having-roles")
        self.assertEqual(1, len(resource["data"]))

        # ADD A DOCUMENT TO THIS CORRESPONDENT
        r, status, resource = self.api_post("documents", data={
            "data": {
                "type": "document",
                "attributes": {
                    "title": "New Doc"
                },
                "relationships": {
                    "images": {
                        "data": [
                            {"id": 1, "type": "image"},
                        ]
                    },
                    "institution": {
                        "data": {"id": 3, "type": "institution"}
                    },
                    "owner": {
                        "data": {"id": 2, "type": "user"}
                    }
                }
            }
        })
        self.assertEqual('201 CREATED', status)
        r, status, resource = self.api_post("persons-having-roles", data={
            "data": {
                "type": "correspondent-has-role",
                "relationships": {
                    "document": {
                        "data": {"type": "document", "id": 12}
                    },
                    "correspondent-role": {
                        "data": {"type": "correspondent-role", "id": 1}
                    },
                    "correspondent": {
                        "data": {"type": "correspondent", "id": 9}
                    }
                }
            }
        })
        self.assertEqual('201 CREATED', status)

        r, status, resource = self.api_get("persons/9/documents")
        self.assertEqual(2, len(resource["data"]))
