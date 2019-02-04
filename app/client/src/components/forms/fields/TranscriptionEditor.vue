<template>
  <div class="editor-area">
    <div class="editor-controls" ref="controls">
      <div class="editor-controls-group">
        <editor-button :selected="buttons.paragraph" :active="editorHasFocus" :callback="simpleFormat" :format="'paragraph'"/>
        <editor-button :active="isNoteButtonActive" :callback="newNoteChoiceOpen" :format="'note'"/>
        <editor-button :selected="buttons.page" :active="editorHasFocus" :callback="simpleFormat" :format="'page'"/>
        <editor-button :selected="buttons.link" :active="editorHasFocus" :callback="simpleFormat" :format="'link'"/>
      </div>
      <div class="editor-controls-group">
        <editor-button :selected="buttons.bold" :active="editorHasFocus" :callback="simpleFormat" :format="'bold'"/>
        <editor-button :selected="buttons.italic" :active="editorHasFocus" :callback="simpleFormat" :format="'italic'"/>
        <editor-button :selected="buttons.superscript" :active="editorHasFocus" :callback="simpleFormat" :format="'superscript'"/>
        <editor-button :selected="buttons.underline" :active="editorHasFocus" :callback="simpleFormat" :format="'underline'"/>
      </div>
      <div class="editor-controls-group">
        <editor-button :selected="buttons.del" :active="editorHasFocus" :callback="simpleFormat" :format="'del'"/>
        <editor-button :selected="buttons.person" :active="editorHasFocus" :callback="displayPersonForm" :format="'person'"/>
        <editor-button :selected="buttons.location" :active="editorHasFocus" :callback="displayLocationForm" :format="'location'"/>
        <editor-button :selected="buttons.cite" :active="editorHasFocus" :callback="simpleFormat" :format="'cite'"/>
      </div>
    </div>
    <div class="editor-container">
      <div class="quill-editor" id="transcription-editor" ref="editor" spellcheck="false"></div>
      <note-actions
              v-show="selectedNoteId && this.editor.hasFocus()"
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
</template>

<script>

  import { mapState } from 'vuex'
  import EditorButton from './EditorButton.vue';
  import EditorMixins from '../editor/EditorMixins'
  import EditorNotesMixins from '../editor/EditorNotesMixins'
  import TextfieldForm from '../TextfieldForm';
  import NoteActions from '../editor/NoteActions';
  import NewNoteActions from '../editor/NewNoteActions';

  export default {
    name: "transcription-editor",
    props: {initialContent: { type: String }},
    mixins: [EditorMixins, EditorNotesMixins],
    components: {
      NewNoteActions,
      NoteActions,
      TextfieldForm,
      EditorButton,
    },
    data() {
      return {
        storeActions: {
          changed: null//'transcription/changed'
        },
        delta: null,
        buttons: {
          bold: false,
          italic: false,
          superscript: false,
          underline: false,
          del: false,
          person: false,
          location: false,
          note: false,
          paragraph: false,
        }
      }
    },
    mounted () {

      this.initEditor(this.$refs.editor, this.$props.initialContent);

    },
    beforeDestroy () {
      this.deactivateEvents();
    },
    methods: {

      updateContent () {
        this.delta = this.editor.getContents().ops;

      },

    },

    computed: {
      ...mapState('transcription', ['transcriptionSaved']),
      ...mapState('translation', ['translationSaved']),
    }
  }
</script>