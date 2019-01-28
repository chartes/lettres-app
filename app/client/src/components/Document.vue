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

          <section class="changes-section section" v-if="changelog.documents">
            <header>
              <h2 class="section__title subtitle">Historique des modifications</h2>
            </header>
            <article class="changes-section__content">
              <ol>
                <ul v-for="change in changelog.documents" :key="change.data.id">
                  <span>{{change.data.attributes["event-date"]}}</span>
                  <span>{{change.data.attributes["description"]}}</span>
                  <span class="tag">{{change.user.username}}</span>
                </ul>
              </ol>
            </article>
          </section>
        </div>
      </div>

    </article>

    <loading-indicator :active="documentLoading" :full-page="true"/>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import LoadingIndicator from './ui/LoadingIndicator';
  import DocumentNotice from './document/DocumentNotice';
  import DocumentCorrespondents from './document/DocumentCorrespondents';
  import DocumentTranscription from './document/DocumentTranscription';

  export default {

    name: 'Document',
    components: {DocumentCorrespondents, DocumentNotice, DocumentTranscription, LoadingIndicator},
    props: {
      "doc_id" : {required: true}
    },
    created () {
      this.$store.dispatch('user/fetchCurrent').then(response => {

        this.$store.dispatch('document/fetch', this.doc_id);

        if (this.current_user) {
          this.$store.dispatch('changelog/fetchObjectChanges', {objectType: 'documents', objectId: this.doc_id});
        }
      });
    },
    computed: {
      ...mapState('document', ['document', 'documentLoading']),
      ...mapState('user', ['current_user']),
      ...mapState('changelog', ['changelog'])
    }
  }
</script>

<style scoped>
  .changes-section {
    color: #962D3E;
    font-size: small;
  }
  .section__title {
    margin-bottom: 20px;
    color: #962D3E;
  }
</style>