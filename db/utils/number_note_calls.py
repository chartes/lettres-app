"""Écrit en base le numéro des appels de notes.

Le front remplace à l'affichage "[note]" par la position de la note dans la liste des notes
de la lettre (getNoteIndex, "TODO remove once [note] have been replaced in database").
Ce script écrit ce même numéro en base, en retirant les <span> et les caractères U+FEFF
qui entourent parfois le libellé :
    <a class="note" href="#4820"><span>[note]</span></a>  ->  <a class="note" href="#4820">[1]</a>
Les appels déjà numérotés dont le numéro ne correspond pas à la position de la note
sont renumérotés.

Champs traités : titre, analyse, transcription, adresse de la lettre, contenu et cote des témoins.
Le script peut être relancé.

Usage (depuis lettres-app) :
    python3 db/utils/number_note_calls.py db/lettres.staging.sqlite            # simulation
    python3 db/utils/number_note_calls.py db/lettres.staging.sqlite --apply    # écriture
"""
import argparse
import sqlite3
import re

TABLES = {
    "document": ("id", ("title", "argument", "transcription", "address")),
    "witness": ("document_id", ("content", "classification_mark")),
}
NOTE_CALL = re.compile(r'<a class="note" href="#(\d+)">(?:\uFEFF|</?span>)*\[(note|\d+)\](?:\uFEFF|</?span>)*</a>', re.I)


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

    updated_rows = {table: 0 for table in TABLES}
    numbered = {table: 0 for table in TABLES}
    examples = {table: [] for table in TABLES}
    renumbered, unknown = [], []
    try:
        for table, (document_column, fields) in TABLES.items():
            for row in db.execute(f"SELECT id, {document_column}, {', '.join(fields)} FROM {table}").fetchall():
                row_id, document_id, updates = row[0], row[1], {}
                for field, html in zip(fields, row[2:]):
                    if not html:
                        continue
                    where = f"lettre {document_id}, {field}" if table == "document" else f"lettre {document_id}, témoin {row_id}, {field}"

                    def number(match):
                        note_id, label = int(match.group(1)), match.group(2)
                        index = positions.get(document_id, {}).get(note_id)
                        if index is None:
                            unknown.append(f"{where}, note {note_id}")
                            return match.group(0)
                        call = f'<a class="note" href="#{note_id}">[{index}]</a>'
                        if call != match.group(0):
                            if label.lower() == "note":
                                numbered[table] += 1
                            else:
                                renumbered.append(f"{where}, note {note_id} : [{label}] -> [{index}]")
                        return call

                    new_html = NOTE_CALL.sub(number, html)
                    if new_html != html:
                        updates[field] = new_html
                        if len(examples[table]) < 3:
                            i = new_html.index('class="note"')
                            examples[table].append(f"{where} : ...{new_html[max(0, i - 50):i + 40]}")
                if updates:
                    updated_rows[table] += 1
                    assignments = ", ".join(f"{field} = ?" for field in updates)
                    db.execute(f"UPDATE {table} SET {assignments} WHERE id = ?", (*updates.values(), row_id))

        print(f"lettres : {numbered['document']} appel(s) [note] numéroté(s) dans {updated_rows['document']} lettre(s)")
        print(f"témoins : {numbered['witness']} appel(s) [note] numéroté(s) dans {updated_rows['witness']} témoin(s)")
        print(f"{len(renumbered)} appel(s) mal numéroté(s) corrigé(s)")
        for change in renumbered:
            print(f"  {change}")
        print("exemples :")
        for example in examples["document"] + examples["witness"]:
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
