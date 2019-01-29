//import Embed from 'quill/blots/embed';
import Parchment from 'parchment';

class LineBreak extends Parchment.Embed {
  static create(value) {
    let node = super.create(value);
    return node;
  }
  length () {
    return 1
  }
  insertInto(parent, ref) {
    Parchment.Embed.prototype.insertInto.call(this, parent, ref)
  }
}
LineBreak.blotName = 'linebreak';
LineBreak.tagName = 'br';


export default LineBreak;
