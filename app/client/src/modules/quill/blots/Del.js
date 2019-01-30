/*
 texte supprimé
 Blot : inline
 HTML5 : del
*/

import Quill from 'quill';

let Inline = Quill.import('blots/inline');

class Del extends Inline { }
Del.blotName = 'del';
Del.tagName = 'del';

export default Del;
