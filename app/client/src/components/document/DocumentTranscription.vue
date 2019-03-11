<template>
  <div v-if="document.transcription.length  || editable> 0" class="document__transcription document__subsection">
    <br/>
    <header class="title">
      <h2 class="document__transcription--title subtitle">Transcription</h2>
    </header>

    <rich-text-editor
            v-if="editable"
            v-model="transcriptionContent"
    />
    <div v-else class="document__transcription--content" v-html="transcriptionContent"></div>

    <ol v-if="notesContent.length" class="note-list notes">
       <li  v-for="(note, index) in notesContent" :key="note.id">
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
  import DocumentAttributes from './DocumentAttributes';
  import TranscriptionEditor from '../forms/fields/TranscriptionEditor';
  import IconBin from '../ui/icons/IconBin';
  import IconPenEdit from '../ui/icons/IconPenEdit';
  import ModalConfirmNoteDelete from '../forms/ModalConfirmNoteDelete';
  import RichTextEditor from '../forms/fields/RichTextEditor';
  import NoteForm from '../forms/NoteForm';

  export default {
    name: 'DocumentTranscription',
    components: {
      NoteForm,
      RichTextEditor, ModalConfirmNoteDelete, IconPenEdit, IconBin, TranscriptionEditor, DocumentAttributes},
    props: {
      editable: {
        type: Boolean,
        default: false
      },
    },
    data () {
      return {
        noteId: null,
        noteEdit: false,
        noteEditId: false,
      }
    },
    created() {
      this.transcriptionContent = this.document.transcription;
      this.notesContent = this.notes;
    },
    methods: {
      confirmNoteDelete (noteId) {
        console.log("confirmNoteDelete", noteId)
        this.$store.dispatch('document/removeNote', noteId)
          .then(noteId => {
            const pattern  = new RegExp('<a class="note" href="#'+noteId+'">\\[note\\]<\\/a>', 'gi')
            console.log('pattern', pattern)
            console.log('note in transcription', pattern.test(this.transcriptionContent))
            console.log('note in title', pattern.test(this.document.title), this.document.title)
            console.log('note in title', this.document.title.replace(pattern, ''))
            console.log('note in argument', pattern.test(this.document.argument), this.document.argument)
          })
      },
      cancelNoteDelete () {
        console.log("cancelNoteDelete")
        this.noteId = false
      },
      updateNote (note) {
        console.log("updateNote", note)
        this.$store.dispatch('document/updateNote', note)
          .then(() => {
            this.closeNoteEdit()
          })
          .catch(error => {

          })
      },
      openNoteEdit (note) {
        console.log("openNoteEdit", note)
        this.noteEdit = note;
      },
      closeNoteEdit () {
        console.log("closeNoteEdit")
        this.noteEdit = false;
      },

      removeNoteFromTranscription () {

      },
      removeNoteFromArgument () {

      },
      removeNoteFromTitle () {

      },
    },
    computed: {
      ...mapState('document', ['document', 'notes']),
      noteItemClass () {
        return this.editable ? 'note-item--editable' : false
      }
    }
  }
</script>

<style scoped>
</style>