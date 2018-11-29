import random
import sqlalchemy
from faker import Faker
from sqlalchemy.exc import IntegrityError


def create_fake_users(db, nb_users=50, fake=None):
    from app.models import User
    from app.models import UserRole
    from app.models import Whitelist

    if fake is None:
        fake = Faker()

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
                active=random.choice([0, 1]),
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            u1.role = random.choice(roles)
            u1.whitelists = [random.choice(whitelists)]
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
    db.session.commit()
    roles = CorrespondentRole.query.all()

    # add fake correspondents
    if nb_correspondents is None:
        nb_correspondents = nb_docs * 2

    for i in range(0, nb_correspondents):
        db.session.add(Correspondent(
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            key=fake.name(),
            ref=random.choice([None, fake.uri()])
        ))
    db.session.commit()
    correspondents = Correspondent.query.all()

    # add fake Institutions
    institutions = []
    for i in range(0, 20):
        ins = Institution(name=fake.sentence(nb_words=3), ref=fake.uri())
        db.session.add(ins)
        institutions.append(ins)
    db.session.commit()

    # add fake Traditions
    traditions = []
    for i in range(0, 20):
        trad = Tradition(label=fake.word(), description=fake.sentence())
        db.session.add(trad)
        traditions.append(trad)
    db.session.commit()

    # add fake documents
    last_progress = -1
    for n_doc in range(0, nb_docs):

        try:
            doc = Document(
                title=fake.sentence(),
                witness_label=fake.sentence(nb_words=5),
                classification_mark=fake.sentence(nb_words=10),
                transcription=fake.text(max_nb_chars=random.randint(100, 7500)),
                argument=fake.text()
            )
            doc.institution = random.choice(institutions)
            doc.tradition = random.choice(traditions)
            doc.owner_id = random.choice(users).id
            doc.whitelist_id = random.choice(whitelists).id
            doc.languages = random.choices(languages)

            db.session.add(doc)
            db.session.commit()

            # add fake Images
            nb_images = random.randint(1, 10)
            for i in range(0, nb_images):
                img = Image(img_url=fake.uri(), manifest_url=fake.uri(), document_id=doc.id)
                db.session.add(img)

            # add fake Notes
            for i in range(0, random.randint(0, 30)):
                n = Note(label=fake.sentence(), content=fake.paragraph(), document_id=doc.id)
                db.session.add(n)

            # add fake correspondent to the doc
            from app.models import CorrespondentHasRole

            correspondents_have_roles = []
            for i in range(1, random.randint(1, 4)):
                role = random.choice(roles)
                co = random.choice(correspondents)
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
            db.session.commit()
            doc.correspondents_have_roles = c_h_roles

            if random.randint(0, 10) % 2 == 0:
                docs = Document.query.filter(Document.id != doc.id).all()
                if len(docs) > 0:
                    doc.next_document = random.choice(docs)

            db.session.add(doc)

        except IntegrityError as e:
            db.session.rollback()

        progress = int(n_doc / nb_docs * 100)
        if progress % 10 == 0 and last_progress != progress:
            print("%s..." % progress, end="", flush=True)
            last_progress = progress
    db.session.commit()

