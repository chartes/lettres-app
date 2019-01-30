/*
 Note
 Blot : embed
 Utilisation : Appel de note
*/

import Parchment from 'parchment';

class NoteBlot extends Parchment.Embed {
  static create(value) {
    let node = super.create();
    return node;
  }

}
NoteBlot.blotName = 'note';
NoteBlot.tagName = 'a';
NoteBlot.className = 'note';

export default NoteBlot;
