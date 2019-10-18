/*
 Note
 Blot : embed
 Utilisation : Appel de note
*/

import Parchment from 'parchment';
//import Quill from 'quill/quill';

//const Embed  = Quill.import('blots/embed')

const ATTRIBUTES = [
  'href',
];

const getNoteId = domNode => { //domNode.getAttribute('href')//.substring(1)
  return domNode.getAttribute('href')
  const re = /^#(.*)$/.exec(domNode.getAttribute('href'))
  if (re[1]) return parseInt(re[1])
  return ''
}

class NoteBlot extends Parchment.Embed {

  static create(value) {
    let node = super.create();
    node.setAttribute('href', '#' + value);
    node.setAttribute('contenteditable', false);
    node.innerText = '[note]'
    return node;
  }

  constructor(domNode, value) {
    domNode.setAttribute('contenteditable', false);
    super(domNode, value);
  }

  static formats(domNode) {
    return getNoteId(domNode)
  }

  static value(domNode) {
    return getNoteId(domNode)
  }

  format(name, value) {
    //return;
    if (ATTRIBUTES.indexOf(name) > -1) {
      if (value) {
        this.domNode.setAttribute(name, value);
      } else {
        this.domNode.removeAttribute(name);
      }
    } else {
      super.format(name, value);
    }
  }

}
NoteBlot.blotName = 'note';
NoteBlot.tagName = 'a';
NoteBlot.className = 'note';

export default NoteBlot;
