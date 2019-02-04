<template>
  <div class="document">

    <article v-if="document" class="document__content">
      <div class="columns">
        <div class="column">
          <document-notice/>
          <document-correspondents/>
          <document-transcription/>
        </div>
        <div class="column is-one-quarter">

        </div>
      </div>
      <div style="margin-left: 0px;">
        <changelog v-if="current_user" v-bind:compact="true" :doc-id="doc_id" page-size="10"/>
      </div>
    </article>

    <loading-indicator :active="documentLoading" :full-page="true"/>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import LoadingIndicator from './ui/LoadingIndicator';
  import Changelog from './sections/Changelog';
  import DocumentNotice from './document/DocumentNotice';
  import DocumentCorrespondents from './document/DocumentCorrespondents';
  import DocumentTranscription from './document/DocumentTranscription';

  export default {

    name: 'Document',
    components: {Changelog, DocumentCorrespondents, DocumentNotice, DocumentTranscription, LoadingIndicator},
    props: {
      "doc_id" : {required: true}
    },
    created () {
      this.$store.dispatch('user/fetchCurrent').then(response => {
        this.$store.dispatch('document/fetch', this.doc_id);
      });
    },
    computed: {
      ...mapState('document', ['document', 'documentLoading']),
      ...mapState('user', ['current_user']),
    }
  }
</script>

