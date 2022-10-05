import logging
from faker import Faker
from faker.generator import random
from sqlalchemy.exc import IntegrityError
from app.models import Collection, WITNESS_STATUS_VALUES, TRADITION_VALUES


def create_fake_users(db, nb_users=50, fake=None):
    from app.models import User
    from app.models import UserRole

    if fake is None:
        fake = Faker()

    #logging.getLogger('faker.factory').setLevel(logging.ERROR)

    admin = UserRole(name=fake.word())
    contributor = UserRole(name=fake.word())

    db.session.add(admin)
    db.session.add(contributor)
    db.session.commit()

    roles = [admin, contributor]

    for i in range(0, nb_users):
        u1 = User(
            username=fake.user_name(),
            password=fake.user_name(),
            email=fake.free_email(),
            active=1,
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        u1.role = roles[1]
        db.session.add(u1)
        db.session.commit()


def create_fake_documents(db, nb_docs=1000, nb_correspondents=None, fake=None):
    from app.models import Document
    from app.models import Institution
    from app.models import User
    from app.models import Image
    from app.models import Note
    from app.models import Language
    from app.models import PersonRole
    from app.models import Person
    from app.models import Witness

    if fake is None:
        fake = Faker()
    logging.getLogger('faker.factory').setLevel(logging.ERROR)

    users = User.query.all()

    # add some languages
    db.session.add(Language(code="FRO"))
    db.session.add(Language(code="ENG"))
    db.session.add(Language(code="OCC"))
    db.session.add(Language(code="CZC"))
    db.session.add(Language(code="ITA"))
    db.session.commit()
    languages = Language.query.all()

    # add fake collections
    for i in range(1, 3):
        db.session.add(
            Collection(title=fake.sentence(), description=fake.text(), admin_id=random.choice(users).id)
        )
    db.session.flush()
    root_cols = Collection.query.all()
    for i in range(1, 2):
        root_col = random.choice(root_cols)
        db.session.add(
            Collection(title=fake.sentence(), description=fake.text(), parent_id=root_col.id, admin_id=root_col.admin_id)
        )
    db.session.commit()
    collections = Collection.query.all()

    # add fake correspondent roles
    for i in range(5, 20):
        db.session.add(PersonRole(label=fake.word(), description=fake.sentence()))
        db.session.flush()
    roles = PersonRole.query.all()

    # add fake persons
    if nb_correspondents is None:
        nb_correspondents = nb_docs * 2

    for i in range(0, nb_correspondents):
        db.session.add(Person(
            label=fake.name(),
            ref=fake.uri()
        ))
        db.session.flush()
    correspondents = Person.query.all()

    # add fake Institutions
    institutions = []
    for i in range(0, 20):
        ins = Institution(name=fake.sentence(nb_words=3), ref=fake.uri())
        db.session.add(ins)
        institutions.append(ins)
        db.session.flush()

    # add fake documents
    last_progress = -1
    for n_doc in range(0, nb_docs):
        try:
            doc = Document(
                title=fake.sentence(),
                transcription=fake.text(max_nb_chars=1000),
                argument=fake.text()
            )
            doc.owner_id = users[0].id
            doc.languages = [languages[0], languages[1]]
            doc.collections = collections
            db.session.add(doc)
            db.session.flush()
            # add fake witnesses
            witnesses = []
            for i in range(0, 3):
                wit = Witness(
                    document_id=doc.id,
                    content=fake.sentence(),
                    tradition=random.choice(TRADITION_VALUES),
                    status=random.choice(WITNESS_STATUS_VALUES),
                    institution_id=random.choice(institutions).id,
                    classification_mark=fake.sentence()
                )
                db.session.add(wit)
                witnesses.append(wit)
                db.session.flush()

            # add fake Images
            for w in range(0, len(witnesses)):
                for i in range(0, 5):
                    img = Image(canvas_id=0, order_num=0, witness_id=witnesses[w].id)
                    db.session.add(img)

            # add fake Notes
            nb_notes = 50
            for i in range(0, nb_notes):
                n = Note(content=fake.paragraph(), document_id=doc.id)
                db.session.add(n)
                db.session.flush()

            # add fake correspondent to the doc
            from app.models import PersonHasRole

            correspondents_have_roles = []
            nb_corr = 3
            for i in range(0, nb_corr):
                role = roles[0]
                co = correspondents[i]
                correspondents_have_roles.append((role.id, co.id))

            c_h_roles = []
            for (role_id, co_id) in set(correspondents_have_roles):
                chr = PersonHasRole(
                    document_id=doc.id,
                    person_id=co_id,
                    person_role_id=role_id,
                    function=fake.sentence(),
                    field=random.choice([None, 'transcription'])
                )
                db.session.add(chr)
                c_h_roles.append(chr)
                db.session.flush()
            doc.correspondents_have_roles = c_h_roles

            docs = Document.query.filter(Document.id != doc.id).all()
            if len(docs) > 0:
                if len(docs) > doc.id - 1 > 0:
                    doc.next_document = docs[doc.id - 1]

            db.session.add(doc)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            print("Warning:", e)

        progress = int(n_doc / nb_docs * 100)
        if progress % 10 == 0 and last_progress != progress:
            print("%s..." % progress, end="", flush=True)
            last_progress = progress

        db.session.commit()
