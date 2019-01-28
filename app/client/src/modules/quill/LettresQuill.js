import Quill from 'quill';
import Delta from 'quill-delta';

import PlainClipboard from './PlainClipboard'

import BoldBlot from './blots/Bold';
import ItalicBlot from './blots/Italic';
import SuperscriptBlot from './blots/Superscript';

import DelBlot from './blots/Del';
import LinkBlot from './blots/Link';
import PersonBlot from './blots/Person';
import CiteBlot from './blots/Cite';
import LocationBlot from './blots/Location';

import LineBreak from './blots/LineBreak';
import Paragraph from './blots/Paragraph';
import NoteBlot from './blots/Note';
import ZoneBlot from './blots/Zone';

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

Quill.register(LineBreak, true);
Quill.register(BoldBlot, true);
Quill.register(ItalicBlot, true);
Quill.register(SuperscriptBlot, true);
Quill.register(DelBlot, true);
Quill.register(LinkBlot, true);
Quill.register(LocationBlot, true);
Quill.register(CiteBlot, true);
Quill.register(PersonBlot, true);
Quill.register(Paragraph, true);
Quill.register(NoteBlot, true);
Quill.register(ZoneBlot, true);

// other
Quill.register(SpeechpartBlot, true);

function lineBreakMatcher() {
  var newDelta = new Delta();
  newDelta.insert({'linebreak': ''});
  return newDelta;
}

const options = {
  modules: {

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
  }
};


function getNewQuill (elt, opt = null) {

  let opts = opt || options;

  let quill = new Quill(elt, options);
  var length = quill.getLength()
  var text = quill.getText(length - 2, 2)

  // Remove extraneous new lines
  if (text === '\n\n') {
    quill.deleteText(quill.getLength() - 2, 2)
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
