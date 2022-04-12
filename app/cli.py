import os

import click
import json
import pprint
import requests
from elasticsearch import AuthorizationException

from app import create_app
from app.api.collection.facade import CollectionFacade
from app.api.person.facade import PersonFacade
from app.api.document.facade import DocumentFacade
from app.api.institution.facade import InstitutionFacade
from app.api.language.facade import LanguageFacade
from app.api.placename.facade import PlacenameFacade
from app.api.user.facade import UserFacade
from app.api.witness.facade import WitnessFacade
from app.models import UserRole, User, Document, Collection, Language, Witness, Person, Institution, Placename

app = None


def add_default_users(db):
    UserRole.add_default_roles()
    db.session.flush()
    User.add_default_users()


def load_elastic_conf(conf_name, index_name, rebuild=False):
    url = '/'.join([app.config['ELASTICSEARCH_URL'], index_name])
    res = None
    try:
        if rebuild:
            res = requests.delete(url)

            with open('elasticsearch/_settings.conf.json', 'r') as _settings:
                settings = json.load(_settings)

                with open('elasticsearch/%s.conf.json' % conf_name, 'r') as f:
                    payload = json.load(f)
                    payload["settings"] = settings
                    res = requests.put(url, json=payload)
                    assert str(res.status_code).startswith("20")

    except FileNotFoundError as e:
        print("no conf...", flush=True, end=" ")
    except Exception as e:
        print(res.text, str(e), flush=True, end=" ")
        raise e


def make_cli():
    """ Creates a Command Line Interface for everydays tasks

    :return: Click groum
    """
    @click.group()
    @click.option('--config', default="dev")
    def cli(config):
        """ Generates the client"""
        click.echo("Loading the application")
        global app
        global env
        env = config
        app = create_app(config)

    @click.command("db-create")
    def db_create():
        """ Creates a local database
        """
        with app.app_context():
            from app import db
            db.create_all()

            add_default_users(db)

            db.session.commit()
            click.echo("Created the database")

    @click.command("db-recreate")
    def db_recreate():
        """ Recreates a local database. You probably should not use this on
        production.
        """
        with app.app_context():
            from app import db
            db.drop_all()
            db.create_all()

            add_default_users(db)

            db.session.commit()
            click.echo("Dropped then recreated the database")


    #@click.command('make-manifests')
    #@click.option('--host', required=False, default="https://dev.chartes.psl.eu")
    #@click.option('--witnesses', default=None)
    #@click.option('--upload', default=False)
    #def make_manifests(host, witnesses, upload):
    #    with app.app_context():
    #        if witnesses is None:
    #            witnesses = Witness.query.all()
    #        else:
    #            witnesses = Witness.query.filter(Witness.id.in_(witnesses.split(','))).all()
    #
    #        witnesses = [w for w in witnesses if w.images and len(w.images) > 0]
    #
    #        host = "{host}{api_prefix}".format(host=host, api_prefix=app.config["API_URL_PREFIX"])
    #
    #        for w in witnesses:
    #            manifest, manifest_url = app.manifest_factory.make_manifest(host, w)
    #
    #            tmp_filename = os.path.join(app.config.get('LOCAL_TMP_FOLDER'), "manifest{0}.json".format(w.id))
    #            print(tmp_filename, manifest_url, end="... ", flush=False)
    #            upload_manifest(tmp_filename, manifest, upload=upload)
    #            print('OK')
    #
    #@click.command('make-collection-manifests')
    #@click.option('--documents', default=None)
    #@click.option('--upload', default=False)
    #def make_collection_manifests(documents, upload):
    #    with app.app_context():
    #        if documents is None:
    #            documents = Document.query.all()
    #        else:
    #            documents = Document.query.filter(Document.id.in_(documents.split(','))).all()
    #
    #        for doc in documents:
    #
    #            collection, collection_url = app.manifest_factory.make_collection(doc)
    #
    #            tmp_filename = os.path.join(app.config.get('LOCAL_TMP_FOLDER'), "document{0}.json".format(doc.id))
    #            print(tmp_filename, collection_url, end="... ", flush=False)
    #            upload_collection(tmp_filename, collection, upload=upload)
    #            print('OK')

    @click.command("db-reindex")
    @click.option('--indexes', default="all")
    @click.option('--host', required=True)
    @click.option('--rebuild', is_flag=True, help="truncate the index before updating its configuration")
    def db_reindex(indexes, host, rebuild):
        """
        Rebuild the elasticsearch indexes from the current database
        """
        indexes_info = {
            "collections": {"facade": CollectionFacade, "model": Collection},
            "languages": {"facade": LanguageFacade, "model": Language},
            "witnesses": {"facade": WitnessFacade, "model": Witness},
            "persons": {"facade": PersonFacade, "model": Person},
            "placenames": {"facade": PlacenameFacade, "model": Placename},
            "documents": {"facade": DocumentFacade, "model": Document},
            "institutions": {"facade": InstitutionFacade, "model": Institution},
            "users": {"facade": UserFacade, "model": User}
        }

        def reindex_from_info(name, info):

            with app.app_context():

                prefix = "{host}{api_prefix}".format(host=host, api_prefix=app.config["API_URL_PREFIX"])
                print("Reindexing %s... " % name, end="", flush=True)

                index_name = info["facade"].get_index_name()

                url = "/".join([app.config['ELASTICSEARCH_URL'], index_name, '_settings'])

                def reset_readonly():
                    r = requests.put(url, json={"index.blocks.read_only_allow_delete": None})
                    assert (r.status_code == 200)

                try:
                    load_elastic_conf(name, index_name, rebuild=rebuild)

                    for obj in info["model"].query.all():
                        f_obj = info["facade"](prefix, obj)
                        try:
                            f_obj.reindex("insert", propagate=False)
                        except AuthorizationException:
                            reset_readonly()
                            f_obj.reindex("insert", propagate=False)

                    print("OK")
                except Exception as e:
                    print("NOT OK!  ", str(e))

        if indexes == "all": # reindex every index configured above
            indexes = ",".join(indexes_info.keys())

        for name in indexes.split(","):
            if name in indexes_info:
                reindex_from_info(name, indexes_info[name])
            else:
                print("Warning: index %s does not exist or is not declared in the cli" % name)

    @click.command("run")
    def run():
        """ Run the application in Debug Mode [Not Recommended on production]
        """
        app.run()

    cli.add_command(db_create)
    cli.add_command(db_recreate)
    cli.add_command(db_reindex)
    #cli.add_command(make_manifests)
    #cli.add_command(make_collection_manifests)

    cli.add_command(run)

    return cli
