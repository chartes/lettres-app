from faker import Faker
from flask import current_app

from .create_fake_data import create_fake_users, create_fake_documents


def load_fixtures(db):

    fake = Faker()
    fake.seed(12345)
    #db.session = db.create_scoped_session()
    #current_app.mce.register_events(db.session)
    create_fake_users(db, nb_users=5, fake=fake)
    create_fake_documents(db, nb_docs=10, nb_correspondents=8, fake=fake)
