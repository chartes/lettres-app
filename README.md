# L'API de [Lettres](https://ecco.chartes.psl.eu/)
API de l'application Lettres (édition collaborative de correspondances).

![Static Badge](https://img.shields.io/badge/python-3.12-blue?style=for-the-badge&logo=python&label=PYTHON&color=blue)

![Static Badge](https://img.shields.io/badge/Flask-2.3.2-blue?logo=flask)
![Static Badge](https://img.shields.io/badge/elasticsearch-8.12-blue?logo=elasticsearch)

## Prérequis - Installer Elasticsearch

### Installer Elasticsearch _et_ son plugin ICU

:warning: Utiliser une version d'Elasticsearch compatible avec [requirements.txt](./requirements.txt)
:information_source: Les commandes ci-dessous sont exécutées hors environnement virtuel (`deactivate`)
  - Elasticsearch : se référer aux instructions de votre organisation ou à la [documentation d'Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html#elasticsearch-install-packages)
  - [Plugin ICU](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html) : vérifier s'il est installé avec `uconv -V`, sinon :
    <pre><code><b><i>chemin/vers/elasticsearch</i></b>/bin/elasticsearch-plugin install analysis-icu</code></pre>

- Avec docker (sécurité désactivée) :
```bash
docker run --name es-lettres -d -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" elasticsearch:8.12.1
docker exec es-lettres bash -c "bin/elasticsearch-plugin install analysis-icu"
docker restart es-lettres
```

## Installation

- Cloner le repository GitHub dans le répertoire des projets :
<pre><code>
  cd <b><i>chemin/vers/projets</i></b>
  git clone https://github.com/chartes/lettres-app.git
</code></pre>

- S'assurer d'utiliser Python 3.12, par exemple avec pyenv :
  ```bash
  pyenv shell 3.12
  ```

- Créer l'environnement virtuel (les répertoires `venv*` sont ignorés par git) :
  <pre><code>
  cd <b><i>chemin/vers/projets</i></b>/lettres-app
  python -m venv <b><i>your_venv_name</i></b>
  source <b><i>your_venv_name</i></b>/bin/activate
  pip install -r requirements.txt
  </code></pre>

- Pour les serveurs qui utilisent uWSGI pour lancer les applications Python (serveurs Nginx distants) :
  - vérifier si uWSGI est installé : `pip list --local`
  - sinon l'installer dans l'environnement virtuel : `pip install uwsgi`.
  L'application WSGI est `flask_app:flask_app`
  *NB : cette commande peut nécessiter wheel :*
    - pour vérifier si wheel est installé : `pip show wheel`
    - pour l'installer si besoin : `pip install wheel`

## Copier la base de données

- Récupérer la dernière base de données
- La copier, avec les droits appropriés, dans le répertoire <b><i>chemin/vers/lettres-app</i></b>/db
- Le chemin de la base est défini par `DATABASE_URI` dans le fichier `<config>.env` : `db/lettres.local.sqlite`, `db/lettres.staging.sqlite`, etc.

## Configuration

Les fichiers `local.env`, `staging.env`, `prod.env` et `test.env` contiennent la configuration de chaque environnement.
Le fichier utilisé est choisi avec l'option `--config` (`staging` par défaut). Sur les serveurs, il peut être imposé par la variable d'environnement `SERVER_ENV_CONFIG` (prioritaire sur `--config`).
Les variables d'environnement déjà définies sont prioritaires sur celles du fichier `.env`.

Avec la sécurité d'Elasticsearch activée, les identifiants sont indiqués dans `ELASTICSEARCH_URL` (`https://elastic:<mot_de_passe>@localhost:9200`).

## Lancer l'application

> :warning: Les commandes ci-dessous servent surtout au lancement en local.
> Sur les serveurs, les applications sont lancées par des outils de gestion de processus (supervisor + uWSGI), se référer à la documentation des serveurs.
  - Réactiver l'environnement virtuel si besoin (<code>source <b><i>your_venv_name</i></b>/bin/activate</code>)
  - Depuis le répertoire contenant flask_app.py (<code>cd <b><i>chemin/vers/lettres-app</i></b></code>) :
```bash
python flask_app.py (--config=<local/staging/prod>)
```
  - Lancer une requête de contrôle : http://localhost:5004/api/1.0/documents?page[size]=2

## Indexation

> :warning: Les commandes d'indexation sont exécutées dans l'environnement virtuel de l'application, qui doit être lancée.
>
> Les options sont indiquées entre parenthèses <em>(option)</em>. Les retirer si besoin.
>
> `--host` est l'URL racine de l'API lancée : `http://localhost:5004` en local, l'URL publique sur les serveurs (ex. `https://dev.chartes.psl.eu/ecco`). Elle sert à construire les liens enregistrés dans les index.

Lors de la première indexation, ou pour recréer les index selon les [mappings](./elasticsearch/) :
```bash
python manage.py (--config=<local/staging/prod>) db-reindex --rebuild --host=http://localhost:5004
```

Pour les indexations suivantes :
```bash
python manage.py (--config=<local/staging/prod>) db-reindex --host=http://localhost:5004
```

Les index sont nommés `<INDEX_PREFIX>__<type>` (ex. `ecco__documents`).
Pour vérifier qu'ils ont bien été créés :
```bash
curl http://localhost:9200/_cat/indices?v
```

## Ajouter un utilisateur

Depuis le répertoire de l'application, exécuter :
```bash
python manage.py (--config=<local/staging/prod>) add-user --email=<email@email.fr> --username=<username> --password=<userpassword>
```

Ajouter le flag `--admin` pour accorder des droits d'administrateur à l'utilisateur.

## Documentation
- [Documentation de l'API](./docs/API.md)

## Lancer le front-end
- [Readme du Front-end](https://github.com/chartes/lettres-vue/blob/dev/README.md)

---
Détail des commandes hors ligne :

```bash
python manage.py --help

Usage: manage.py [OPTIONS] COMMAND [ARGS]...

Options:
  --config [local|staging|prod|test]
                                  select appropriate .env file to use
                                  [default: staging]
  --help                          Show this message and exit.

Commands:
  add-user
  db-create    Creates a local database
  db-recreate  Recreates a local database.
  db-reindex   Rebuild the elasticsearch indexes from the current database
  run          Run the application in Debug Mode [Not Recommended on...
```
