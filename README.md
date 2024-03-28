# Lettres

## Installation
Dans un répertoire local dédié au projet :
- Cloner le repository GitHub :
```bash
git clone https://github.com/chartes/lettres-app.git
```

Dans le répertoire d'accueil de l'application :
- Exécuter les commandes :
```bash
python3 -m venv lettresenv
source lettresenv/bin/activate
pip install -r requirements.txt
```

- Se rendre dans le sous-répertoire contenant le fichier flask_app.py et le lancer :
```bash
python3 flask_app.py
```
- Lancer une requête de contrôle :
(ex: http://127.0.0.1:5004/lettres/api/1.0/documents?page[size]=2)


## Indexation

Installer la version Elasticsearch conforme aux spécifications.
Avec docker cela donne :
```bash
docker run --name es-lettres -d -p 9200:9200  elasticsearch:8.12.1
docker exec es-lettres bash -c "bin/elasticsearch-plugin install analysis-icu"
docker restart es-lettres
```

Lors de la première indexation, avec une application en local
sur le port 5004, utiliser la commande :
```bash
python3 manage.py (--config=<dev/prod>) db-reindex --rebuild --host=http://localhost:5004
```
Cette commande crée les index de l'application sur la base des [mappings](./elasticsearch/)

Pour les indexations suivantes, exécuter :
```bash
python3 manage.py (--config=<dev/prod>) db-reindex --host=http://localhost:5004
```

## Ajouter un utilisateur

Depuis le répertoire d'accueil de l'application, exécuter :
```bash
python3 manage.py add-user --email=<email@email.fr> --username=<username> --password=<userpassword>
```

Ajouter le flag `--admin` pour accorder des droits d'administrateur à l'utilisateur.


## Documentation :
- [Documentation de l'API](./docs/API.md)

## Lancer le front-end
- [Readme du Front-end](https://github.com/chartes/lettres-vue/blob/dev/README.md)
