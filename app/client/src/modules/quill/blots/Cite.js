/*
 Mentions bibliographiques / titre ouvrage
 Blot : inline
 HTML5 : cite/a
*/

// TODO

import Quill from 'quill';

let Inline = Quill.import('blots/inline');

class CiteBlot extends Inline {

  static create(data) {
    let node = super.create();
    node.setAttribute('ref', data);
    return node;
  }

  static formats(domNode) {
    let ref = domNode.getAttribute('ref');
    return ref || true;
  }



  format(name, data) {
    if (name === 'location' && data) {
      this.domNode.setAttribute('ref', data);
    } else {
      super.format(name, data);
    }
  }

  formats() {
    let formats = super.formats();
    formats['cite'] = CiteBlot.formats(this.domNode);
    return formats;
  }
}
CiteBlot.blotName = 'cite';
CiteBlot.tagName = 'cite';

export default CiteBlot;

