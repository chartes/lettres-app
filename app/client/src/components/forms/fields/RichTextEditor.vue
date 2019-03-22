<template>
  
  <div class="field rich-text-editor">
    
    <field-label v-if="!!label" :label="label"/>
    
    <div class="editor-area">
      <div class="editor-controls" ref="controls">
        
        <div v-for="group, gindex in formats" :key="gindex" class="editor-controls-group field has-addons">
          <editor-button
              v-for="format in group"
              :active="formatCallbacks[format].active"
              :callback="formatCallbacks[format].cb"
              :selected="buttons[format]"
              :format="format"
              :key="format"
          />
        </div>
        <div class="editor-controls-group is-additional" v-if="slotNotEmpty">
          <slot></slot>
        </div>
      
      </div>
      
      <div class="editor-container">
        <div class="quill-editor" :class="{ 'single-line': !multiline }" ref="editor" spellcheck="false"></div>
      </div>
      <note-form
              v-if="formNote"
              title="Nouvelle note"
              :submit="submitNoteForm"
              :cancel="closeNoteForm"
      />
      <textfield-form
              v-if="formTextfield"
              :title="formTextfield.title"
              :label="formTextfield.label"
              :value="formTextfield.value"
              :submit="customSubmitTextfieldForm || submitTextfieldForm"
              :cancel="closeTextfieldForm"
              :remove="removeTextfieldForm"
      />
      <person-list-form
          v-if="formPerson"
          title="Sélectionner une personne"
          :submit="submitPersonForm"
          :cancel="closePersonForm"
          :remove="removePersonForm"
      />
      <placename-list-form
          v-if="formLocation"
          title="Sélectionner un lieu"
          :submit="submitLocationForm"
          :cancel="closeLocationForm"
          :remove="removeLocationForm"
      />
      
      <pre v-if="debug" style="white-space: normal">{{value}}</pre>

    </div>
  
  </div>

</template>

<script>

  import Vue from 'vue';
  import ClickOutside from 'vue-click-outside';
  import EditorButton from './EditorButton.vue';
  import TextfieldForm from '../TextfieldForm';
  import FieldLabel from './FieldLabel';

  import Quill, { getNewQuill } from '../../../modules/quill/LettresQuill';
  import { getNewDelta } from '../../../modules/quill/DeltaUtils';
  import _isEmpty from 'lodash/isEmpty';
  import NoteForm from '../NoteForm';
  import PersonListForm from '../PersonListForm';
  import PlacenameListForm from '../PlacenameListForm';

  const wrapPattern = /^<p>(.*)<\/p>$/im;
  let formatCallbacks = {}

  export default {
    name: "RichTextEditor",
    props: {
      label: { type: String, default: null },
      value: { type: String, default: '' }, // v-model support
      multiline: { type: Boolean, default: true },
      enabled: { type: Boolean, default: true },
      formats: { type: Array, default: () => [['note','page','link'],['bold','italic','superscript','underline','del'],['person','location','cite']] },
    },
    //mixins: [EditorNotesMixins],
    components: {
      PlacenameListForm,
      PersonListForm,
      NoteForm,
      FieldLabel,
      TextfieldForm,
      EditorButton,
    },
    directives: {
      ClickOutside
    },
    data() {
      return {
        debug: false,
        editor: null,
        editorElement: null,
        editorContentElement: null,
        editorHasFocus: false,
        currentSelection: null,
        formTextfield: null,
        formPerson: null,
        formLocation: null,
        formNote: null,
        actionsPositions: {
          top: 0, left: 0, right: 0, bottom: 0
        },
        editorInited: false,
        delta: null,
        customSubmitTextfieldForm: null,
        buttons: {}
      }
    },
    mounted () {
      //console.log("this.$props.value", this.$props.value, this.buttons)
      this.initEditor(this.$refs.editor, this.$props.value);

      let flattenFormats = [];
      this.$props.formats.forEach(group => {
        flattenFormats.push(...group)
      })
      flattenFormats.forEach(format => { this.buttons[format] = false })

    },
    beforeDestroy () {
      this.deactivateEvents();
    },
    methods: {

      initEditor(editorElement, initialContent) {

        console.log("initEditor", initialContent)

        editorElement.innerHTML = this.sanitize(initialContent);
        this.editor = getNewQuill(editorElement);
        this.editorElement = editorElement;
        this.editorContentElement = editorElement.children[0];
        this.activateEvents();
        this.editor.updateContents(getNewDelta().retain(this.editor.getLength(), 'silent'))
        this.editorInited = true;
      },

      activateEvents () {
        if (!this.multiline) {
          this.editorElement.addEventListener('keydown', this.onSingleKeyup, true)
        }
        this.editor.on('selection-change', this.onSelection);
        this.editor.on('selection-change', this.onFocus);
        this.editor.on('text-change', this.onTextChange);
        this.editor.on('text-change', this.updateValue);
      },
      deactivateEvents () {
        //console.log("EditorMixins.deactivateEvents")
        this.editorElement.removeEventListener('keydown', this.onSingleKeyup, true)
        this.editor.off('selection-change', this.onSelection);
        this.editor.off('selection-change', this.onFocus);
        this.editor.off('text-change', this.onTextChange);
        this.editor.off('text-change', this.updateValue);
      },

      getEditorHTML () {
        return this.editorContentElement.innerHTML;
      },

      /**************
       *
       * V-MODEL SUPPORT
       */

      updateValue () {
        const content = this.getEditorHTML();
        content.replace(' contenteditable="false"', '')
        if (this.multiline) {
          return this.$emit('input', content.replace(/<p><br><\/p>$/, ''));
        }
        let inputValue = content.replace(/<(\/)*p>/gi, '');
        inputValue = inputValue === '<br>' ? '' : inputValue;
        this.$emit('input', inputValue)
      },

      updateContent () {
        this.delta = this.editor.getContents().ops;
      },

      /**************
       *
       * SANITIZE
       */

      sanitize (val) {
        let newValue = val || '';
        newValue = newValue.replace(/\n/gmi, '')
        if (!this.multiline) {
          newValue = newValue.replace(/<(br)?(\/)?(p)?>/gi, '');
        }
        newValue = newValue === '' ? '<br>' : newValue;
        const test = wrapPattern.test(newValue)
        newValue = test ? newValue : `<p>${newValue}</p>`;
        return newValue
      },

      preventLineBreaks (delta) {
        const ops = delta.ops;
        const l = ops.length;
        return;
        if (ops[l-1].insert && ops[l-1].insert === '\n') {
          const updateDelta = getNewDelta();
          if (l === 1) {
             updateDelta.delete(1)
          } else {
            const retain = ops[l-2].retain;
            updateDelta.retain(retain).delete(1)
          }
          this.editor.updateContents(updateDelta, 'silent')
        }
      },

      /**************
       *
       * EDITOR EVENT HANDLERS
       */

      onTextChange (delta, oldDelta, source) {
        if (!this.multiline){
          this.preventLineBreaks(delta)
        }
        return;
        if (delta.ops.length > 1 && delta.ops[1].delete) {
          const diff = this.editor.getContents().diff(oldDelta).ops
          console.log(' diff', diff, diff.length > 1 && diff[1].insert && diff[1].insert.note)
        }
      },
      onSelection (range) {
        if (range) {
          this.setRangeBound(range);
          let formats = this.editor.getFormat(range.index, range.length);
          this.updateButtons(formats);
        }
      },
      onSingleKeyup (evt) {
        if (evt.code === "Escape") {
          this.$emit('on-keyup-escape')
        } else if (evt.code === "Enter") {
          evt.preventDefault()
          evt.stopImmediatePropagation()
          evt.stopPropagation()
          this.$emit('on-keyup-enter')
        }
      },
      onFocus () {
        this.editorHasFocus = this.editor.hasFocus();
      },

      simpleFormat(formatName) {
        let selection = this.editor.getSelection();
        let format = this.editor.getFormat(selection.index, selection.length);
        let value = !format[formatName];
        this.editor.format(formatName, value);
        let formats = this.editor.getFormat(selection.index, selection.length);
        this.updateButtons(formats);
      },

      insertPageBreak (pageNum) {
        this.insertEmbed('page', pageNum)
      },
      insertEmbed (formatName, value) {
        console.log('insertEmbed', formatName, value)
        let format = {}
        format[formatName] = value;
        let range = this.editor.getSelection(true);
        this.editor.insertEmbed(range.index, formatName, value, Quill.sources.API)
        this.editor.setSelection(range.index + 1, Quill.sources.SILENT);
      },

      updateButtons (formats) {
        if (_isEmpty(formats)) formats = { paragraph: true }
        for (let key in this.buttons) {
          this.buttons[key] = !!formats[key];
        }
      },

      setRangeBound (range) {
        let rangeBounds = this.editor.getBounds(range);
        this.actionsPositions.left = rangeBounds.left;
        this.actionsPositions.right = rangeBounds.right;
        this.actionsPositions.bottom = rangeBounds.bottom;
      },

      /**************
       *
       * NOTES METHODS
       */

      displayNoteForm() {
        console.log('displayNoteForm')
        this.formNote = true
      },
      closeNoteForm() {
        this.formNote = false
      },
      submitNoteForm(note) {
        console.log('submitNoteForm', note)
        this.insertEmbed('note', note.id)
        this.closeNoteForm();
        let formats = this.editor.getFormat();
        this.updateButtons(formats)
      },
      removeNoteForm() {
        console.log("Note")
        this.editor.format('location', false);
        this.closeLocationForm();
        let formats = this.editor.getFormat();
        this.updateButtons(formats)
      },

      /**************
       *
       * TEXTFIELD FORM METHODS
       */

      displayTextfieldForm (formData) {
        let format = this.editor.getFormat();
        formData.value = format[formData.format];
        this.formTextfield = formData;
      },
      closeTextfieldForm () {
        this.formTextfield = null;
        this.customSubmitTextfieldForm = null;
      },
      removeTextfieldForm () {
        this.editor.format(this.formTextfield.format, false);
        this.formTextfield = null;
      },
      submitTextfieldForm (data) {
        this.editor.format(this.formTextfield.format, data);
        this.closeTextfieldForm();
        let formats = this.editor.getFormat();
        this.updateButtons(formats)
      },
      removeFormat () {
        //console.log("removeFormat", this.formTextfield.format)
        const formatName = this.formTextfield.format;
        const selection = this.editor.getSelection();
        this.editor.format(formatName, '');
        this.closeTextfieldForm();
        let formats = this.editor.getFormat(selection.index, selection.length);
        this.updateButtons(formats);
      },

      /**************
       *
       * LOCATION METHODS
       */

      displayLocationForm() {
        this.formLocation = true
      },
      closeLocationForm() {
        this.formLocation = false
      },
      submitLocationForm(loc) {
        this.editor.format('location', loc.id);
        this.closeLocationForm();
        let formats = this.editor.getFormat();
        this.updateButtons(formats)
      },
      removeLocationForm() {
        console.log("removeLocationForm")
        this.editor.format('location', false);
        this.closeLocationForm();
        let formats = this.editor.getFormat();
        this.updateButtons(formats)
      },

      /**************
       *
       * LINK METHODS
       */

      displayLinkForm() {
        this.displayTextfieldForm ({
          format: 'link',
          title: '<i class="fas fa-link"></i> Insérer un lien',
          label: 'URL du lien'
        });
      },

      /**************
       *
       * PAGE BREAK METHODS
       */

      displayPageBreakForm () {
        this.customSubmitTextfieldForm = this.submitPageBreakForm;
        this.displayTextfieldForm ({
          format: 'link',
          title: '<i class="fas fa-page"></i> Insérer un saut de page',
          label: 'Numéro de page'
        });

      },
      submitPageBreakForm (pageNum) {
        console.log("submitPageBreakForm", pageNum)
        this.insertEmbed('page', {pageNum})
        this.closeTextfieldForm();
        let formats = this.editor.getFormat();
        this.updateButtons(formats)
      },

      /**************
       *
       * PERSON METHODS
       */

      displayPersonForm() {
        this.formPerson = true
      },
      closePersonForm() {
        this.formPerson = false
      },
      submitPersonForm(pers) {
        this.editor.format('person', pers.id);
        this.closePersonForm();
        let formats = this.editor.getFormat();
        this.updateButtons(formats)
      },

      /**************
       *
       * CITE METHODS
       */

      displayCiteForm() {
        this.displayTextfieldForm ({
          format: 'cite',
          title: '<i class="fas fa-book"></i> Ajouter une mention bibliographique',
          label: 'Référence'
        });
      },

    },

    watch: {
      value (val) {
        const range = this.editor.getSelection();
        this.editorContentElement.innerHTML = this.sanitize(val);
        Vue.nextTick(() => {
          if (range) {
            //console.log('setSelection', range.index)
            this.editor.setSelection(range.index, range.length, Quill.sources.SILENT);
          }
        })
      },
      enabled (val) {
        this.editor.enable(val);
      }
    },

    computed: {
      formatCallbacks() {
        return {
          note: { cb: this.displayNoteForm, active: this.isNoteButtonActive },
          page: { cb: this.displayPageBreakForm, active: this.editorHasFocus },
          link: { cb: this.displayLinkForm, active: this.editorHasFocus },
          bold: { cb: this.simpleFormat, active: this.editorHasFocus },
          italic: { cb: this.simpleFormat, active: this.editorHasFocus },
          superscript: { cb: this.simpleFormat, active: this.editorHasFocus },
          underline: { cb: this.simpleFormat, active: this.editorHasFocus },
          del: { cb: this.simpleFormat, active: this.editorHasFocus },
          person: { cb: this.displayPersonForm, active: this.editorHasFocus },
          location: { cb: this.displayLocationForm, active: this.editorHasFocus },
          cite: { cb: this.simpleFormat, active: this.editorHasFocus },
        }
      },
      actionsPosition () {
        /** get the actions bar position **/
        let top = this.actionsPositions.bottom + 5;
        let left = (this.actionsPositions.left+this.actionsPositions.right)/2;
        return `top:${top}px;left:${left}px`;
      },
      isNoteButtonActive () {
        if (!this.editor) return;
        const selection = this.editor.getSelection();
        const cond = this.editorHasFocus
          //&& this.buttons.note
          && !selection.length;
        return cond;
      },
      slotNotEmpty () {
        return !!this.$slots.default;
      },
    },
  }
</script>

<style scoped>

</style>