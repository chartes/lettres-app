import {getCorrespondents, getInstitution, getLanguages, getTradition} from '../document-helpers'

const includedIn = [
  {
    "type": "correspondent",
    "id": 10,
    "attributes": {
      "firstname": "Diane",
      "lastname": "Smith",
      "key": "Angel Edwards",
      "ref": "http://rodriguez.com/app/index.jsp"
    },
    "meta": {},
    "links": {
      "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/10"
    },
    "relationships": {
      "roles-within-documents": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/10/relationships/roles-within-documents",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/10/roles-within-documents"
        },
        "data": [
          {
            "id": 6,
            "type": "correspondent-has-role"
          }
        ]
      },
      "documents": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/10/relationships/documents",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/10/documents"
        },
        "data": [
          {
            "id": 9,
            "type": "document"
          }
        ]
      }
    }
  },
  {
    "type": "correspondent",
    "id": 5,
    "attributes": {
      "firstname": "Carlos",
      "lastname": "Watson",
      "key": "Amanda Francis",
      "ref": "http://www.mclaughlin.com/wp-content/home/"
    },
    "meta": {},
    "links": {
      "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/5"
    },
    "relationships": {
      "roles-within-documents": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/5/relationships/roles-within-documents",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/5/roles-within-documents"
        },
        "data": [
          {
            "id": 7,
            "type": "correspondent-has-role"
          },
          {
            "id": 9,
            "type": "correspondent-has-role"
          },
          {
            "id": 14,
            "type": "correspondent-has-role"
          },
          {
            "id": 20,
            "type": "correspondent-has-role"
          }
        ]
      },
      "documents": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/5/relationships/documents",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/5/documents"
        },
        "data": [
          {
            "id": 9,
            "type": "document"
          },
          {
            "id": 11,
            "type": "document"
          },
          {
            "id": 13,
            "type": "document"
          },
          {
            "id": 20,
            "type": "document"
          }
        ]
      }
    }
  },
  {
    "type": "correspondent",
    "id": 4,
    "attributes": {
      "firstname": "James",
      "lastname": "Taylor",
      "key": "Erin Carter",
      "ref": null
    },
    "meta": {},
    "links": {
      "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/4"
    },
    "relationships": {
      "roles-within-documents": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/4/relationships/roles-within-documents",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/4/roles-within-documents"
        },
        "data": [
          {
            "id": 8,
            "type": "correspondent-has-role"
          }
        ]
      },
      "documents": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/4/relationships/documents",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/4/documents"
        },
        "data": [
          {
            "id": 9,
            "type": "document"
          }
        ]
      }
    }
  },
  {
    "type": "correspondent-role",
    "id": 12,
    "attributes": {
      "id": 12,
      "label": "add",
      "description": null
    },
    "meta": {},
    "links": {
      "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondent-roles/12"
    },
    "relationships": {}
  },
  {
    "type": "correspondent-role",
    "id": 8,
    "attributes": {
      "id": 8,
      "label": "democratic",
      "description": null
    },
    "meta": {},
    "links": {
      "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondent-roles/8"
    },
    "relationships": {}
  },
  {
    "type": "correspondent-role",
    "id": 9,
    "attributes": {
      "id": 9,
      "label": "mention",
      "description": null
    },
    "meta": {},
    "links": {
      "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondent-roles/9"
    },
    "relationships": {}
  },
  {
    "type": "correspondent-has-role",
    "id": 6,
    "attributes": {},
    "meta": {},
    "links": {
      "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/6"
    },
    "relationships": {
      "correspondent-role": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/6/relationships/correspondent-role",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/6/correspondent-role"
        },
        "data": {
          "id": 12,
          "type": "correspondent-role"
        }
      },
      "document": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/6/relationships/document",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/6/document"
        },
        "data": {
          "id": 9,
          "type": "document"
        }
      },
      "correspondent": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/6/relationships/correspondent",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/6/correspondent"
        },
        "data": {
          "id": 10,
          "type": "correspondent"
        }
      }
    }
  },
  {
    "type": "correspondent-has-role",
    "id": 7,
    "attributes": {},
    "meta": {},
    "links": {
      "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/7"
    },
    "relationships": {
      "correspondent-role": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/7/relationships/correspondent-role",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/7/correspondent-role"
        },
        "data": {
          "id": 8,
          "type": "correspondent-role"
        }
      },
      "document": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/7/relationships/document",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/7/document"
        },
        "data": {
          "id": 9,
          "type": "document"
        }
      },
      "correspondent": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/7/relationships/correspondent",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/7/correspondent"
        },
        "data": {
          "id": 5,
          "type": "correspondent"
        }
      }
    }
  },
  {
    "type": "correspondent-has-role",
    "id": 8,
    "attributes": {},
    "meta": {},
    "links": {
      "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/8"
    },
    "relationships": {
      "correspondent-role": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/8/relationships/correspondent-role",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/8/correspondent-role"
        },
        "data": {
          "id": 9,
          "type": "correspondent-role"
        }
      },
      "document": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/8/relationships/document",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/8/document"
        },
        "data": {
          "id": 9,
          "type": "document"
        }
      },
      "correspondent": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/8/relationships/correspondent",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/8/correspondent"
        },
        "data": {
          "id": 4,
          "type": "correspondent"
        }
      }
    }
  }
]

const resultOk = [
  {
    relationId: 6,
    roleId: 12,
    correspondentId: 10,
    correspondent: {
      "firstname": "Diane",
      "lastname": "Smith",
      "key": "Angel Edwards",
      "ref": "http://rodriguez.com/app/index.jsp"
    },
    role: {
      "id": 12,
      "label": "add",
      "description": null
    }
  },
  {
    relationId: 7,
    roleId: 8,
    correspondentId: 5,
    correspondent: {
      "firstname": "Carlos",
      "lastname": "Watson",
      "key": "Amanda Francis",
      "ref": "http://www.mclaughlin.com/wp-content/home/"
    },
    role: {
      "id": 8,
      "label": "democratic",
      "description": null
    }
  },
  {
    relationId: 8,
    roleId: 9,
    correspondentId: 4,
    correspondent: {
      "firstname": "James",
      "lastname": "Taylor",
      "key": "Erin Carter",
      "ref": null
    },
    role: {
      "id": 9,
      "label": "mention",
      "description": null
    },
  }
]

describe('Correspondents helpers', () => {

  test('getCorrespondents', () => {
    expect(getCorrespondents(includedIn)).toEqual(resultOk)
  })

  test('getInstitution', () => {

    const incIn = [
      {
        "type": "institution",
        "id": 11,
        "attributes": {
          "name": "Marriage parent share.",
          "ref": "https://kelley.biz/posts/wp-content/author.html"
        },
        "meta": {},
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/institutions/11"
        },
        "relationships": {
          "documents": {
            "links": {
              "self": "http://0.0.0.0:5004/lettres/api/1.0/institutions/11/relationships/documents",
              "related": "http://0.0.0.0:5004/lettres/api/1.0/institutions/11/documents"
            },
            "data": [
              {
                "id": 9,
                "type": "document"
              }
            ]
          }
        }
      }
    ]

    expect(getInstitution(incIn)).toEqual({ "id": 11, "name": "Marriage parent share.", "ref": "https://kelley.biz/posts/wp-content/author.html" })
  })

  test('getTradition', () => {

    const incIn = [
      {
        "type": "tradition",
        "id": 1,
        "attributes": {
          "label": "south",
          "description": "Pm interview everything sound."
        },
        "meta": {},
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/traditions/1"
        },
        "relationships": {
          "documents": {
            "links": {
              "self": "http://0.0.0.0:5004/lettres/api/1.0/traditions/1/relationships/documents",
              "related": "http://0.0.0.0:5004/lettres/api/1.0/traditions/1/documents"
            },
            "data": [
              {
                "id": 9,
                "type": "document"
              }
            ]
          }
        }
      }
    ]

    expect(getTradition(incIn)).toEqual({ "id": 1, "label": "south", "description": "Pm interview everything sound." })
  })

  test('getLanguages', () => {

    const incIn = [
      {
        "type": "language",
        "id": 4,
        "attributes": {
          "code": "CZC",
          "label": null
        },
        "meta": {},
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/languages/4"
        },
        "relationships": {
          "documents": {
            "links": {
              "self": "http://0.0.0.0:5004/lettres/api/1.0/languages/4/relationships/documents",
              "related": "http://0.0.0.0:5004/lettres/api/1.0/languages/4/documents"
            },
            "data": [
              {
                "id": 2,
                "type": "document"
              },
              {
                "id": 9,
                "type": "document"
              },
              {
                "id": 17,
                "type": "document"
              },
              {
                "id": 18,
                "type": "document"
              },
              {
                "id": 1,
                "type": "document"
              }
            ]
          }
        }
      },
      {
        "type": "language",
        "id": 5,
        "attributes": {
          "code": "ITA",
          "label": null
        },
        "meta": {},
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/languages/5"
        },
        "relationships": {
          "documents": {
            "links": {
              "self": "http://0.0.0.0:5004/lettres/api/1.0/languages/5/relationships/documents",
              "related": "http://0.0.0.0:5004/lettres/api/1.0/languages/5/documents"
            },
            "data": [
              {
                "id": 1,
                "type": "document"
              },
              {
                "id": 3,
                "type": "document"
              },
              {
                "id": 6,
                "type": "document"
              },
              {
                "id": 10,
                "type": "document"
              },
              {
                "id": 11,
                "type": "document"
              },
              {
                "id": 13,
                "type": "document"
              },
              {
                "id": 14,
                "type": "document"
              },
              {
                "id": 16,
                "type": "document"
              }
            ]
          }
        }
      }
    ], ok = [
      {"id": 4, "code": "CZC", "label": null },
      {"id": 5, "code": "ITA", "label": null }
    ]

    expect(getLanguages(incIn)).toEqual(ok)
  })

})
