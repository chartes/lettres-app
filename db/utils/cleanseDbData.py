import sqlite3
import os
import re
from collections import Counter
from lxml import html
print('os.getcwd() :', os.getcwd())

db_path = os.getcwd() + '/db/lettres.dev_forProd.sqlite'
print('db_path : ', db_path)
#  ['203961.xml', '203962.xml', '203963.xml']
# xml_files = ['203964_test_withBibl_withoutNS.xml']


db = sqlite3.connect(db_path)
cursor = db.cursor()
cursor.execute('PRAGMA foreign_keys=ON')


param = 'class="note"'
t = '%'+param+'%'

cursor.execute("SELECT note.id FROM note GROUP BY note.id HAVING COUNT(note.id) > 1")
notesAccrossDocs = cursor.fetchall()
print("notesAccrossDocs db : ", notesAccrossDocs)

cursor.execute("SELECT id, content, document_id \
FROM witness \
WHERE content LIKE '%' || ? || '%'", (t,))
witnessResults = [[item for item in result] for result in cursor.fetchall()]
print("witnessResults[0] : ", witnessResults[0])
print("len(witnessResults) : ", len(witnessResults))


cursor.execute("SELECT document.id, document.title, document.argument, document.transcription, document.address \
FROM document \
WHERE transcription LIKE '%' || ? || '%' OR argument LIKE '%' || ? || '%' OR address LIKE '%' || ? || '%' OR title LIKE '%' || ? || '%'", (t, t, t, t))
results = cursor.fetchall()
print("len(results) : ", len(results))
print(results[0])
notePattern = re.compile('<a class="note" href="#(\d+)">[^<]*</a>')

for w in witnessResults:
    #print("w[1]", w[1])
    noteIDsearch = re.search(notePattern, w[1])
    w[1] = int(noteIDsearch.group(1))
#print("witnessResults : ", witnessResults)

notes_occurences_docId = []
for res in results:
    #print("res[0], res[1] :", res[0], res[1])
    fieldset = [res[1], res[2], res[3], res[4]]
    if len(re.findall(notePattern, ' '.join(str(item) for item in fieldset))) > 0:
        counts = dict(Counter([x.group() for x in re.finditer(notePattern, ' '.join(str(item) for item in fieldset))]))
        notes_occurences_docId.append([res[0], [re.findall(notePattern, key)[0] for key, value in counts.items()]])
        notes_occurences = {re.findall(notePattern, key)[0]: value for key, value in counts.items()}
        #print("notes_occurences : ", notes_occurences)
        for key, value in notes_occurences.items():
            inWitness = [x for x in witnessResults if x[2] == res[0] and x[1] == int(key)]
            if len(inWitness):
                print("la note " + key + " existe aussi dans le(s) témoin(s) " + str([str(w[0]) for w in inWitness]))
            #print("key, value", key, value)
            cursor.execute("SELECT note.document_id, note.id, note.occurences FROM note WHERE note.id = ?", (key,))
            query = cursor.fetchone()
            #print("query", len(query))
            if not query:
                #print("query", query)
                print(str(value) +" note(s) dans le doc " + str(res[0]) + " pour la note " + str(key) + " mais pas en base")
            else:
                #print("query", query)
                noteDB = query
                #print("noteDB", noteDB)
                if noteDB[2] != value + len(inWitness):
                    if noteDB[0] != res[0]:
                        print("erreur de doc :  la note " + str(
                            noteDB[1]) + " appartient au document " + str(noteDB[0]) + " et pas au doc  " + str(res[0]))
                    else:
                        print("erreur d'occurences sur le doc " + str(res[0]) + " pour la note " + str(noteDB[1]) + ": DB occurences = " + str(noteDB[2]) + " vs. fields = " + str(value + len(inWitness)) + " (dans doc : " + str(value) + " / témoins : " + str(len(inWitness)) + ")")
                        '''try:
                            cursor.execute(
                                "UPDATE note SET occurences = ? WHERE note.id = ?",
                                (value, key))
                            db.commit()
                        except:
                            print("error updating")
                            db.rollback()'''

        #notes_occurences_docId.append({"docId": res[0], "notes_occurences": notes_occurences})

        '''if len(notes_occurences) > 0:
            print("liste de notes", res[0], re.findall(notePattern, ' '.join(str(item) for item in fieldset)), notes_occurences)
    tree = html.fromstring(res[1])
    for item in tree.xpath("//a[@class='note']"):
        pattern = re.compile('</?span>')
        print("\nres[0], item : \n", res[0], item.attrib['href'], re.sub(pattern, '', str(html.tostring(item, with_tail=False)).replace('&#65279;', '')), item.text_content())'''

dupesAcrossDocuments = []
for i, doc in enumerate(notes_occurences_docId, 5):
    for note in doc[1]:
        #print("doc[0] doc[1] / note", doc[0], doc[1], note)
        for row in notes_occurences_docId[i+1:]:
            if note in row[1]:
                #print("docId1, note, docId2, row[1]", doc[0], note, row[0], row[1])
                dupesAcrossDocuments.append(doc)
print("dupesAcrossDocuments (fields data) : ", dupesAcrossDocuments)


param = 'class="persName"'
p = '%'+param+'%'
cursor.execute("SELECT document.id, document.title, document.argument, document.transcription, document.address \
FROM document \
WHERE transcription LIKE '%' || ? || '%' OR argument LIKE '%' || ? || '%' OR address LIKE '%' || ? || '%' OR title LIKE '%' || ? || '%'", (p, p, p, p))
persNameResults = cursor.fetchall()
persPattern = re.compile('<a class="persName" [^<]*>[^<]*</a>')
print("\n len(persNameResults)", len(persNameResults))
for res in persNameResults[:10]:
    print("\n title", res[0], re.findall(persPattern, res[1]))
    print("\n argument", res[0], re.findall(persPattern, res[2]) if res[2] else 'Null')
    print("\n transcription", res[0], re.findall(persPattern, res[3]))
    print("\n address", res[0], re.findall(persPattern, res[4]) if res[4] else 'Null')

persIDnotinDB = []
persID = re.compile('id="(d+)"')
for res in persNameResults:
    print("\nres[0] :", res[0])
    res_fieldset = [res[1], res[2], res[3], res[4]]
    res_persnames = re.findall(persPattern, ' '.join(str(item) for item in res_fieldset))
    res_persIds = re.findall('id="(\d+)"', ' '.join(str(item) for item in res_persnames))
    #print("res_persnames : ", res_persnames)
    #print("res_persnames join : ", ' '.join(str(item) for item in res_persnames))
    #print("persName res ids : ", re.findall('id="(\d+)"', ' '.join(str(item) for item in res_persnames)) if len(res_persnames)>0 else 'None')
    print("res_persIds", res_persIds)
    if len(res_persIds) == 1:
        cursor.execute("SELECT COUNT(*) from person where id = %s" % res_persIds[0])
        (number_of_rows,) = cursor.fetchone()
        if number_of_rows == 0:
            persIDnotinDB.append((res[0], res_persIds[0]))
    elif len(res_persIds) > 1:
        for id in res_persIds:
            cursor.execute("SELECT COUNT(*) from person where id = %s" % id)
            (number_of_rows,) = cursor.fetchone()
            if number_of_rows == 0:
                persIDnotinDB.append((res[0], id))

print("persIDnotinDB", persIDnotinDB)
for error in persIDnotinDB:
    cursor.execute("SELECT document.transcription \
    FROM document \
    WHERE id= %s" % error[0])
    (transcription,) = cursor.fetchone()
    #print("transcription", transcription)
    persErrorPattern = re.compile('<a class="persName" id="%s">([^<]*)</a>' % error[1])
    persErrorsTag = [x.group() for x in re.finditer(persErrorPattern, transcription)]
    persErrorsContent = re.findall(persErrorPattern, transcription)
    print("persErrorPattern", persErrorPattern)
    print("test", re.findall(persErrorPattern, transcription))
    print("test2", [x.group() for x in re.finditer(persErrorPattern, transcription)])
    if error[1] == '13':
        updated_transcription = transcription
        for index, tobeReplaced in enumerate(persErrorsTag):
            updated_transcription = updated_transcription.replace(tobeReplaced, '<a class="persName" target="_blank" href="https://www.wikidata.org/entity/Q53448" title="Henri III (1551-1589)" id="122">' + persErrorsContent[index].strip() + '</a>')
            print("updated_transcription", updated_transcription)
        if error[0] == 745:
            cursor.execute("""UPDATE document
                SET transcription = %(updated_transcription)s
                WHERE id = %(id)s""", {'updated_transcription': updated_transcription, 'id': error[0]})

param = 'class="placeName"'
p = '%'+param+'%'
cursor.execute("SELECT document.id, document.title, document.argument, document.transcription, document.address \
FROM document \
WHERE transcription LIKE '%' || ? || '%' OR argument LIKE '%' || ? || '%' OR address LIKE '%' || ? || '%' OR title LIKE '%' || ? || '%'", (p, p, p, p))
PlaceNameResults = cursor.fetchall()
placePattern = re.compile('<a class="placeName" [^<]*>[^<]*</a>')
print("\n len(PlaceNameResults)", len(PlaceNameResults))
#for res in PlaceNameResults[:10]:
    #print("\n title", res[0], re.findall(placePattern, res[1]))
    #print("\n argument", res[0], re.findall(placePattern, res[2]) if res[2] else 'Null')
    #print("\n transcription", res[0], re.findall(placePattern, res[3]))
    #print("\n address", res[0], re.findall(placePattern, res[4]) if res[4] else 'Null')

placeIDnotinDB = []
placeID = re.compile('id="(d+)"')
for res in PlaceNameResults:
    #print("\nres[0] :", res[0])
    res_fieldset = [res[1], res[2], res[3], res[4]]
    res_placenames = re.findall(placePattern, ' '.join(str(item) for item in res_fieldset))
    res_placeIds = re.findall('id="(\d+)"', ' '.join(str(item) for item in res_placenames))
    #print("res_placenames : ", res_placenames)
    #print("res_placenames join : ", ' '.join(str(item) for item in res_placenames))
    #print("placename res ids : ", re.findall('id="(\d+)"', ' '.join(str(item) for item in res_placenames)) if len(res_placenames)>0 else 'None')
    #print("res_placeIds", res_placeIds)
    if len(res_placeIds) == 1:
        cursor.execute("SELECT COUNT(*) from placename where id = %s" % res_placeIds[0])
        (number_of_rows,) = cursor.fetchone()
        if number_of_rows == 0:
            placeIDnotinDB.append((res[0], res_placeIds[0]))
    elif len(res_placeIds) > 1:
        for id in res_placeIds:
            cursor.execute("SELECT COUNT(*) from placename where id = %s" % id)
            (number_of_rows,) = cursor.fetchone()
            if number_of_rows == 0:
                placeIDnotinDB.append((res[0], id))

print("placeIDnotinDB", placeIDnotinDB)

db.close()
