# Fonctionnalités

## Définitions

### Document
Un *document* = une lettre, transcription de 1 à n images (à feuilleter).

### Visualisation d'un document
Visualisation d'un document et de toutes les données associées (notamment les témoins, les images, les notes de bas de page et les documents précédents/suivants)


### Création d'un document
* En fournissant uniquement les champs obligatoires (title, witness ?, sender ?, creation ?)
* En fournissant l'ensemble des données possibles pour un document

TODO à revoir avec OP : quels sont les champs nécessaires à la création d’un nouveau document ? Autrement dit, quelles sont les métadonnées obligatoires pour son identification ?

### Modification d'un document
* Modification des attributs (`title`, etc.)
* Ajout/Modification/Suppression des relations (`witnesses`, `correpondents-having-roles`, etc.)

## Contenu riche

Certains champs peuvent contenir du contenu semi-structuré.

### Types d’enrichissements

|Classe|Enrichissement|HTML5|Exemple|
|------|--------------|-----|-------|
|structure|paragraphe|`p`|`<p>…</p>`|
|structure|saut de page|`a`|`<a class="pb" href="https://gallica.bnf.fr/ark:/12148/bpt6k6227983s/f61">[p. 15]</a>`|
|stucture|appel de note|`a`|`<a class="note" href="#76">[note]</a>`|
|typographie|italique|`i`|`<i>…</i>`|
|typographie|gras|`b`|`<b>…</b>`|
|typographie|exposant|`sup`|`<sup>…</sup>`|
|typographie|sous-ligné|`u`|`<u>…</u>`|
|sémantique|suppression|`del`|`<del>…</del>`|
|sémantique|personne|`a`|`<a class="persName" href="url">…</a>`|
|sémantique|lieu|`a`|`<a class="placeName" href="url">…</a>`|


### Éditeurs

|Champ|Description|Classe(s)|
|-----|-----------|------|
|`Document["title"]`|Titre de la lettre||
|`Document["argument"]`|Analyse (résumé) de la lettre||
|`Document["transcription"]`|Transcription de la lettre||
|`Document["creation-label"]`|Date de rédaction de la lettre||
|`Witness["label"]`|Référence du témoin||
|`Witness["classification_mark"]`|Cote du témoin édité||
|`Note["content"]`|Des notes (commentaires)||


## Correspondants

* Un correspondant a un et un seul rôle au sein d'un même document.
* Un correspondant peut être associé à un ou plusieurs documents.

Il doit être possible de modifier ces informations (changer le rôle d'un correspondant au sein d'un document, en ajouter, en modifier, en supprimer).

## Rôles utilisateur

### `admin` (administrateur)
* tous les droits  (création, modification, suppression, (dé)publication) sur tous les documents
* vérouillage et dévérouillage de tous les documents
* tous les droits (création, modification, suppression) sur toutes les collections
* tous les droits  (création, modification, suppression) sur tous les entités des référentiels (langues, personnes, rôle des correspondants, institutions de conversation)
* invitation d'utilisateurs extérieurs à devenir contributeur ou administrateur

### `contributor` (contributeur)
* lecture de tous les documents
* modification de tout document non vérouillé par autrui (dont (dé)publication et association à une ou plusieurs collections)
* modification des référentiels utilisés (langues, personnes, rôle des correspondants, institutions de conversation)
* vérouillage d'un document non vérouillé par autrui
* dévérouillage d'un document dont on possède le vérrou

### utilisateur non identifié
  * lecture seule de tous les documents publiés

## Statut du document
Le statut du document (`publié` ou `non publié`) conditionne uniquement l'accès en lecture de ce dernier aux visiteurs : un document au statut `non publié` ne sera pas visible pour un utilisateur non connecté.

## Vérouillage du document
Indépendamment de son statut de publication, un document peut être vérouillé par un contributeur afin d'éviter toute modification concomitante de la part d'autres contributeurs. Autrement dit, un contributeur peut se réserver le droit de modifier un document pour une période donnée.

Un contributeur peut :
- vérouiller un document pour une période renouvelable de 7 jours
- dévérouiller un document qu'il a lui-même vérouillé avant la fin de la période de 7 jours
- voir quels sont les documents vérouillés, par qui et pourquoi (lorsque la raison a été indiquée)

Un administrateur peut vérouiller et déverouiller tous les documents à n'importe quel moment.

**Un document publié est dévérouillé**.

## Historique des changements

Un utilisateur connecté peut voir l'historique des objets modifiés (qui a modifié quoi et à quelle date). Un champ "description" permet à l'utilisateur apportant les modifications de se justifier.
Les anciennes versions ne sont pas sauvegardées et donc ne seront pas disponibles à la consultation.
