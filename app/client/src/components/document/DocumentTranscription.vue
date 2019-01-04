<template>
  <section v-if="document.transcription.length > 0" class="document__transcription section">
    <br/>
    <header class="title">
      <h2 class="document__transcription--title subtitle">Transcription</h2>
    </header>

    <div class="document__transcription--content" v-html="transcriptionContent">
    </div>
    <ol v-if="notesContent.length > 0" class="document__notes--content notes">
       <li  v-for="(note, index) in notesContent" v-html="note.content" :id="index + 1">
       </li>
    </ol>
  </section>
</template>

<script>

  import { mapState } from 'vuex'
  import DocumentAttributes from './DocumentAttributes';
  export default {
    name: 'DocumentTranscription',
    components: {DocumentAttributes},
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