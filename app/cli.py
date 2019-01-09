import click

from app import create_app, db
from app.api.document.facade import DocumentFacade
from app.models import UserRole, User, Document

app = None


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
        app = create_app(config)

    @click.command("db-create")
    def db_create():
        """ Creates a local database
        """
        with app.app_context():
            db.create_all()

            UserRole.add_default_roles()
            User.add_default_users()

            db.session.commit()
            click.echo("Created the database")

    @click.command("db-recreate")
    def db_recreate():
        """ Recreates a local database. You probably should not use this on
        production.
        """
        with app.app_context():
            db.drop_all()
            db.create_all()

            UserRole.add_default_roles()
            User.add_default_users()

            db.session.commit()
            click.echo("Dropped then recreated the database")

    @click.command("db-fixtures")
    def db_fixtures():
        """ Loads demo/tests data to the database
        """
        with app.app_context():
            db.drop_all()
            db.create_all()

            from faker import Faker
            fake = Faker()
            fake.seed(12345)
            from db.fixtures.create_fake_data import create_fake_documents, create_fake_users
            print("Generating fake data...", end=" ", flush=True)
            create_fake_users(db, nb_users=5, fake=fake)
            create_fake_documents(db, nb_docs=100, nb_correspondents=20, fake=fake)
            print("done !")

            click.echo("Loaded fixtures to the database")

    @click.command("db-reindex")
    def db_reindex():
        """
        Rebuild the elasticsearch indexes from the current database
        """
        with app.app_context():
            index_name = DocumentFacade.get_index_name()
            print("Reindexing... %s" % index_name, end="")
            app.elasticsearch.indices.delete(index=index_name, ignore=[400, 404])  # remove all records
            for doc in Document.query.all():
                print("Indexing", doc)
                doc.update_index(doc)
            print("completed!")

    @click.command("run")
    def run():
        """ Run the application in Debug Mode [Not Recommended on production]
        """
        app.run()

    cli.add_command(db_create)
    cli.add_command(db_fixtures)
    cli.add_command(db_recreate)
    cli.add_command(db_reindex)
    cli.add_command(run)

    return cli
