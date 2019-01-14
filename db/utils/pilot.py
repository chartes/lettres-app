import sqlite3
import xml2db


db_path = '../lettres-dev.sqlite'
xml_file_name = '6227983.xml'
xml_files = ['6227983.xml', '6227926.xml', '6227988.xml', '6227994.xml', '6227997.xml', '6228018.xml', '6228047.xml', '6228061.xml']

db = sqlite3.connect(db_path)
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys=ON')

xml2db.insert_ref_data(db, cursor)
# xml2db.insert_letter(db, cursor, xml_file_name)
for xml_file in xml_files:
    print("traitement de "+xml_file)
    xml2db.insert_letter(db, cursor, xml_file)

db.close()

