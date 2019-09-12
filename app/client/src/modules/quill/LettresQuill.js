import Quill from 'quill';
import Delta from 'quill-delta';

import PlainClipboard from './PlainClipboard'

import BoldBlot from './blots/Bold';
import CiteBlot from './blots/Cite';
import DelBlot from './blots/Del';
import ItalicBlot from './blots/Italic';
import LineBreak from './blots/LineBreak';
import LinkBlot from './blots/Link';
import LocationBlot from './blots/Location';
import NoteBlot from './blots/Note';
import PageBlot from './blots/Page';
import ParagraphBlot from './blots/Paragraph';
import PersonBlot from './blots/Person';
import SuperscriptBlot from './blots/Superscript';



let Inline = Quill.import('blots/inline');
let Embed = Quill.import('blots/embed');

// Lower index means deeper in the DOM tree, since not found (-1) is for embeds
Inline.order = [
  'cursor', 'inline',   // Must be lower
  'underline', 'strike', 'italic', 'bold', 'script',
  'del', 'link', 'code',
  'person', 'location',          // Must be higher
];

Quill.register('modules/clipboard', PlainClipboard, true);

Quill.register(BoldBlot, true);
Quill.register(CiteBlot, true);
Quill.register(DelBlot, true);
Quill.register(ItalicBlot, true);
Quill.register(LineBreak, true);
Quill.register(LinkBlot, true);
Quill.register(LocationBlot, true);
Quill.register(NoteBlot, true);
Quill.register(PageBlot, true);
Quill.register(ParagraphBlot, true);
Quill.register(PersonBlot, true);
Quill.register(SuperscriptBlot, true);

function lineBreakMatcher() {
  var newDelta = new Delta();
  newDelta.insert({'linebreak': ''});
  return newDelta;
}

const options = {
  modules: {
    history: {
      userOnly: true
    },

    clipboard: {
      matchers: [
        ['lb', lineBreakMatcher]
      ]
    },
    keyboard: {
      bindings: {
        linebreak: {
          key: 13,
          shiftKey: true,
          handler: function (range) {
            this.quill.insertEmbed(range.index, 'linebreak', true, 'user');
            this.quill.setSelection(range.index + 1, Quill.sources.SILENT);
          }
        }
      }
    }
  },
  placeholder: null,
};


function getNewQuill (elt, opt = null) {

  const opts = {...options, ...opt};
  console.log("quill options:", opts);
  
  let quill = new Quill(elt, opts);
  var length = quill.getLength()
  var text = quill.getText(length - 2, 2)
  // Remove extraneous new lines

  if (text === '\n\n') {
    quill.deleteText(quill.getLength() - 2, 2)
  }
  
  // fix placeholder not showing
  if (quill.getLength() === 4) {
    quill.setText('');
  }

  return quill;
}

export {

  getNewQuill,

  Inline,
  Embed,

  options,

  Quill as default
}
