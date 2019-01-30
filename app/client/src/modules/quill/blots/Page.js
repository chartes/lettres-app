import Parchment from 'parchment';
//import { sanitize } from '../formats/link';

const ATTRIBUTES = [
  'href',
];

class PageBlot extends Parchment.Embed {

  static create(value) {

    if (typeof value !== 'object') return;
    let node = super.create();
    node.setAttribute('href', this.sanitize(value.href));
    node.innerText = value.pageNum
    return node;
  }

  static formats(domNode) {
    return {
      href: domNode.getAttribute('href'),
      pageNum: domNode.innerText
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
      pageNum: domNode.innerText
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

/*
import Parchment from 'parchment';

class PageBlot extends Parchment.Embed {

  static create(data) {
    let node = super.create();
    console.log("PageBlot.create", node, data)
    //node.text = data.page
    node.setAttribute('href', data);
    console.log("   => create", node)
    return node;
  }

  static formats(domNode) {
    console.log("PageBlot.formats", domNode.getAttribute('href'), domNode.text)

    let format = {
      href: domNode.getAttribute('href'),
      //page: domNode.text
    };
    console.log("   format =>", format)
    return format || {};
  }



  format(name, data) {
    console.log("page format()", name, data)
    if (name === 'page' && data) {
      //this.domNode.text = data.page
      this.domNode.setAttribute('href', data);
    } else {
      super.format(name, data);
    }
  }

  formats() {
    let formats = super.formats();
    formats['page'] = PageBlot.formats(this.domNode);
    console.log("page formats()", formats, this.domNode)
    return formats;
  }
}
PageBlot.blotName = 'page';
PageBlot.tagName = 'a';
PageBlot.className = 'pb';

export default PageBlot;
*/
