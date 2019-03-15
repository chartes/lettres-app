

import Parchment from 'parchment';
import Quill from 'quill/quill';

const Embed  = Quill.import('blots/embed')
const ATTRIBUTES = [
  'href',
];

const getPageNum = txt => {
  const re = /\[p\. (.*)\]/.exec(txt)
  if (re[1]) return re[1]
  return ''
}

class PageBlot extends Parchment.Embed {

  static create(value) {
    if (typeof value !== 'object') return;
    let node = super.create();
    node.setAttribute('href', this.sanitize(value.href));
    node.setAttribute('contenteditable', false);
    node.innerText = `[p. ${value.pageNum}]`
    return node;
  }

  static formats(domNode) {
    return {
      href: domNode.getAttribute('href'),
      pageNum: getPageNum(domNode.innerText)
    }
  }

  static match(url) {
    return url
    //return /\.(jpe?g|gif|png)$/.test(url) || /^data:image\/.+;base64/.test(url);
  }

  static sanitize(url) {
    return url;
    //return sanitize(url, ['http', 'https', 'data']) ? url : '//:0';
  }

  static value(domNode) {
    return {
      href: domNode.getAttribute('href'),
      pageNum: getPageNum(domNode.innerText)
    }
  }

  format(name, value) {
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
PageBlot.blotName = 'page';
PageBlot.tagName = 'a';
PageBlot.className = 'pb';


export default PageBlot;