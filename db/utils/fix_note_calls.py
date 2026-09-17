"""Corrige des appels de notes et recalcule les compteurs d'occurrences des notes.

1. Lettre 2 : ajoute l'appel de la note 1 à la fin du titre et de l'adresse (vérifié sur l'image Gallica).
2. Lettre 3470 : remplace le "[note]" sans lien (entouré de caractères U+FEFF résiduels)
   par l'appel de la note 4822 ([3]).
3. Toutes les notes : recalcule note.occurences d'après les appels réels de la lettre
   (titre, analyse, transcription, adresse, étiquette de date, contenu et cote des témoins).
   Les notes sans aucun appel ne sont pas modifiées, elles sont seulement signalées.

Le script peut être relancé : les corrections déjà faites ne sont pas refaites.

Usage (depuis lettres-app) :
    python db/utils/fix_note_calls.py db/lettres.staging.sqlite            # simulation
    python db/utils/fix_note_calls.py db/lettres.staging.sqlite --apply    # écriture
"""
import argparse
import collections
import re
import sqlite3

NOTE_CALL = re.compile(r'<a\b[^>]*\bclass="note"[^>]*>', re.I)
NOTE_HREF = re.compile(r'href="#(\d+)"')
DOCUMENT_FIELDS = ("title", "argument", "transcription", "address", "creation_label")


def fix_letter_2(db, changes):
    """Appel de la note 1 à la fin du titre et de l'adresse de la lettre 2."""
    call = '<a class="note" href="#1">[1]</a>'
    title, address = db.execute("SELECT title, address FROM document WHERE id = 2").fetchone()
    updates = {}
    for field, value in (("title", title), ("address", address)):
        if value and 'href="#1"' not in value:
            updates[field] = value + call
    for field, value in updates.items():
        db.execute(f"UPDATE document SET {field} = ? WHERE id = 2", (value,))
        changes.append(f"lettre 2, {field} : ...{value[-70:]}")


def fix_letter_3470(db, changes):
    """Le "[note]" sans lien de la transcription de la lettre 3470 devient l'appel de la note 4822."""
    transcription = db.execute("SELECT transcription FROM document WHERE id = 3470").fetchone()[0]
    if 'href="#4822"' in transcription:
        return
    new_transcription, count = re.subn(r'\uFEFF+\[note\]\uFEFF+', '<a class="note" href="#4822">[3]</a>', transcription)
    if count == 1:
        db.execute("UPDATE document SET transcription = ? WHERE id = 3470", (new_transcription,))
        i = new_transcription.index('href="#4822"')
        changes.append(f"lettre 3470, transcription : ...{new_transcription[i - 60:i + 40]}")
    elif count > 1:
        raise RuntimeError(f"lettre 3470 : {count} '[note]' sans lien trouvés, correction non appliquée")


def recount_occurrences(db, changes):
    """Recalcule note.occurences d'après les appels réels de chaque lettre."""
    calls = collections.defaultdict(collections.Counter)

    def count(document_id, html):
        for tag in NOTE_CALL.findall(html or ""):
            href = NOTE_HREF.search(tag)
            if href:
                calls[document_id][int(href.group(1))] += 1

    for row in db.execute(f"SELECT id, {', '.join(DOCUMENT_FIELDS)} FROM document"):
        for html in row[1:]:
            count(row[0], html)
    for document_id, content, mark in db.execute("SELECT document_id, content, classification_mark FROM witness"):
        count(document_id, content)
        count(document_id, mark)

    without_calls = []
    for note_id, document_id, occurences in db.execute("SELECT id, document_id, occurences FROM note").fetchall():
        actual = calls[document_id][note_id]
        if actual == 0:
            without_calls.append((note_id, document_id))
        elif actual != occurences:
            db.execute("UPDATE note SET occurences = ? WHERE id = ?", (actual, note_id))
            changes.append(f"note {note_id} (lettre {document_id}) : occurences {occurences} -> {actual}")
    return without_calls


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("database")
    parser.add_argument("--apply", action="store_true", help="écrire les modifications (sinon simulation)")
    args = parser.parse_args()

    db = sqlite3.connect(args.database)
    changes = []
    try:
        fix_letter_2(db, changes)
        fix_letter_3470(db, changes)
        without_calls = recount_occurrences(db, changes)
        print(f"{len(changes)} modification(s) :")
        for change in changes:
            print(f"  {change}")
        if without_calls:
            print(f"notes sans aucun appel (non modifiées) : {without_calls}")
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
