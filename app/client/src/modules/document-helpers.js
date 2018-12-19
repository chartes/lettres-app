const getCorrespondents = function (included) {

    const hasRoleById = {};
    const rolesById = {};
    const correspondentsById = {};
    included.forEach(inc => {
      if (inc.type === 'correspondent') {
        correspondentsById[inc.id] = {...inc.attributes}
      } else if (inc.type === 'correspondent-role') {
        rolesById[inc.id] = {...inc.attributes}
      } else if (inc.type === 'correspondent-has-role') {
        hasRoleById[inc.id] = {
          relationId: inc.id,
          roleId: inc.relationships['correspondent-role'].data.id,
          correspondentId: inc.relationships.correspondent.data.id,
        }
      }
    });
    return Object.values(hasRoleById).map(hasRole => { return {
        ...hasRole, correspondent: correspondentsById[hasRole.correspondentId], role: rolesById[hasRole.roleId]
    }})

  },

  getInstitution = function (included) {
    return getSimpleRelation('institution', included)
  },

  getLanguages = function (included) {
    return  included.filter(item => item.type === 'language').map(lang => { return { id: lang.id, ...lang.attributes }});
  },

  getTradition = function (included) {
    return getSimpleRelation('tradition', included)
  },

  getSimpleRelation = function (propName, included) {
    let found = included.find(item => item.type === propName);
    return { id: found.id, ...found.attributes}
  };




export  {

  getCorrespondents,
  getInstitution,
  getTradition,
  getLanguages,

}

/*

"relationships": {
      "correspondents-having-roles": {
        "links": {
          "self": "http://0.0.0.0:5004/lettres/api/1.0/documents/9/relationships/correspondents-having-roles",
          "related": "http://0.0.0.0:5004/lettres/api/1.0/documents/9/correspondents-having-roles"
        },
        "data": [
          {
            "id": 6,
            "type": "correspondent-has-role"
          },
          {
            "id": 7,
            "type": "correspondent-has-role"
          },
          {
            "id": 8,
            "type": "correspondent-has-role"
          }
        ]
      },
    },

    "included": [
    {
      "type": "correspondent",
      "id": 2,
      "attributes": {
        "firstname": "Christopher",
        "lastname": "Dominguez",
        "key": "Matthew Blackwell",
        "ref": "https://brady.info/tag/wp-content/privacy.html"
      },
      "meta": {},
      "links": {
        "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/2"
      },
      "relationships": {
        "roles-within-documents": {
          "links": {
            "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/2/relationships/roles-within-documents",
            "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/2/roles-within-documents"
          },
          "data": [
            {
              "id": 1,
              "type": "correspondent-has-role"
            },
            {
              "id": 12,
              "type": "correspondent-has-role"
            }
          ]
        },
        "documents": {
          "links": {
            "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/2/relationships/documents",
            "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents/2/documents"
          },
          "data": [
            {
              "id": 2,
              "type": "document"
            },
            {
              "id": 13,
              "type": "document"
            }
          ]
        }
      }
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
      "type": "correspondent-has-role",
      "id": 1,
      "attributes": {},
      "meta": {},
      "links": {
        "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/1"
      },
      "relationships": {
        "correspondent-role": {
          "links": {
            "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/1/relationships/correspondent-role",
            "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/1/correspondent-role"
          },
          "data": {
            "id": 8,
            "type": "correspondent-role"
          }
        },
        "document": {
          "links": {
            "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/1/relationships/document",
            "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/1/document"
          },
          "data": {
            "id": 2,
            "type": "document"
          }
        },
        "correspondent": {
          "links": {
            "self": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/1/relationships/correspondent",
            "related": "http://0.0.0.0:5004/lettres/api/1.0/correspondents-having-roles/1/correspondent"
          },
          "data": {
            "id": 2,
            "type": "correspondent"
          }
        }
      }
    }
  ]
 */