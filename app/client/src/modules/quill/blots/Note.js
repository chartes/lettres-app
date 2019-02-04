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
    console.log('NoteBlot.formats', domNode.getAttribute('href'))
    return { note: domNode.getAttribute('href').substring(1) }
  }

  static value(domNode) {
    console.log('note value', domNode.getAttribute('href').substring(1))
    return domNode.getAttribute('href').substring(1)
  }

  format(name, value) {
    console.log('note format', name, value)
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
