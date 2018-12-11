<template>
  <div class="document">
    <div v-if="document" class="document__content">
      <div class="columns">
        <div class="column">

          <document-notice/>
          <document-correspondents/>
          <document-traditions/>

        </div>
        <div class="column  is-one-fifth">
          Second column
        </div>
      </div>
    </div>
    <loading-indicator :active="documentLoading" :full-page="true"/>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import LoadingIndicator from './ui/LoadingIndicator';
  import DocumentNotice from './document/DocumentNotice';
  import DocumentCorrespondents from './document/DocumentCorrespondents';
  import DocumentTraditions from './document/DocumentTraditions';

  export default {

    name: 'Document',
    components: {DocumentTraditions, DocumentCorrespondents, DocumentNotice, LoadingIndicator},
    props: ['doc_id'],
    created () {
      this.$store.dispatch('document/fetch', this.doc_id)
      /*this.$store.dispatch('user/setAuthToken', this.auth_token).then(() => {
          this.$store.dispatch('user/getCurrentUser').then(() => {
            return this.$store.dispatch('document/fetch', this.doc_id)
          });
      });
       */
    },
    computed: {
      ...mapState('document', ['document', 'documentLoading'])
    }
  }
</script>

<style scoped>

</style>