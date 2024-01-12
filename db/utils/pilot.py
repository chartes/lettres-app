import sqlite3
import xml2db
import os
#print('os.getcwd() :', os.getcwd())

db_path = os.getcwd() + '/lettres.dev.sqlite'
# TODO  ['203964.xml', '203965.xml', '203966.xml', '203967.xml', '6218232.xml', '6479798.xml']
# DONE  ['203964.xml', '203965.xml', '203966.xml', '203967.xml', '6218232.xml', '6479798.xml']
xml_files = ['6479798.xml']



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

