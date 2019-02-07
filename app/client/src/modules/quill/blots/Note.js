/*
 Note
 Blot : embed
 Utilisation : Appel de note
*/

import Parchment from 'parchment';

class NoteBlot extends Parchment.Embed {

  static create(value) {
    let node = super.create();
    node.setAttribute('href', '#'+value);
    node.innerText = '[note]'
    return node;
  }

  static formats(domNode) {
    return { note: domNode.getAttribute('href').substring(1) }
  }

  static value(domNode) {
    return domNode.getAttribute('href').substring(1)
  }

  format(name, value) {
    if (name === 'note' && value) {
      this.domNode.setAttribute('href', '#' + value);
    } else {
      super.format(name, value);
    }
  }

}
NoteBlot.blotName = 'note';
NoteBlot.tagName = 'a';
NoteBlot.className = 'note';

export default NoteBlot;
