"""Remplace le libellé "[note]" des appels de notes par leur numéro.

Le front remplace à l'affichage "[note]" par la position de la note dans la liste des notes
de la lettre (getNoteIndex, "TODO remove once [note] have been replaced in database").
Ce script écrit ce même numéro en base, en retirant les <span> et les caractères U+FEFF
qui entourent parfois le libellé :
    <a class="note" href="#4820"><span>[note]</span></a>  ->  <a class="note" href="#4820">[1]</a>

Champs traités : titre, analyse, transcription, adresse (ceux que le front renumérote).
Les appels déjà numérotés ne sont pas modifiés. Le script peut être relancé.

Usage (depuis lettres-app) :
    python3 db/utils/number_note_calls.py db/lettres.staging.sqlite            # simulation
    python3 db/utils/number_note_calls.py db/lettres.staging.sqlite --apply    # écriture
"""
import argparse
import sqlite3
import re

FIELDS = ("title", "argument", "transcription", "address")
NOTE_CALL = re.compile(r'<a class="note" href="#(\d+)">(?:\uFEFF|</?span>)*\[note\](?:\uFEFF|</?span>)*</a>', re.I)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("database")
    parser.add_argument("--apply", action="store_true", help="écrire les modifications (sinon simulation)")
    args = parser.parse_args()

    db = sqlite3.connect(args.database)
    # même ordre que la liste des notes renvoyée par l'API
    positions = {}
    for note_id, document_id in db.execute("SELECT id, document_id FROM note ORDER BY document_id, id"):
        notes = positions.setdefault(document_id, {})
        notes[note_id] = len(notes) + 1

    documents, calls, unknown, examples = 0, 0, [], []
    try:
        for row in db.execute(f"SELECT id, {', '.join(FIELDS)} FROM document").fetchall():
            document_id, updates = row[0], {}
            for field, html in zip(FIELDS, row[1:]):
                if not html:
                    continue

                def number(match):
                    nonlocal calls
                    note_id = int(match.group(1))
                    index = positions.get(document_id, {}).get(note_id)
                    if index is None:
                        unknown.append((document_id, field, note_id))
                        return match.group(0)
                    calls += 1
                    return f'<a class="note" href="#{note_id}">[{index}]</a>'

                new_html = NOTE_CALL.sub(number, html)
                if new_html != html:
                    updates[field] = new_html
                    if len(examples) < 5:
                        i = new_html.index('class="note"')
                        examples.append(f"lettre {document_id}, {field} : ...{new_html[max(0, i - 50):i + 40]}")
            if updates:
                documents += 1
                assignments = ", ".join(f"{field} = ?" for field in updates)
                db.execute(f"UPDATE document SET {assignments} WHERE id = ?", (*updates.values(), document_id))

        print(f"{calls} appel(s) numéroté(s) dans {documents} lettre(s)")
        for example in examples:
            print(f"  {example}")
        if unknown:
            print(f"appels vers une note absente de la lettre (non modifiés) : {unknown}")
        if args.apply:
            db.commit()
            print("modifications enregistrées")
        else:
            db.rollback()
            print("simulation : rien n'a été écrit (ajouter --apply pour enregistrer)")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
