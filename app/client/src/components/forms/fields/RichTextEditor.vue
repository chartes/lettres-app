<template>

  <div class="field rich-text-editor">

    <field-label v-if="!!label" :label="label"/>

    <div class="editor-area">
      <div class="editor-controls" ref="controls">

        <div v-for="group, gindex in formats" :key="gindex" class="editor-controls-group">
          <editor-button
                  v-for="format in group"
                  :active="formatCallbacks[format].active"
                  :callback="formatCallbacks[format].cb"
                  :selected="buttons[format]"
                  :format="format"
                  :key="format"
          />
        </div>

      </div>

      <div class="editor-container">
        <div class="quill-editor" id="transcription-editor" ref="editor" spellcheck="false"></div>
        <note-actions
                v-show="selectedNoteId && editorHasFocus"
                refs="noteActions"
                :style="actionsPosition"
                :newNote="setNoteEditModeNew"
                :edit="setNoteEditModeEdit"
                :updateLink="setNoteEditModeList"
                :unlink="unlinkNote"
                :delete="setNoteEditModeDelete"/>
        <new-note-actions
                v-if="defineNewNote"
                :modeNew="setNoteEditModeNew"
                :modeLink="setNoteEditModeList"
                :cancel="newNoteChoiceClose"
        />
      </div>
      <textfield-form
              v-if="formTextfield"
              :title="formTextfield.title"
              :label="formTextfield.label"
              :value="formTextfield.value"
              :submit="submitTextfieldForm"
              :cancel="cancelTextfieldForm"/>

    </div>

  </div>

</template>

<script>
  import Vue from 'vue';
  import EditorButton from './EditorButton.vue';
  import EditorNotesMixins from '../editor/EditorNotesMixins'
  import TextfieldForm from '../TextfieldForm';
  import NoteActions from '../editor/NoteActions';
  import NewNoteActions from '../editor/NewNoteActions';
  import FieldLabel from './FieldLabel';

  import Quill, { getNewQuill } from '../../../modules/quill/LettresQuill';
  import { getNewDelta } from '../../../modules/quill/DeltaUtils';
  import _isEmpty from 'lodash/isEmpty';

  const wrapPattern = /^<p>(.*)<\/p>$/im;
  let formatCallbacks = {}

  export default {
    name: "RichTextEditor",
    props: {
      label: { type: String, default: null },
      value: { type: String, default: '' }, // v-model support
      multiline: { type: Boolean, default: true },
      formats: { type: Array, default: () => [['note','page','link'],['bold','italic','superscript','underline','del'],['person','location','cite']] },
    },
    mixins: [EditorNotesMixins],
    components: {
      FieldLabel,
      NewNoteActions,
      NoteActions,
      TextfieldForm,
      EditorButton,
    },
    data() {
      return {
        editor: null,
        editorContentElement: null,
        editorHasFocus: false,
        currentSelection: null,
        formTextfield: null,
        actionsPositions: {
          top: 0, left: 0, right: 0, bottom: 0
        },
        editorInited: false,
        delta: null,
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
      //console.log('flattenFormats', flattenFormats)

    },
    beforeDestroy () {
      this.deactivateEvents();
    },
    methods: {

      initEditor(editorElement, initialContent) {

        //console.log("initEditor", editorElement, initialContent)

        editorElement.innerHTML = this.sanitize(initialContent);
        this.editor = getNewQuill(editorElement);
        this.editorContentElement = editorElement.children[0];
        this.activateEvents();
        this.editor.updateContents(getNewDelta().retain(this.editor.getLength(), 'silent'))
        this.editorInited = true;
      },

      activateEvents () {
        //console.log("EditorMixins.activateEvents")
        this.editor.on('selection-change', this.onSelection);
        this.editor.on('selection-change', this.onFocus);
        this.editor.on('text-change', this.onTextChange);
        this.editor.on('text-change', this.updateValue);
      },
      deactivateEvents () {
        //console.log("EditorMixins.deactivateEvents")
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
        if (this.multiline) {
          return this.$emit('input', content.replace(/<p><br><\/p>$/, ''));
        }
        let inputValue = content.replace(/<(\/)*p>/gi, '');
        inputValue = inputValue === '<br>' ? '' : inputValue;
        this.$emit('input', inputValue)
      },

      updateContent () {
        //console.log("updateContent")
        this.delta = this.editor.getContents().ops;

      },

      /**************
       *
       * SANITIZE
       */

      sanitize (val) {
        let newValue = val || '';
        //console.log("")
        //console.log("sanitize", this.multiline ? 'multi': 'single', val);
        if (!this.multiline) {
          newValue = newValue.replace(/<(br)?(\/)?(p)?>/gi, '');
          //console.log('   0. single', newValue)
        } else {
          //console.log('   0. multi', newValue)

        }
        newValue = newValue === '' ? '<br>' : newValue;
        //console.log('   1.', newValue)
        const test = wrapPattern.test(newValue)
        newValue = test ? newValue : `<p>${newValue}</p>`;
        //console.log('   2.', newValue)
        //console.log("")
        return newValue

      },

      preventLineBreaks (delta) {
        const ops = delta.ops;
        const l = ops.length;
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
        //console.log('onTextChange', delta.ops)
        if (!this.multiline){
          this.preventLineBreaks(delta)
        }
      },
      onSelection (range) {
        if (range) {
          this.setRangeBound(range);
          let formats = this.editor.getFormat(range.index, range.length);
          this.updateButtons(formats);
          //console.log("onSelection", range, formats)
          if (!!formats.note) {
            this.onNoteSelected(formats.note, range);
            this.buttons.note = false;
          } else {
            this.selectedNoteId = null;
            this.buttons.note = true;
          }
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

      insertNote () {
        this.insertEmbed('note', true)
      },
      insertPageBreak () {
        this.insertEmbed('page', true)
      },
      insertEmbed (formatName, value) {
        let format = {}
        format[formatName] = value;
        let range = this.editor.getSelection(true);
        this.editor.updateContents(getNewDelta().retain(range.index).delete(range.length).insert(format), Quill.sources.USER);
        this.editor.setSelection(range.index + 1, Quill.sources.SILENT);
      },

      updateButtons (formats) {
        if (_isEmpty(formats)) formats = { paragraph: true }
        for (let key in this.buttons) {
          this.buttons[key] = !!formats[key];
        }
      },

      setRangeBound (range) {
        /** get and set the range bound of the selection to locate the actions bar **/
          //console.log("setRangeBound", range);
        let rangeBounds = this.editor.getBounds(range);
        this.actionsPositions.left = rangeBounds.left;
        this.actionsPositions.right = rangeBounds.right;
        this.actionsPositions.bottom = rangeBounds.bottom;
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
      cancelTextfieldForm () {
        this.formTextfield = null;
      },
      submitTextfieldForm (data) {
        this.editor.format(this.formTextfield.format, data);
        this.cancelTextfieldForm();
        let formats = this.editor.getFormat();
        this.updateButtons(formats)
      },
      removeFormat () {
        //console.log("removeFormat", this.formTextfield.format)
        const formatName = this.formTextfield.format;
        const selection = this.editor.getSelection();
        this.editor.format(formatName, '');
        this.cancelTextfieldForm();
        let formats = this.editor.getFormat(selection.index, selection.length);
        this.updateButtons(formats);
      },

      /**************
       *
       * LOCATION METHODS
       */

      displayLocationForm() {
        this.displayTextfieldForm ({
          format: 'location',
          title: '<i class="fas fa-map-marker-alt"></i> Identifier un lieu',
          label: 'Nom du lieu'
        });
      },

      /**************
       *
       * PERSON METHODS
       */

      displayPersonForm() {
        this.displayTextfieldForm ({
          format: 'person',
          title: '<i class="fas fa-user"></i> Identifier une personne',
          label: 'Nom de la personne'
        });
      },

      /**************
       *
       * PERSON METHODS
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
        //console.log('watcher value val', val, range, this.editor.hasFocus())
        this.editorContentElement.innerHTML = this.sanitize(val);
        Vue.nextTick(() => {
          if (range) {
            //console.log('setSelection', range.index)
            this.editor.setSelection(range.index, range.length, Quill.sources.SILENT);
          }
        })

        //this.editor.update();
      }
    },

    computed: {
      formatCallbacks() {
        return {
          note: { cb: this.newNoteChoiceOpen, active: this.isNoteButtonActive },
          page: { cb: this.simpleFormat, active: this.editorHasFocus },
          link: { cb: this.simpleFormat, active: this.editorHasFocus },
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
        const cond = this.editorHasFocus && this.buttons.note;
        return cond;
      }
    }
  }
</script>

<style scoped>

</style>