<template>
  <section v-if="document.transcription.length  || editable> 0" class="document__transcription section">
    <br/>
    <header class="title">
      <h2 class="document__transcription--title subtitle">Transcription</h2>
    </header>

    <transcription-editor v-if="editable" :initial-content="transcriptionContent"/>
    <div v-else class="document__transcription--content" v-html="transcriptionContent"></div>

    <ol v-if="notesContent.length" class="document__notes--content notes">
       <li  v-for="(note, index) in notesContent" v-html="note.content" :id="note.id"></li>
    </ol>
  </section>
</template>

<script>

  import { mapState } from 'vuex'
  import DocumentAttributes from './DocumentAttributes';
  import TranscriptionEditor from '../forms/fields/TranscriptionEditor';
  export default {
    name: 'DocumentTranscription',
    components: {TranscriptionEditor, DocumentAttributes},
    props: {
      editable: {
        type: Boolean,
        default: false
      },
    },
    created() {
      this.transcriptionContent = this.document.transcription;
      this.notesContent = this.notes;
    },
    computed: {
      ...mapState('document', ['document', 'notes'])
    }
  }
</script>

<style scoped>
  .notes {
    margin-top: 40px;
    margin-bottom: 40px;
    padding-top: 20px;
    border-top: solid 1px darkgrey;
    color: grey;
  }
  .section {
    padding-top: 24px;
    padding-bottom: 24px;
  }
</style>