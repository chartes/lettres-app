# API Lettres
---

L'API Lettres implémente en grande partie la spécification [**json:api 1.0**](https://jsonapi.org)

Les collections de ressources sont nativement paginées et il est possible de contrôler
cette fonctionnalité via les paramètres ```page[size]=25``` et ```page[number]=2```

## Document

### **Récupération** d'un document

Il y a trois possibilités qui différent en terme de performance et de quantité d'information à propos des relations entre le document et ses ressources liées (images, langages, propriétaire, etc).

Avec toutes les informations (liens des relations + ```id``` des ressources liées) :
```json
curl -X GET \
  http://localhost:5004/lettres/api/1.0/documents/3 \
  -H 'Accept: application/vnd.api+json' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'cache-control: no-cache'
```

Avec uniquement les liens des relations (mais pas les ```id``` des ressources liées) :
```json
curl -X GET \
  'http://localhost:5004/lettres/api/1.0/documents/3?with-relationships=links' \
  -H 'Accept: application/vnd.api+json' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'cache-control: no-cache'
```
Sans les relations :
```json
curl -X GET \
  'http://localhost:5004/lettres/api/1.0/documents/3?without-relationships' \
  -H 'Accept: application/vnd.api+json' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'cache-control: no-cache'
```

### **Création** d'un document

| Champ| Type | Obligatoire| Description
|------|------|------------| ---------|
|id | Integer |Non | |
|title | String | **Oui** | texte riche |
|witness-label | String | Non |  texte riche |
|classification-mark | String | Non | texte riche |
|argument | Text | Non |  texte riche |
|creation | Date | Non | |
|creation-label | String| Non |  texte riche |
|location-date-label | String | Non |  texte riche |
|location-date-ref | String | Non | |
|transcription | Text | Non |  texte riche |
|date-insert | Date  | Non | |
|date-update | Date | Non | |
|is-published | Boolean | Non | | |

Ainsi que les relations suivantes :

| Relation  | Type | Arité | Obligatoire| Méthodes| Description |
|------|------|-------|------------|---------|---------|
|images | image | liste | Non |  GET,POST,PATCH | |
|notes | note | liste | Non | GET,POST,PATCH | |
|languages | language | liste | Non | GET,POST,PATCH | |
|owner | user | un seul | **Oui** | GET,POST,PATCH | |
|institution | institution | un seul | Non | GET,POST,PATCH | |
|tradition| tradition | un seul | Non | GET,POST,PATCH | |
|whitelist| whitelist | un seul | Non | GET,POST,PATCH | |
|prev-document | document | un seul | Non | GET,POST,PATCH | |
|next-document | document | un seul | Non | GET,POST,PATCH | |
|correspondents-having-roles| correspondent-has-role| liste | Non | GET,POST,PATCH | Liste des objets Document <-> Person <-> PersonRole |
|roles| correspondent-role| liste | Non | GET | Liste des roles des correspondants du document |
|correspondents| correspondent| liste | Non | GET | Liste des correspondants du document  |

**Exemple de création :**

**NB :** les ressources liées (images, owner, institution) existent au préalable.
```json
curl -X POST \
  http://localhost:5004/lettres/api/1.0/documents \
  -H 'Accept: application/vnd.api+json' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
  "data": {
    "type": "document",
    "attributes": {
      "title": "New Doc"
    },
    "relationships": {
    	"images" : {
    		"data" : [
	    		{"id": 10, "type": "image"},
	    		{"id": 11, "type": "image"}
    		]
    	},
    	"institution" : {
    		"data" :{"id": 3, "type": "institution"}
    	},
    	"owner" : {
    		"data" :{"id": 2, "type": "user"}
    	}
	}
  }
}'
```
**Réponse ```201 CREATED```** :
```json
{
    "data": {
        "type": "document",
        "id": 25,
        "attributes": {
            "title": "New Doc",
            "witness-label": null,
            "classification-mark": null,
            "argument": null,
            "creation": null,
            "creation-label": null,
            "location-date-label": null,
            "location-date-ref": null,
            "transcription": null,
            "date-insert": null,
            "date-update": null,
            "is-published": null
        },
        "meta": {},
        "links": {
            "self": "http://localhost:5004/lettres/api/1.0/documents/25"
        },
        "relationships": {
            "correspondents-having-roles": {
                "links": {
                    "self": persons,
                    "related": persons
                },
                "data": []
            },
            "roles": {
                "links": {
                    "self": "http://localhost:5004/lettres/api/1.0/documents/25/relationships/roles",
                    "related": "http://localhost:5004/lettres/api/1.0/documents/25/roles"
                },
                "data": []
            },
            "correspondents": {
                "links": {
                    "self": persons,
                    "related": persons
                },
                "data": []
            },
            "images": {
                "links": {
                    "self": "http://localhost:5004/lettres/api/1.0/documents/25/relationships/images",
                    "related": "http://localhost:5004/lettres/api/1.0/documents/25/images"
                },
                "data": [
                    {
                        "id": 10,
                        "type": "image"
                    },
                    {
                        "id": 11,
                        "type": "image"
                    }
                ]
            },
            "notes": {
                "links": {
                    "self": "http://localhost:5004/lettres/api/1.0/documents/25/relationships/notes",
                    "related": "http://localhost:5004/lettres/api/1.0/documents/25/notes"
                },
                "data": []
            },
            "languages": {
                "links": {
                    "self": "http://localhost:5004/lettres/api/1.0/documents/25/relationships/languages",
                    "related": "http://localhost:5004/lettres/api/1.0/documents/25/languages"
                },
                "data": []
            },
            "institution": {
                "links": {
                    "self": "http://localhost:5004/lettres/api/1.0/documents/25/relationships/institution",
                    "related": "http://localhost:5004/lettres/api/1.0/documents/25/institution"
                },
                "data": {
                    "id": 3,
                    "type": "institution"
                }
            },
            "tradition": {
                "links": {
                    "self": "http://localhost:5004/lettres/api/1.0/documents/25/relationships/tradition",
                    "related": "http://localhost:5004/lettres/api/1.0/documents/25/tradition"
                },
                "data": null
            },
            "owner": {
                "links": {
                    "self": "http://localhost:5004/lettres/api/1.0/documents/25/relationships/owner",
                    "related": "http://localhost:5004/lettres/api/1.0/documents/25/owner"
                },
                "data": {
                    "id": 2,
                    "type": "user"
                }
            },
            "whitelist": {
                "links": {
                    "self": "http://localhost:5004/lettres/api/1.0/documents/25/relationships/whitelist",
                    "related": "http://localhost:5004/lettres/api/1.0/documents/25/whitelist"
                },
                "data": null
            },
            "prev-document": {
                "links": {
                    "self": "http://localhost:5004/lettres/api/1.0/documents/25/relationships/prev-document",
                    "related": "http://localhost:5004/lettres/api/1.0/documents/25/prev-document"
                },
                "data": null
            },
            "next-document": {
                "links": {
                    "self": "http://localhost:5004/lettres/api/1.0/documents/25/relationships/next-document",
                    "related": "http://localhost:5004/lettres/api/1.0/documents/25/next-document"
                },
                "data": null
            }
        }
    },
    "jsonapi": {
        "version": "1.0"
    },
    "meta": {
        "search-fields": [
            "title"
        ],
        "total-count": 1
    }
}
```

- Une requête mal formulée (champ obligatoire manquant, erreur de syntaxe) aura comme réponse ```403 Forbidden```
- Une requête faisant référence à une ressource non existante aura comme réponse ```404 NOT FOUND```


## Manipulation des relations et modification des resources

Il y a deux manières de procéder pour ajouter une ressource à un document.

Dans le **premier cas**, la création de la ressource (ex: image) peut être faite indépendemment de celle du document :

```json
curl -X POST \
  http://localhost:5004/lettres/api/1.0/images \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "data": {
        "type": "image",
        "attributes": {
            "canvas-idx": 10,
            "manifest-url": "http://burgess.biz/"
        }
    }
}'
```
Il n'est pas nécessaire de fournir de champ `id`, bien que cela reste possible (au même niveau que le champ ```type```), le client doit s'assurer de l'unicité de l'```id``` sous peine de recevoir une réponse ```409 Conflict```.

Liaison avec le document :
```json
curl -X PATCH \
  http://localhost:5004/lettres/api/1.0/images/1/relationships/document \
  -H 'Accept: application/vnd.api+json' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
	"data" : {"id" : 3, "type": "document"}
}'
```

Réponse ```200 OK```
```json
{
    "data": {
        "type": "image",
        "id": 1,
        "attributes": {
            "canvas-idx": 4,
            "manifest-url": "http://gonzalez.com/main/homepage.html"
        },
        "meta": {},
        "links": {
            "self": "http://localhost:5004/lettres/api/1.0/images/1"
        },
        "relationships": {
            "document": {
                "links": {
                    "self": "http://localhost:5004/lettres/api/1.0/images/1/relationships/document",
                    "related": "http://localhost:5004/lettres/api/1.0/images/1/document"
                },
                "data": {
                    "id": 3,
                    "type": "document"
                }
            }
        }
    },
    "jsonapi": {
        "version": "1.0"
    },
    "meta": {
        "search-fields": [],
        "total-count": 1
    }
}
```

Dans le **second cas**, il est nécessaire d'avoir l'```id``` du document pour le lier à la ressource :

```json
curl -X POST \
  http://localhost:5004/lettres/api/1.0/images \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
    "data": {
        "type": "image",
        "attributes": {
            "canvas-idx": 4,
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
}'
```

La méthode ```POST``` ajoute une ressource tandis que ```PATCH``` remplace toutes les ressources d'une relation.
Il est possible de supprimer une association entre deux ressources en fournissant ```null``` comme valeur de la relation :

Pour retirer toutes les images du document 1 :
```json
curl -X PATCH \
  http://localhost:5004/lettres/api/1.0/documents/1/relationships/images \
  -H 'Accept: application/vnd.api+json' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
	"data" : null
}'
```

Pour ne retirer qu'une seule image d'un document, il est cependant plus facile de passer par la relation inverse (image -> document).

Pour retirer l'image d'```id``` 5 du document auquel elle est (potentiellement) associée :
```json
curl -X PATCH \
  http://localhost:5004/lettres/api/1.0/images/5/relationships/document \
  -H 'Accept: application/vnd.api+json' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
	"data" : null
}'
```
Mais il est également possible de **supprimer** la ressource de la base :

```json
curl -X DELETE \
  http://localhost:5004/lettres/api/1.0/images/5 \
  -H 'cache-control: no-cache'
```
Réponse ```204 NO CONTENT```
