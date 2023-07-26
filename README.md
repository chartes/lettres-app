# Lettres

## Installation
Dans un répertoire local dédié au projet :
- Cloner le repository GitHub : `git clone https://github.com/chartes/lettres-app.git`

Dans le répertoire d'accueil de l'application :
- Exécuter les commandes :
```
python3 -m venv lettresenv
source lettresenv/bin/activate
pip install -r requirements.txt
```

- Se rendre dans le sous-répertoire contenant le fichier flask_app.py et le lancer : `python3 flask_app.py`
- Lancer une requête de contrôle : http:/yourhost/lettres/api/1.0/documents?page[size]=2
(ex: http://127.0.0.1:5004/lettres/api/1.0/documents?page[size]=2)


## Indexation

Installer la version Elasticsearch conforme aux spécifications.
Avec docker cela donne :

```bash
docker run --name es-lettres -d -p 9200:9200  elasticsearch:6.8.22
docker exec es-lettres bash -c "bin/elasticsearch-plugin install analysis-icu"
docker restart es-lettres
```

Lors de la première indexation, en supposant que l'application tourne en local
sur le port 5004, utiliser la commande :

```bash
python3 manage.py db-reindex --rebuild --host=http://localhost:5004
```
Cette commande s'occupe de créer les index de l'application avec les bons
mappings.

Pour les indexations suivantes, exécuter :
```bash
python3 manage.py db-reindex --host=http://localhost:5004
```

## Ajouter un utilisateur

Depuis le répertoire d'accueil de l'application, exécuter :

`python3 manage.py add-user --email=myemail@email.fr --username=myusername --password=MySup3rPassw0rd!`

Ajouter le flag `--admin` pour ajouter les droits d'admin au compte crée


## Documentation :
- [Documentation de l'API](https://github.com/chartes/lettres-app/blob/master/docs/API.md)

## Lancer le front-end
- Voir [Readme du Front-end](https://github.com/chartes/lettres-vue/blob/dev/README.md)
