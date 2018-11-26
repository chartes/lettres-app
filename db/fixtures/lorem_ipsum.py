


def load_fixtures(db):
    # test
    from app.models import Document
    from app.models import Institution
    from app.models import Tradition
    from app.models import User
    from app.models import UserRole
    from app.models import Whitelist
    from app.models import Image
    from app.models import Note
    from app.models import Language
    from app.models import CorrespondentRole
    from app.models import Correspondent

    ur = UserRole(label="admin")

    u1 = User(username="u1", password="u1", email="u1@u1.u1", active=1, first_name='User1', last_name='User1')
    u1.role = ur
    db.session.add(u1)
    db.session.commit()

    wl1 = Whitelist(label="Whitelist1")
    db.session.add(wl1)
    db.session.commit()

    u1.whitelists = [wl1]
    db.session.add(u1)

    d1 = Document(title="Test1")
    d1.institution = Institution(name="Instit1", ref="ref instit1")
    d1.tradition = Tradition(label="Tradition1", description="description tradition 1")
    d1.owner_id = u1.id
    d1.whitelist_id = wl1.id

    db.session.add(d1)
    db.session.commit()

    i1 = Image(img_url="http://url", manifest_url="http://url")
    i1.document_id = d1.id
    db.session.add(i1)
    db.session.commit()

    n1 = Note(content="note1", label="label note")
    n1.document_id = d1.id
    db.session.add(n1)
    db.session.commit()

    l1 = Language(code="FRO")
    d1.languages = [l1]
    db.session.add(l1)
    db.session.commit()

    cr1 = CorrespondentRole(label="emetteur")
    db.session.add(cr1)
    db.session.commit()

    c1 = Correspondent(firstname="Correspondent1")
    db.session.add(c1)
    db.session.commit()

    from app.models import CorrespondentHasRole
    d1.correspondents_have_roles = [
        CorrespondentHasRole(document_id=d1.id, correspondent_id=c1.id, correspondent_role_id=cr1.id)]

    d2 = Document(title="Test2")
    d2.owner_id = u1.id
    db.session.add(d2)
    db.session.commit()

    d2.prev_document = d1
    db.session.add(d2)
    db.session.commit()

    print(d1.id, d2.prev_document_id, d1.next_document,
          d1.whitelist_id, wl1.users,
          d1.images, d1.notes, d1.languages,
          [(c.correspondent.id, c.correspondent_role) for c in d1.correspondents_have_roles])