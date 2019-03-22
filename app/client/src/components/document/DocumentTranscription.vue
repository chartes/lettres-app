<template>
  <div v-if="editable" class="document__transcription document__subsection">
    <br/>
    <header class="title">
      <h2 class="document__transcription--title subtitle">Transcription</h2>
    </header>

    <rich-text-editor
            v-if="editable"
            v-model="transcriptionContent"
    >
      <editor-save-button
              :doc-id="document.id"
              name="transcription"
              :value="transcriptionContent"/>
    </rich-text-editor>
    <div v-else class="document__transcription--content" v-html="transcriptionContent"></div>

    <ol v-if="notes.length" class="note-list notes">
       <li  v-for="note in notes" :key="note.id">
         <div class="note-item" :class="noteItemClass">
           <div class="note-item__text" v-html="note.content"></div>
           <a v-if="editable" @click="openNoteEdit(note)" class="note-item__edit"><icon-pen-edit/></a>
           <a v-if="editable" @click="noteId = note.id" class="note-item__delete"><icon-bin/></a>
         </div>
       </li>
    </ol>
    <note-form
            v-if="noteEdit"
            title="Éditer la note"
            :note="noteEdit"
            :noteId="noteEditId"
            :submit="updateNote"
            :cancel="closeNoteEdit"
    />
    <modal-confirm-note-delete
          v-if="noteId"
          :note-id="noteId"
          :cancel="cancelNoteDelete"
          :submit="confirmNoteDelete"
      />
  </div>
</template>

<script>

  import { mapState } from 'vuex'
  import { removeContentEditableAttributesFromString, removeContentEditableAttributesFromObject } from '../../modules/document-helpers';
  import IconBin from '../ui/icons/IconBin';
  import IconPenEdit from '../ui/icons/IconPenEdit';
  import ModalConfirmNoteDelete from '../forms/ModalConfirmNoteDelete';
  import RichTextEditor from '../forms/fields/RichTextEditor';
  import NoteForm from '../forms/NoteForm';
  import EditorSaveButton from '../forms/fields/EditorSaveButton';

  export default {
    name: 'DocumentTranscription',
    components: {EditorSaveButton, NoteForm, RichTextEditor, ModalConfirmNoteDelete, IconPenEdit, IconBin },
    props: {
      editable: {
        type: Boolean,
        default: false
      },
    },
    data () {
      return {
        transcriptionContent: '',
        noteId: null,
        noteEdit: false,
        noteEditId: false,
      }
    },
    mounted() {
      this.transcriptionContent = this.document.transcription || ''
    },
    methods: {
      confirmNoteDelete (noteId) {
        this.$store.dispatch('document/removeNote', noteId)
          .then(noteId => {
            this.removeNoteFromDocument(noteId)
            this.removeNoteFromWitnesses(noteId)
            this.cancelNoteDelete()
          })
      },
      cancelNoteDelete () {
        this.noteId = false
      },
      updateNote (note) {
        this.$store.dispatch('document/updateNote', note)
          .then(() => {
            this.closeNoteEdit()
          })
          .catch(error => {

          })
      },
      openNoteEdit (note) {
        this.noteEdit = note;
      },
      closeNoteEdit () {
        this.noteEdit = false;
      },

      removeNoteFromDocument (noteId) {
        const pattern  = new RegExp('<a class="note" href="#'+noteId+'">\\[note\\]<\\/a>', 'mgi')
        const attributes = {};
        let changed = false;
        if (this.transcriptionContent) {
          const docTranscription = removeContentEditableAttributesFromString(this.transcriptionContent)
          const inTranscription = pattern.test(docTranscription)
          if (inTranscription) {
            attributes.transcription = docTranscription.replace(pattern, '')
            changed = true
          }
        }
        if (this.document.title) {
          const docTitle = removeContentEditableAttributesFromString(this.document.title)
          const inTitle = pattern.test(docTitle)
          if (inTitle) {
            attributes.title = docTitle.replace(pattern, '')
            changed = true
          }
        }
        if (this.document['creation-label']) {
          const docLabel = removeContentEditableAttributesFromString(this.document['creation-label'])
          const inLabel = pattern.test(docLabel)
          if (inLabel) {
            attributes['creation-label'] = docLabel.replace(pattern, '')
            changed = true
          }
        }
        if (this.document.argument) {
          const docArgument = removeContentEditableAttributesFromString(this.document.argument)
          const inArgument = pattern.test(docArgument)
          if (inArgument) {
            attributes.argument = docArgument.replace(pattern, '')
            changed = true
          }
        }
        if (changed) {
          const data = { id: this.document.id, attributes };
          this.$store.dispatch('document/save', data)
            .then(response => {
              if (attributes.transcription) this.transcriptionContent = attributes.transcription
            })
            .catch(err => {
              console.error(err)
          })
        }
      },
      removeNoteFromWitnesses (noteId) {
        const pattern  = new RegExp('<a class="note" href="#'+noteId+'">\\[note\\]<\\/a>', 'gi')
        this.witnesses.forEach((wit, index) => {
          const w = {...wit}
          removeContentEditableAttributesFromObject(w)
          const inContent = pattern.test(w.content)
          const inClassification = pattern.test(w['classification-mark'])
          let changed = false
          if (inContent) {
            w.content = w.content.replace(pattern, '')
            changed = true
          }
          if (inClassification) {
            w['classification-mark'] = w['classification-mark'].replace(pattern, '')
            changed = true
          }
          if(changed) {
            this.$store.dispatch('document/updateWitness', w)
              .then(response => {})
              .catch(err => {
                console.error(err)
              })
          }
        })
      }
    },
    computed: {
      ...mapState('document', ['document', 'notes', 'witnesses']),
      noteItemClass () {
        return this.editable ? 'note-item--editable' : false
      }
    },
    watch: {

    }
  }
</script>

<style scoped>
</style>