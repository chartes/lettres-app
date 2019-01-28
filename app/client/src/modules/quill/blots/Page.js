import Quill from 'quill';

let Block = Quill.import('blots/block');

class PageBlot extends Block { }
PageBlot.blotName = 'page';
PageBlot.tagName = 'a';
PageBlot.className = 'pb';

export default PageBlot;