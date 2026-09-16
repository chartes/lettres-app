"""Ajoute target="_blank" aux liens externes des citations de témoins (witness.content).

Les liens importés ont la forme <a href="https://gallica.bnf.fr/..."> sans target,
alors que l'éditeur (blot Quill Link) crée des liens avec target="_blank".
Les ancres internes (href="#...") et les liens ayant déjà un target ne sont pas modifiés.

Usage (depuis lettres-app) :
    python db/utils/witness_links_target_blank.py db/lettres.local.sqlite            # simulation
    python db/utils/witness_links_target_blank.py db/lettres.local.sqlite --apply    # écriture
"""
import argparse
import re
import sqlite3

# balise <a> avec un href externe et sans attribut target
LINK_WITHOUT_TARGET = re.compile(r'<a(?![^>]*\btarget\s*=)([^>]*\bhref\s*=\s*"https?://[^"]*"[^>]*)>', re.I)


def add_target_blank(content):
    return LINK_WITHOUT_TARGET.subn(r'<a\1 target="_blank">', content)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("database")
    parser.add_argument("--apply", action="store_true", help="écrire les modifications (sinon simulation)")
    args = parser.parse_args()

    db = sqlite3.connect(args.database)
    rows = db.execute("SELECT id, document_id, content FROM witness WHERE content LIKE '%href%'").fetchall()

    updates, links, documents = [], 0, set()
    for witness_id, document_id, content in rows:
        new_content, count = add_target_blank(content)
        if count:
            updates.append((new_content, witness_id))
            links += count
            documents.add(document_id)

    print(f"témoins à corriger : {len(updates)} | liens : {links} | lettres : {len(documents)}")
    for new_content, witness_id in updates[:3]:
        print(f"  témoin {witness_id} : {new_content[:160]}")

    if args.apply:
        with db:
            db.executemany("UPDATE witness SET content = ? WHERE id = ?", updates)
        print("modifications enregistrées")
    else:
        print("simulation : rien n'a été écrit (ajouter --apply pour enregistrer)")
    db.close()


if __name__ == "__main__":
    main()
