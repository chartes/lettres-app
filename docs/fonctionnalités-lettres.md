# Fonctionnalités attendues

## Définition(s)
Un *document* = une lettre, éventuellement sur plusieurs pages (avec plusieurs images associées à feuilleter).

## Visualisation d'un document
Visualisation d'un document et de toutes les données associées (notamment les images, les notes de bas de page et les documents précédents/suivants)

![consultation, visu](https://github.com/chartes/lettres-app/blob/master/mockup/visu.png)

## Création d'un document
* En fournissant uniquement les champs obligatoires (une transcription n’est pas requise au *CREATE*)
* En fournissant l'ensemble des données possibles pour un document

### Modification d'un document
* Modification des attributs (`title`, `witnesss_label`, etc.)
* Ajout/Modification/Suppression des relations (`images`, `tradition`, `correpondents-having-roles`, etc.)

### Listes fermées, TBD
* Les listes fermées (vocabulaires) : langue, tradition
* Ces listes sont éditables uniquement par les `admin` (cf plus bas, *User roles*).


### Contenu riche

Certains champs peuvent contenir du contenu semi-structuré (paragraphes, typo, appels de notes) :

|Champ|Description|
|-----|-----------|
|`Document["title"]`|Titre de la lettre|
|`Document["witness_label"]`|Référence du témoin|
|`Document["classification_mark"]`|Cote du témoin édité|
|`Document["argument"]`|Analyse (résumé) de la lettre|
|`Document["transcription"]`|Transcription de la lettre|
|`Document["creation-label"]`|Date de rédaction de la lettre|
|`Note["content"]`|Des notes (commentaires)|

#### Enrichissement attendus
* italique, sous-ligné, gras, exposant
* paragraphe
* appel de notes (type point: `"…blah blah<ref target="#link_to_note/> blah blah…"`)
* annotation sémantique : personnes et lieu (type segment: `"…écrit à <persName ref="uri_to_julien">Julien</persName> que…"`)

## Correspondants

* Un correspondant a un et un seul rôle au sein d'un même document.
* Un correspondant peut apparaître dans un ou plusieurs documents.

Il doit être possible de modifier ces informations (changer le rôle d'un correspondant au sein d'un document, en ajouter, en modifier, en supprimer).

## Correspondants roles
* Un correspondant est soit `sender` soit `recipient`.
* Seuls les `admin` peuvent éditer est ajouter de nouveaux rôles.

## Images
Les images seront accessibles via le numéro de canvas  `Image["canvas-idx"]` du **manifeste IIIF** disponible à l'adresse `Image["manifest-url"]`.  
Un rebond (lien ou appel à un webservice) vers une autre application web permettra dans le futur d'upload de nouveaux manifestes.

Lors de la création d'un document une boite de dialogue doit permettre de choisir **un ou plusieurs canvas d'un ou plusieurs manifestes** afin de les associer au document.

Il doit être possible de modifier ou de supprimer ces informations.  
Un document peut n'être lié à aucune image à un moment donné de son existence.

## Notes
Les notes sont liées à un et un seul document
Il doit être possible de modifier ou de supprimer une note.

## User roles
Les rôles possibles (liste fermée) sont :
* `admin`(administrateur)
  * création d’un document.
  * édition des *whitelists* : attribution d’une transcription à un tous les, un seul, ou aucun contributeur(s).
  * modification, suppression de tous les documents et de tous leurs attributs.
* `contributor` (contributeur)
  * modification de tous les documents si la *whitelist* associée l’autorise.
  * modification de la *whitelist* UNIQUEMENT pour s’auto-attribuer un document en modification (et empêcher la modification par d’autres `contributors`, cf plus bas, *Whitelists*).
* `visitor` (utilisateur non identifié)
  * lecture seule (aucun droit en modification).

## Users
La création/modification/suppression des utilisateurs sera gérée
par un plugin Flask.


## Whitelists
Les whitelists donnent le droit d'écriture aux documents aux utilisateurs qui y sont mentionnés.
* Par défaut un document est ouvert en écriture à tous (tous les `admin` et tous les `contributor`)
* Les admin peuvent éditer TOUS les documents (par défaut toujours inscrits à toutes les *whitelists*).
* Un `contributor` peut s’attribuer l’édition d’un document (s’inscrire dans la whitelist associée au doc et rester le SEUL `contributor` inscrit dans la liste).
* Un `admin` peut retirer l’unique `contributor` d’une *whitelist*.

Les *whitelists* doivent pouvoir être crées, modifiées et supprimées.  
Un document sans *whitelist* est modifiable par tous.

# Moteur de recherche
L'appel au service de recherche (coming soon) devra permettre de peupler dynamiquement les listes de saisie  quand cela s'avère utile (ex: recherche d'un correspondant par son nom)
