# -*- coding: utf-8 -*-
import sqlite3
import os
from lxml import etree
from lxml.etree import tostring
import io
import re
from more_itertools import unique_everseen

# Contrôler avant chargement (dans la src XML) la normalisation des witness : on autorise quoi ? cite, sup, ?
# Contrôler avant chargement (dans la src XML) l’enrichissement typo des creation_label


def insert_ref_data(db, cursor):
    """ Insertion des données de référence pour notre collection Catherine de Médicis """


    """
    try:
        cursor.execute(
            "INSERT INTO person ("
            "id,"
            "label,"
            "ref)"
            "VALUES (?, ?, ?)",
            (77,
            'Henri de Bourbon (1553-1610)',
            'https://www.wikidata.org/wiki/Q936976'))
    except sqlite3.IntegrityError as e:
        print(e)

    try:
        cursor.execute("INSERT INTO person_role (id, label, description) VALUES (?, ?, ?)",
                       (1, 'sender', 'Expéditeur de la lettre'))
    except sqlite3.IntegrityError as e:
        print(e)

    try:
        cursor.execute("INSERT INTO language (id, code, label) VALUES (1, 'fro', 'Ancien français')")
    except sqlite3.IntegrityError as e:
        print(e)
    """

    try:
        cursor.execute("INSERT INTO collection (id, parent_id, title, description) VALUES (?, ?, ?, ?)",
                       (3, None, 'Henri IV', 'Lettres de Henri IV'))
    except sqlite3.IntegrityError as e:
        print(e)

    db.commit()


def insert_letter(db, cursor, xml_file):
    """ insertion des lettres depuis le XML """

    # FAKE DATA, pour insertion test
    language_id = 1  # frm
    collection_id = 96  # Lettres de Henri IV suite
    correspondant_id = 77  # Henri IV
    correspondant_role_id = 1  # expéditeur

    files_dir = '../../../Documents/LettresDoc/Numérisations/'
    file = files_dir+xml_file
    files = [f for f in os.listdir(files_dir) if os.path.isfile(os.path.join(files_dir, f))]
    print('files : ', files)
    print('file : ', file)
    tree = etree.parse(file)
    #for node in tree.iter():
    #    print("node.tag: ", node.tag)
    print("tree : ", tree)
    ns = {"tei" : "http://www.tei-c.org/ns/1.0"}
    #bibl_test = tree.getroot().findall(ns+'teiHeader')
    #print("bibl_test :", bibl_test)
    # la référence du volume (on considère que cette réf est un temoin de type édition,
    # qu’on insérera juste avant les témoins
    #print("tree.xpath('TEI/teiHeader/fileDesc/sourceDesc/bibl', namespaces=ns) : ", tree.xpath('//tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl', namespaces=ns))
    bibl = tostring(tree.xpath('teiHeader/fileDesc/sourceDesc/bibl')[0], encoding='unicode')
    print('bibl1 :', bibl)
    bibl = re.sub('<(/?)title>', '<\\1cite>', bibl)
    bibl = re.sub('<ref target="([^"]+)">', '<a href="\\1">', bibl)
    bibl = bibl.replace('</ref>', '</a>')
    bibl = bibl[6:-14]
    print('bibl2 :', bibl)

    for div in tree.xpath('text/body/div'):
        letter = {}

        letter['id'] = div.get('id')

        letter['title'] = normalize_punctuation(tei2html(div.xpath('head')[0]))
        letter['title'] = letter['title'].rstrip('.')
        letter['function'] = normalize_punctuation(tei2html(div.xpath('head')[1]))

        # première page avant le début de la lettre, si le saut de page ne précède pas le tout début de celle-ci
        # on teste si la div commence par un pb
        first_el_name = div.xpath('name(*[1])')
        first_pb = div.xpath('pb[1]')[0] if (first_el_name == 'pb') else div.xpath('./preceding::pb[1]')[0]
        first_page_num = first_pb.get('n')
        first_page_iiif_url = first_page_url = first_pb.get('facs')
        first_page_url = first_page_url.split('/full')[0]
        first_page_url = first_page_url.replace('/iiif', '')
        letter['num_start_page'] = '<a href="'+first_page_url+'">p. '+first_page_num+'</a>'
        # référence biblio de l’édition, considérée comme un témoin de base, de type édition
        witness_ed = bibl[:-1]+', '+letter['num_start_page']+'.'

        # la liste des images
        images_iiif_url = []
        images_iiif_url.append(first_page_iiif_url)
        images_iiif_url.extend(div.xpath('.//pb/@facs'))
        # https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-whilst-preserving-order
        images_iiif_url = list(unique_everseen(images_iiif_url))

        # la liste des nœuds witness
        letter['witnesses'] = div.xpath('listWit/witness')
        letter['creation_label'] = normalize_punctuation(tei2html(div.xpath('dateline/date')[0]))
        letter['creation_label'] = letter['creation_label'].rstrip('.')
        letter['creation'] = div.xpath('dateline/date')[0].get('when')
        if letter['creation'] is None:
            letter['creation'] = div.xpath('dateline/date')[0].get('notBefore')
        letter['creation_not_after'] = div.xpath('dateline/date')[0].get('notAfter')

        letter['transcription'] = get_transcription_node(div.xpath('.')[0])
        letter['transcription'] = tei2html(letter['transcription'])
        letter['transcription'] = format_html(letter['transcription'])

        print('{letter} : ', letter)

        # INSERTIONS
        try:
            cursor.execute(
                "INSERT INTO document ("
                "title,"
                "creation,"
                "creation_not_after,"
                "creation_label,"
                "transcription,"
                "is_published,"
                "address)"
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (letter['title'],
                 letter['creation'],
                 letter['creation_not_after'],
                 letter['creation_label'],
                 letter['transcription'],
                 None,
                 letter['title']))
        except sqlite3.IntegrityError as e:
            print(e, "document, lettre %s" % (letter['id']))

        # Id de la dernière lettre insérée
        document_id = cursor.lastrowid


        # édition DIHF source considérée comme témoin de base
        try:
            cursor.execute("INSERT INTO witness (document_id, content, tradition, status) "
                           "VALUES (?, ?, ?, ?)",
                           (document_id, witness_ed, 'édition', 'base'))
        except sqlite3.IntegrityError as e:
            print(e, "sourceDoc witness, lettre %s" % (letter['id']))
        witness_id = cursor.lastrowid

        # on renseigne les URL des images de ce témoin de base
        for i, image_url in enumerate(images_iiif_url):
            i += 1
            image_url_part = image_url.split('/')
            canvas_id = '/'.join(image_url_part[:7]) + '/canvas/' + image_url_part[7]
            try:
                cursor.execute("INSERT INTO image (witness_id, canvas_id, order_num) VALUES (?, ?, ?)",
                               (witness_id, canvas_id, i))
            except sqlite3.IntegrityError as e:
                print(e, "image")

        # les témoins énumérés dans l’édition imprimée
        for i, witness in enumerate(letter['witnesses']):
            witness = tei2html(witness)
            witness = normalize_punctuation(witness.replace('\n', ' '))
            witness = witness.replace(', </cite>', '</cite>, ')
            # on considère que le premier est le témoin de base
            if i == 0:
                try:
                    cursor.execute("INSERT INTO witness (document_id, content, status, num) VALUES (?, ?, ?, ?)",
                                   (document_id, witness, 'base', 2))
                except sqlite3.IntegrityError as e:
                    print(e, "lettre %s" % (letter['id']))
            else:
                try:
                    cursor.execute("INSERT INTO witness (document_id, content, status, num) VALUES (?, ?, ?, ?)",
                                   (document_id, witness, 'autre', i+2))
                except sqlite3.IntegrityError as e:
                    print(e, "witness, lettre %s" % (letter['id']))

        try:
            cursor.execute("INSERT INTO document_has_language (document_id, language_id) VALUES (?, ?)",
                       (document_id, language_id))
        except sqlite3.IntegrityError as e:
            print(e, "document_has_language, lettre %s" % (letter['id']))

        try:
            cursor.execute(
                "INSERT INTO person_has_role (person_id, document_id, person_role_id)"
                "VALUES (?, ?, ?)",
                (correspondant_id, document_id, correspondant_role_id))
        except sqlite3.IntegrityError as e:
            print(e, "lettre %s" % (letter['id']))

        try:
            cursor.execute(
                "INSERT INTO document_has_collection (document_id, collection_id)"
                "VALUES (?, ?)",
                (document_id, collection_id))
        except sqlite3.IntegrityError as e:
            print(e, "document_has_collection, lettre %s" % (letter['id']))

        # notes // NB: des notes dans les notes ?
        note_refs = div.xpath('descendant::ref[@type="note"]')
        for note_ref in note_refs:
            note_xml_id = note_ref.get('target')[1:]
            note_content = tei2html(div.xpath('../../back/div[@type="notes"]/note[@id="'+note_xml_id+'"]')[0])
            note_content = format_html(note_content)
            # print(letter['id']+': '+note_content)
            try:
                cursor.execute("INSERT INTO note (content, document_id) VALUES (?, ?)",
                               (note_content, document_id))
            except sqlite3.IntegrityError as e:
                print(e, "note, lettre %s" % (letter['id']))

            # réécriture des liens aux notes
            note_id = str(cursor.lastrowid)
            try:
                cursor.execute('UPDATE document SET transcription = replace(transcription, ?, ?) WHERE id = ?',
                               (note_xml_id, note_id, document_id))
            except sqlite3.IntegrityError as e:
                print(e, "update notes in document transcription, lettre %s" % (letter['id']))
            try:
                cursor.execute('UPDATE document SET title = replace(title, ?, ?) WHERE id = ?',
                               (note_xml_id, note_id, document_id))
            except sqlite3.IntegrityError as e:
                print(e, "update notes in document title, lettre %s" % (letter['id']))
            try:
                cursor.execute('UPDATE document SET creation_label = replace(creation_label, ?, ?) WHERE id = ?',
                               (note_xml_id, note_id, document_id))
            except sqlite3.IntegrityError as e:
                print(e, "update notes in document creation_label, lettre %s" % (letter['id']))
            try:
                cursor.execute('UPDATE witness SET content = replace(content, ?, ?) WHERE document_id = ?',
                               (note_xml_id, note_id, document_id))
            except sqlite3.IntegrityError as e:
                print(e, "update notes in witness, lettre %s" % (letter['id']))

        db.commit()


def tei2html(tei_node):
    """ conversion HTML 5 de certains nœuds TEI / NB: finalement lourd de retourner du texte… """

    tei2html = io.StringIO('''\
        <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
            <xsl:output method="text"/>
            <xsl:template match="/">
                <xsl:apply-templates/>
            </xsl:template>
            <xsl:template match="p">
                <xsl:text>&lt;p></xsl:text>
                <xsl:apply-templates/>
                <xsl:text>&lt;/p></xsl:text>
            </xsl:template>
            <xsl:template match="hi[@rend='sup']">
                <xsl:text>&lt;sup></xsl:text>
                <xsl:apply-templates/>
                <xsl:text>&lt;/sup></xsl:text>
            </xsl:template>
            <xsl:template match="hi[@rend='sc']">
                <xsl:text>&lt;span class="sc"></xsl:text>
                <xsl:apply-templates/>
                <xsl:text>&lt;/span></xsl:text>
            </xsl:template>
            <xsl:template match="hi[@rend='i']">
                <xsl:text>&lt;i></xsl:text>
                <xsl:apply-templates/>
                <xsl:text>&lt;/i></xsl:text>
            </xsl:template>
            <xsl:template match="hi[@rend='i'][parent::witness]">
                <xsl:text>&lt;cite></xsl:text>
                <xsl:apply-templates/>
                <xsl:text>&lt;/cite></xsl:text>
            </xsl:template>
            <xsl:template match="lb">
                <xsl:text> </xsl:text>
            </xsl:template>
            <xsl:template match="pb">
                <xsl:text>&lt;a class="pb" href="</xsl:text>
                <xsl:value-of select="@facs"/>
                <xsl:text>">[p. </xsl:text>
                <xsl:value-of select="@n"/>
                <xsl:text>]&lt;/a> </xsl:text>
            </xsl:template>
            <xsl:template match="ref[@type='note']">
                <xsl:text>&lt;a class="note" href="</xsl:text>
                <xsl:value-of select="@target"/>
                <xsl:text>">[note]&lt;/a></xsl:text>
            </xsl:template>
        </xsl:stylesheet>''')
    xslt_tei2html = etree.parse(tei2html)
    transform_tei2html = etree.XSLT(xslt_tei2html)
    return str(transform_tei2html(tei_node))


def get_transcription_node(div):
    """ ramasser la seule transcription dans une div """

    get_transcription_node = io.StringIO('''\
            <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                <xsl:output method="xml"/>
                <xsl:template match="@*|node()">
                    <xsl:copy>
                        <xsl:apply-templates select="@*|node()"/>
                    </xsl:copy>
                </xsl:template>
                <xsl:template match="head|dateline|listWit"/>
            </xsl:stylesheet>''')
    xslt_get_transcription_node = etree.parse(get_transcription_node)
    transform_get_transcription_node = etree.XSLT(xslt_get_transcription_node)
    return transform_get_transcription_node(div)


def normalize_punctuation(string):
    """ normalisation de la ponctuation (française) et des espacements """

    # suppression de toutes les espaces (normales et insécables autour de la ponctuation)
    string = re.sub('[  ]*([.,(?;:!)])[  ]*', '\\1', string)
    # restauration de l’espace normale avant les parenthèses
    string = re.sub('(\()', ' \\1', string)
    # restauration des espaces avant/après la ponctuation double (insécable avant, simple après)
    string = re.sub('([?;:!])', ' \\1 ', string)
    # restauration de l’espace normale après la ponctuation simple
    string = re.sub('([.,)])', '\\1 ', string)
    # très moche : problème de la ponctuation dans les listes abréviées
    string = string.replace('. ,', '.,')
    # suppression des espaces multiples (espaces simples, insécables et tab)
    string = re.sub('[  \t]{2,}', ' ', string)
    # ceinture bretelles, on trime
    string = string.strip()
    return string


def format_html(html_string):
    # suppression des lignes vides
    html_string = re.sub('^[  \t ]*\n', '', html_string, flags=re.M)
    # suppression des indentations issues du XML
    html_string = re.sub('^[  \t ]+', '', html_string, flags=re.M)
    # suppression des éventuelles espaces en fin de ligne
    html_string = re.sub('[  \t ]+$', '', html_string, flags=re.M)
    return html_string
