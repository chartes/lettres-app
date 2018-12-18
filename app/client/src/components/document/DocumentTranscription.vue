<template>
  <section class="document__transcription section">
    <br/>
    <header class="title">
      <h3 class="document__transcription--title subtitle">Transcription</h3>
    </header>
    <div class="document__transcription--content">
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
    computed: {
      ...mapState('document', ['document'])
    }
  }
</script>

<style scoped>

</style>