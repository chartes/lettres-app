# Fonctionnalités attendues

## Définition(s)
Un *document* = une lettre, éventuellement sur plusieurs pages (avec plusieurs images associées à feuilleter).

## Visualisation d'un document
Visualisation d'un document et de toutes les données associées (notamment les images, les notes de bas de page et les documents précédents/suivants)


## Création d'un document
* En fournissant uniquement les champs obligatoires (une transcription n’est pas requise au *CREATE*)
* En fournissant l'ensemble des données possibles pour un document

### Modification d'un document
* Modification des attributs (`title`, etc.)
* Ajout/Modification/Suppression des relations (`witnesses`, `correpondents-having-roles`, etc.)

### Contenu riche

Certains champs peuvent contenir du contenu semi-structuré (paragraphes, typo, appels de notes) :

|Champ|Description|
|-----|-----------|
|`Document["title"]`|Titre de la lettre|
|`Document["argument"]`|Analyse (résumé) de la lettre|
|`Document["transcription"]`|Transcription de la lettre|
|`Document["creation-label"]`|Date de rédaction de la lettre|
|`Witness["label"]`|Référence du témoin|
|`Witness["classification_mark"]`|Cote du témoin édité|
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

## Rôles utilisateur
Les rôles possibles sont :
* `admin` (administrateur)
  * tous les droits concernant tous les documents (création, modification, suppression)
  * modification des référentiels utilisés (langues, personnes, rôle des correspondants, institutions de conversation)
  * vérouillage et dévérouillage de tous les documents sans condition
  * invitation d'utilisateurs extérieurs à devenir contributeur ou administrateur
* `contributor` (contributeur)
  * lecture de tous les documents
  * modification de tout document non vérouillé par autrui
  * modification des référentiels utilisés (langues, personnes, rôle des correspondants, institutions de conversation)
  * vérouillage d'un document non vérouillé par autrui
  * dévérouillage d'un document dont on possède le vérrou
* utilisateur non identifié :
  * lecture seule de tous les documents

## Statut du document
Le statut du document (`publié` ou `non publié`) conditionne uniquement l'accès en lecture de ce dernier aux visiteurs : un document au statut `non publié` ne sera pas visible pour un utilisateur non connecté.

## Vérouillage du document
Indépendamment de son statut de publication, un document peut être vérouillé par un contributeur afin d'éviter toute modification concomitante de la part d'autres contributeurs. Autrement dit, un contributeur peut se réserver le droit de modifier un document pour une période donnée.

Un contributeur peut :
- vérouiller un document pour une période renouvelable de 7 jours
- dévérouiller un document qu'il a lui-même vérouillé avant la fin de la période de 7 jours
- voir quels sont les documents vérouillés, par qui et pourquoi (lorsque la raison a été indiquée)

Un administrateur peut vérouiller et déverouiller tous les documents à n'importe quel moment.

## Historique des changements

Un utilisateur connecté peut voir l'historique des objets modifiés (qui a modifié quoi et à quelle date). Un champ "description" permet à l'utilisateur apportant les modifications de se justifier.
Les anciennes versions ne sont pas sauvegardées et donc ne seront pas disponibles à la consultation.
