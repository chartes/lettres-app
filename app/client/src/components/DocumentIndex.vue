<template>
  <section class="documents">
    <ul>
      <li v-for="doc in documents" :key="doc.id">
        <document-preview-card :doc_id="doc.id"></document-preview-card>
      </li>
    </ul>
    <loading-indicator :active="documentLoading" :full-page="true"/>
  </section>
</template>

<script>
  import { mapState } from 'vuex'
  import LoadingIndicator from './ui/LoadingIndicator';
  import DocumentPreviewCard from './DocumentPreviewCard';

  export default {

    name: 'DocumentIndex',
    components: {DocumentPreviewCard, LoadingIndicator},
    props: ["page_id"],
    created () {
      this.$store.dispatch('document/fetchAll', this.page_id);
      /*this.$store.dispatch('user/setAuthToken', this.auth_token).then(() => {
          this.$store.dispatch('user/getCurrentUser').then(() => {
            return this.$store.dispatch('document/fetch', this.doc_id)
          });
      });
       */
    },
    computed: {
      ...mapState('document', ['documents', 'documentLoading'])
    }
  }
</script>

<style scoped>

</style>