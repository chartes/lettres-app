import os
from datetime import datetime

import click
import json
import re
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


clean_tags = re.compile('<.*?>')
clean_notes = re.compile('\[\d+\]')
clean_page_breaks = re.compile('\[p\.?\s?\d+\]')
def remove_html_tags(text):
    without_unbreakable_space = text.replace('\ufeff','') if text else None
    without_html_content = re.sub(clean_tags,'', without_unbreakable_space) if text else None
    without_without_notes = without_html_content.replace("[note]","").strip() if without_html_content else None
    without_numbered_notes = re.sub(clean_notes,' ', without_without_notes) if without_without_notes else None
    without_page_breaks = re.sub(clean_page_breaks,' ', without_numbered_notes) if without_numbered_notes else None
    cleaned = re.sub(' +', ' ', without_page_breaks) if without_page_breaks else None
    return cleaned

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
                with open('elasticsearch/%s.conf.json' % conf_name, 'r') as f:
                    payload = json.load(f)
                    print("payload : ", payload)
                    payload["settings"] = settings
                    print("payload : ", payload)
                    res = requests.put(url, json=payload)
                    assert str(res.status_code).startswith("20")

    except FileNotFoundError as e:
        print("no conf...", flush=True, end=" ")
    except Exception as e:
        print("res.text error : ", str(e), flush=True, end=" ")
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
                            if index_name == "lettres__development__documents":
                                #print("Rebuilding ", index_name)
                                if f_obj.obj.title is not None and len(f_obj.obj.title) >0:
                                    f_obj.obj.title = remove_html_tags(f_obj.obj.title)
                                    #print('f_obj.id / f_obj.obj.title : ', f_obj.id, f_obj.obj.title)
                                if f_obj.obj.argument is not None and len(f_obj.obj.argument) >0:
                                    f_obj.obj.argument = remove_html_tags(f_obj.obj.argument)
                                    #print('f_obj.id / f_obj.obj.argument : ', f_obj.id, f_obj.obj.argument)
                                if f_obj.obj.transcription is not None and len(f_obj.obj.transcription) >0:
                                    f_obj.obj.transcription = remove_html_tags(f_obj.obj.transcription)
                                    #print('f_obj.id / f_obj.obj.transcription : ', f_obj.id, f_obj.obj.transcription)
                                f_obj.reindex("insert", propagate=False)
                            else:
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
