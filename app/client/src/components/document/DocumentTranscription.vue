<template>
  <section v-if="document.transcription.length > 0" class="document__transcription section">
    <br/>
    <header class="title">
      <h2 class="document__transcription--title subtitle">Transcription</h2>
    </header>
    <div class="document__transcription--content" v-html="HTMLContent">
        {{ document.transcription }}
    </div>
  </section>
</template>

<script>

  import { mapState } from 'vuex'
  import DocumentAttributes from './DocumentAttributes';
  export default {
    name: 'DocumentTranscription',
    components: {DocumentAttributes},
    created() {
      this.HTMLContent = this.document.transcription;
    },
    computed: {
      ...mapState('document', ['document'])
    }
  }
</script>

<style scoped>

</style>