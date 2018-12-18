<template>
  <section class="document__preview-card">
    <article v-if="previewCard" class="document__content card">
      <header class="title card-header">
        <h1>{{previewCard.title}}</h1>
      </header>
      <div class="card-content">
        <div class="content">
            test
        </div>
      </div>
    </article>
    <loading-indicator :active="documentLoading" :full-page="true"/>
  </section>
</template>

<script>
  import { mapState } from 'vuex'
  import LoadingIndicator from './ui/LoadingIndicator';
  import DocumentAttributes from './document/DocumentAttributes';

  export default {

    name: 'DocumentPreviewCard',
    components: {DocumentAttributes, LoadingIndicator},
    props: ['doc_id'],
    created () {
      this.$store.dispatch('document/fetchPreview', this.doc_id)
      /*this.$store.dispatch('user/setAuthToken', this.auth_token).then(() => {
          this.$store.dispatch('user/getCurrentUser').then(() => {
            return this.$store.dispatch('document/fetch', this.doc_id)
          });
      });
       */
    },
    computed: {
      ...mapState('document', ['documentPreviewCards', 'documentLoading']),
        previewCard : function() {
          return this.documentPreviewCards[this.doc_id];
        }
    }
  }
</script>

<style scoped>

</style>