import logging
from faker import Faker
from faker.generator import random
from sqlalchemy.exc import IntegrityError


def create_fake_users(db, nb_users=50, fake=None):
    from app.models import User
    from app.models import UserRole
    from app.models import Whitelist

    if fake is None:
        fake = Faker()

    logging.getLogger('faker.factory').setLevel(logging.ERROR)

    wl1 = Whitelist(label="Whitelist1")
    admin = UserRole(label="admin")
    contributor = UserRole(label="contributor")

    db.session.add(wl1)
    db.session.add(admin)
    db.session.add(contributor)
    db.session.commit()

    roles = [admin, contributor]
    whitelists = [wl1]
    try:
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
            u1.whitelists = whitelists
            db.session.add(u1)
            db.session.commit()
    except IntegrityError as e:
        db.session.rollback()


def create_fake_documents(db, nb_docs=1000, nb_correspondents=None, fake=None):
    from app.models import Document
    from app.models import Institution
    from app.models import Tradition
    from app.models import User
    from app.models import Whitelist
    from app.models import Image
    from app.models import Note
    from app.models import Language
    from app.models import CorrespondentRole
    from app.models import Correspondent

    if fake is None:
        fake = Faker()
    logging.getLogger('faker.factory').setLevel(logging.ERROR)

    users = User.query.all()
    whitelists = Whitelist.query.all()

    # add some languages
    db.session.add(Language(code="FRO"))
    db.session.add(Language(code="ENG"))
    db.session.add(Language(code="OCC"))
    db.session.add(Language(code="CZC"))
    db.session.add(Language(code="ITA"))
    db.session.commit()
    languages = Language.query.all()

    # add fake correspondent roles
    for i in range(5, 20):
        db.session.add(CorrespondentRole(label=fake.word()))
        db.session.flush()
    roles = CorrespondentRole.query.all()

    # add fake correspondents
    if nb_correspondents is None:
        nb_correspondents = nb_docs * 2

    for i in range(0, nb_correspondents):
        db.session.add(Correspondent(
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            key=fake.name(),
            ref=fake.uri()
        ))
        db.session.flush()
    correspondents = Correspondent.query.all()

    # add fake Institutions
    institutions = []
    for i in range(0, 20):
        ins = Institution(name=fake.sentence(nb_words=3), ref=fake.uri())
        db.session.add(ins)
        institutions.append(ins)
        db.session.flush()

    # add fake Traditions
    traditions = []
    for i in range(0, 20):
        trad = Tradition(label=fake.word(), description=fake.sentence())
        db.session.add(trad)
        traditions.append(trad)
        db.session.flush()

    # add fake documents
    last_progress = -1
    for n_doc in range(0, nb_docs):
        try:
            doc = Document(
                title=fake.sentence(),
                witness_label=fake.sentence(nb_words=5),
                classification_mark=fake.sentence(nb_words=10),
                transcription=fake.text(max_nb_chars=1000),
                argument=fake.text()
            )
            doc.institution = institutions[0]
            doc.tradition = traditions[0]
            doc.owner_id = users[0].id
            doc.whitelist_id = whitelists[0].id
            doc.languages = [languages[0], languages[1]]

            db.session.add(doc)
            db.session.flush()

            # add fake Images
            nb_images = 10
            for i in range(0, nb_images):
                img = Image(canvas_idx=random.randint(0, 100), manifest_url=fake.uri(), document_id=doc.id)
                db.session.add(img)
                db.session.flush()

            # add fake Notes
            nb_notes = 50
            for i in range(0, nb_notes):
                n = Note(label=fake.sentence(), content=fake.paragraph(), document_id=doc.id)
                db.session.add(n)
                db.session.flush()

            # add fake correspondent to the doc
            from app.models import CorrespondentHasRole

            correspondents_have_roles = []
            nb_corr = 3
            for i in range(0, nb_corr):
                role = roles[0]
                co = correspondents[i]
                correspondents_have_roles.append((role.id, co.id))

            c_h_roles = []
            for (role_id, co_id) in set(correspondents_have_roles):
                chr = CorrespondentHasRole(
                    document_id=doc.id,
                    correspondent_id=co_id,
                    correspondent_role_id=role_id
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
