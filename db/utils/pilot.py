import sqlite3
import xml2db
import os
#print('os.getcwd() :', os.getcwd())

db_path = os.getcwd() + '/db/lettres.dev.sqlite'

# TODO  ['203964.xml', '203965.xml', '203966.xml', '203967.xml', '6218232.xml', '6479798.xml']
# DONE supplément HENRI IV ['203964.xml', '203965.xml', '203966.xml', '203967.xml', '6218232.xml', '6479798.xml']
# DONE supplément Catherine ['3202184.xml', '3202400.xml']
xml_files = ['3202400.xml']


print("Vérifier le chemin relatif de la base: ", f'{os.path.abspath(db_path)}')

db = sqlite3.connect(db_path)
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys=ON')

# déjà en base, id 77
# xml2db.insert_ref_data(db, cursor)
# xml2db.insert_letter(db, cursor, xml_file_name)
for xml_file in xml_files:
    print("traitement de "+xml_file)
    xml2db.insert_letter(db, cursor, xml_file)

db.close()

