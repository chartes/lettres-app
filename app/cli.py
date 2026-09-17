import os
from datetime import datetime

import click
import json
import pprint
import requests
from elasticsearch.helpers import BulkIndexError, streaming_bulk
from sqlalchemy.orm import selectinload

from app import create_app
from app.api.collection.facade import CollectionFacade
from app.api.person.facade import PersonFacade
from app.api.document.facade import DocumentFacade
from app.api.institution.facade import InstitutionFacade
from app.api.language.facade import LanguageFacade
from app.api.placename.facade import PlacenameFacade
from app.api.user.facade import UserFacade
from app.api.witness.facade import WitnessFacade
from app.models import UserRole, User, Document, Collection, Language, Witness, Person, Institution, Placename, \
    PersonHasRole, PlacenameHasRole, Lock

app = None


def add_default_users(db):
    UserRole.add_default_roles()
    db.session.flush()
    User.add_default_users()


def load_elastic_conf(conf_name, index_name, rebuild=False):
    url = '/'.join([app.config['ELASTICSEARCH_URL'], index_name])
    print("url", url)
    res = None
    try:
        if rebuild:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
                "Upgrade-Insecure-Requests": "1", "DNT": "1",
                "Content-Type": "application/json",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
            res = requests.delete(url, headers=headers)
            #res = requests.delete(url)
            print("res delete: ", res)

            with open('elasticsearch/_settings.conf.json', 'r') as _settings:
                settings = json.load(_settings)
                print("settings : ", settings)

                print("'elasticsearch/%s.conf.json' % conf_name : ", 'elasticsearch/%s.conf.json' % conf_name)
                try:
                    with open('elasticsearch/%s.conf.json' % conf_name, 'r') as f:
                        payload = json.load(f)
                except FileNotFoundError:
                    # no mappings: create the index with the shared settings (number_of_replicas...)
                    # instead of letting the first insert create it with the ES defaults (1 replica)
                    print("no conf...", flush=True, end=" ")
                    payload = {}
                payload["settings"] = settings
                print("payload : ", payload)
                res = requests.put(url, json=payload)
                assert str(res.status_code).startswith("20")

    except Exception as e:
        print("res.text error : ", str(e), flush=True, end=" ")
        raise e


def make_cli():
    """ Creates a Command Line Interface for everydays tasks

    :return: Click groum
    """
    @click.group()
    @click.option('--config', default="staging", type=click.Choice(["local", "staging", "prod", "test"]), help="select appropriate .env file to use", show_default=True)
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
    @click.option('--rebuild', is_flag=True, help="truncate the index before updating its configuration")
    def db_reindex(indexes, rebuild):
        """
        Rebuild the elasticsearch indexes from the current database
        """
        # relationships read by the facades when building the payloads, loaded upfront to avoid one query per object
        # (Document.collections is a dynamic relationship and cannot be eager loaded)
        document_loader_options = (
            selectinload(Document.witnesses),
            selectinload(Document.languages),
            selectinload(Document.persons_having_roles).options(
                selectinload(PersonHasRole.person), selectinload(PersonHasRole.person_role)),
            selectinload(Document.placenames_having_roles).options(
                selectinload(PlacenameHasRole.placename), selectinload(PlacenameHasRole.placename_role)),
            selectinload(Document.locks).selectinload(Lock.user),
        )
        indexes_info = {
            "collections": {"facade": CollectionFacade, "model": Collection},
            "languages": {"facade": LanguageFacade, "model": Language},
            "witnesses": {"facade": WitnessFacade, "model": Witness},
            "persons": {"facade": PersonFacade, "model": Person},
            "placenames": {"facade": PlacenameFacade, "model": Placename},
            "documents": {"facade": DocumentFacade, "model": Document, "loader_options": document_loader_options},
            "institutions": {"facade": InstitutionFacade, "model": Institution},
            "users": {"facade": UserFacade, "model": User}
        }

        def reindex_from_info(name, info):

            with app.app_context():

                print("Reindexing %s... " % name, end="", flush=True)

                index_name = info["facade"].get_index_name()

                url = "/".join([app.config['ELASTICSEARCH_URL'], index_name, '_settings'])

                def reset_readonly():
                    r = requests.put(url, json={"index.blocks.read_only_allow_delete": None})
                    assert (r.status_code == 200)

                def actions():
                    query = info["model"].query.options(*info.get("loader_options", ()))
                    for obj in query.all():
                        # the URL prefix is only used for API links, which are not indexed
                        for data in info["facade"]("", obj).get_data_to_index_when_added(propagate=False):
                            yield {"_index": data["index"], "_id": data["id"], "_source": data["payload"]}

                def bulk_index():
                    # one bulk request per chunk instead of one request per object
                    count = 0
                    for ok, item in streaming_bulk(app.elasticsearch, actions(), chunk_size=500):
                        count += 1
                    return count

                try:
                    load_elastic_conf(name, index_name, rebuild=rebuild)
                    try:
                        count = bulk_index()
                    except BulkIndexError as e:
                        # index blocked (read_only_allow_delete, e.g. after a disk watermark): unblock and retry
                        if not any(list(error.values())[0].get("error", {}).get("type") == "cluster_block_exception"
                                   for error in e.errors):
                            raise
                        reset_readonly()
                        count = bulk_index()
                    print("OK (%s)" % count)
                except Exception as e:
                    print("NOT OK!  ", str(e))

        if indexes == "all": # reindex every index configured above
            indexes = ",".join(indexes_info.keys())

        for name in indexes.split(","):
            if name in indexes_info:
                reindex_from_info(name, indexes_info[name])
            else:
                print("Warning: index %s does not exist or is not declared in the cli" % name)

    @click.command("add-user")
    @click.option('--email', required=True)
    @click.option('--username', required=True)
    @click.option('--password', required=True)
    @click.option('--admin', is_flag=True)
    def db_add_user(email, username, password, admin):
        with app.app_context():
            from app import db
            from werkzeug.security import generate_password_hash
            from werkzeug.security import check_password_hash

            pwd_hash = generate_password_hash(password)

            admin_role = UserRole.query.filter(UserRole.name == "admin").first()
            contributor_role = UserRole.query.filter(UserRole.name == "contributor").first()
            roles = [contributor_role, admin_role] if admin else [contributor_role]

            new_user = User(username=username,
                            password=pwd_hash,
                            email=email,
                            active=True,
                            email_confirmed_at=datetime.now(),
                            roles=roles)

            db.session.add(new_user)
            db.session.commit()
            print('User "%s" added' % username)
            #new_user.roles = [contributor_role]
            #db.session.commit()

    @click.command("run")
    def run():
        """ Run the application in Debug Mode [Not Recommended on production]
        """
        app.run()

    cli.add_command(db_create)
    cli.add_command(db_recreate)
    cli.add_command(db_reindex)
    cli.add_command(db_add_user)
    #cli.add_command(make_manifests)
    #cli.add_command(make_collection_manifests)

    cli.add_command(run)

    return cli
