# -*- coding: utf-8 -*-
import sqlite3
from lxml import etree
import io
import re

# Contrôler avant chargement (dans la src XML) la normalisation des witness : on autorise quoi ? cite, sup, ?
# Contrôler avant chargement (dans la src XML) l’enrichissement typo des creation_label


def insert_ref_data(db, cursor):
    """ Insertion des données de référence pour notre collection Catherine de Médicis """

    try:
        cursor.execute(
            "INSERT INTO correspondent ("
            "id,"
            "firstname,"
            "lastname,"
            "key,"
            "ref)"
            "VALUES (?, ?, ?, ?, ?)",
            (1,
            'Catherine',
            'de Médicis',
            'Catherine de Médicis (reine de France ; 1519-1589)',
            'https://data.bnf.fr/ark:/12148/cb123351707'))
    except sqlite3.IntegrityError as e:
        print(e)

    try:
        cursor.execute("INSERT INTO correspondent_role (id, label, description) VALUES (?, ?, ?)",
                       (1, 'sender', 'Expéditeur de la lettre'))
    except sqlite3.IntegrityError as e:
        print(e)

    try:
        cursor.execute("INSERT INTO collection (id, title, description) VALUES (?, ?, ?)",
                       (1, 'Catherine de Médicis', 'Lettres de Catherine de Médicis'))
    except sqlite3.IntegrityError as e:
        print(e)

    db.commit()


def insert_letter(db, cursor, xml_file):
    """ insertion des lettres depuis le XML """

    # FAKE DATA, pour insertion test
    owner_id = 2
    language_id = 1 # frm
    collection_id = 1 # Lettres de Catherine de Medicis
    correspondant_id = 1 # Catherine de Médicis
    correspondant_role_id = 1  # expéditeur


    file = '../../../lettres/src/'+xml_file
    tree = etree.parse(file)
    for div in tree.xpath('/TEI/text/body/div'):
        letter = {}

        letter['id'] = div.get('id')

        letter['title'] = normalize_punctuation(tei2html(div.xpath('head')[0]))
        letter['title'] = letter['title'].rstrip('.')

        letter['witness_label'] = tei2html(div.xpath('listWit/witness')[0])
        # suppression des sauts de ligne + normalisation de la ponctuation
        letter['witness_label'] = normalize_punctuation(letter['witness_label'].replace('\n', ' '))
        # moche, corriger les erreurs de segmentation dans la source, jetable
        letter['witness_label'] = letter['witness_label'].replace(', </cite>', '</cite>, ')

        letter['creation'] = div.xpath('dateline/date')[0].get('when')
        letter['creation_label'] = normalize_punctuation(tei2html(div.xpath('dateline/date')[0]))
        letter['creation_label'] = letter['creation_label'].rstrip('.')

        letter['transcription'] = get_transcription_node(div.xpath('.')[0])
        letter['transcription'] = tei2html(letter['transcription'])
        letter['transcription'] = format_html(letter['transcription'])
        #print(letter['transcription'])

        # INSERTIONS
        try:
            cursor.execute(
                "INSERT INTO document ("
                "title,"
                "witness_label,"
                "creation,"
                "creation_label,"
                "transcription,"
                "owner_id)"
                "VALUES (?, ?, ?, ?, ?, ?)",
                (letter['title'],
                 letter['witness_label'],
                 letter['creation'],
                 letter['creation_label'],
                 letter['transcription'],
                 owner_id))
        except sqlite3.IntegrityError as e:
            print(e, "lettre %s" % (letter['id']))

        # Id de la dernière lettre insérée
        document_id = cursor.lastrowid

        try:
            cursor.execute("INSERT INTO document_has_language (document_id, language_id) VALUES (?, ?)",
                       (document_id, language_id))
        except sqlite3.IntegrityError as e:
            print(e, "lettre %s" % (letter['id']))

        try:
            cursor.execute(
                "INSERT INTO correspondent_has_role (correspondent_id, document_id, correspondent_role_id)"
                "VALUES (?, ?, ?)",
                (correspondant_id, document_id, correspondant_role_id))
        except sqlite3.IntegrityError as e:
            print(e, "lettre %s" % (letter['id']))

        try:
            cursor.execute("INSERT INTO document_has_collection (document_id, collection_id) VALUES (?, ?)",
                           (document_id, collection_id))
        except sqlite3.IntegrityError as e:
            print(e, "lettre %s" % (letter['id']))

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
                print(e, "lettre %s" % (letter['id']))

            note_id = str(cursor.lastrowid)
            try:
                cursor.execute('UPDATE document SET transcription = replace(transcription, ?, ?) WHERE id = ?',
                               (note_xml_id, note_id, document_id))
            except sqlite3.IntegrityError as e:
                print(e, "lettre %s" % (letter['id']))

        db.commit()


def tei2html(tei_node):
    """ conversion HTML 5 de certains nœeuds TEI / NB: finalement lourd de retourner du texte… """

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
                <xsl:text>&lt;a href="</xsl:text>
                <xsl:value-of select="@facs"/>
                <xsl:text>">[p. </xsl:text>
                <xsl:value-of select="@n"/>
                <xsl:text>]&lt;/a> </xsl:text>
            </xsl:template>
            <xsl:template match="ref[@type='note']">
                <xsl:text>&lt;a href="</xsl:text>
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
