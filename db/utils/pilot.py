import sqlite3
import xml2db


db_path = '../lettres-dev.sqlite'
xml_file_name = '6227926.xml'

db = sqlite3.connect(db_path)
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys=ON')

xml2db.insert_ref_data(db, cursor)
xml2db.insert_letter(db, cursor, xml_file_name)

db.close()

