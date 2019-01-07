import pprint
import unittest

from tests.base_server import TestBaseServer
from app import db


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
                    "images": {
                        "data": [
                            {"id": 1, "type": "image"},
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
                    "images": {
                        "data": [
                            {"id": 1, "type": "image"},
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
                    "document": {
                        "data": {
                            "id": 1,
                            "type": "document"
                        }
                    }
                }
            }
        })
        self.assertEqual('201 CREATED', status)

        # WITHOUT IMG-URL
        r, status, resource = self.api_post("images", data={
            "data": {
                "type": "image",
                "attributes": {
                    "manifest-url": "http://burgess.biz/"
                },
                "relationships": {
                    "document": {
                        "data": {
                            "id": 1,
                            "type": "document"
                        }
                    }
                }
            }
        })
        self.assertEqual('403 FORBIDDEN', status)

        # DOCUMENT NOT FOUND
        r, status, resource = self.api_post("images", data={
            "data": {
                "type": "image",
                "attributes": {
                    "manifest-url": "http://burgess.biz/"
                },
                "relationships": {
                    "document": {
                        "data": {
                            "id": 9999,
                            "type": "document"
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

        # WITH DOCUMENT
        r, status, resource = self.api_post("institutions", data={
            "data": {
                "type": "institution",
                "attributes": {
                    "name": "ABC",
                    "ref": "DEF"
                },
                "relationships": {
                    "documents": {
                        "data": [
                            {
                                "id": 1,
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
    
    def test_post_tradition(self):
        r, status, resource = self.api_post("traditions", data={
            "data": {
                "type": "tradition",
                "attributes": {
                    "label": "ABC"
                },
            }
        })
        self.assertEqual('201 CREATED', status)

        # WITH DOCUMENT
        r, status, resource = self.api_post("traditions", data={
            "data": {
                "type": "tradition",
                "attributes": {
                    "label": "ABC",
                    "description": "DEF"
                },
                "relationships": {
                    "documents": {
                        "data": [
                            {
                                "id": 1,
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
        r, status, resource = self.api_post("languages", data={
            "data": {
                "type": "language",
                "attributes": {
                    "content": "NOTE CONTENT",
                }
            }
        })
        self.assertEqual('403 FORBIDDEN', status)
    
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
        r, status, resource = self.api_post("correspondents", data={
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

        r, status, resource = self.api_post("correspondents-having-roles", data={
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

        r, status, resource = self.api_get("documents/11/correspondents-having-roles")
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
        r, status, resource = self.api_post("correspondents-having-roles", data={
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

        r, status, resource = self.api_get("correspondents/9/documents")
        self.assertEqual(2, len(resource["data"]))

