<template>
  <div>
    <section id="main" class="columns">
      <aside class="column is-2">
        <h2 class="title is-size-3">Collections</h2>
      </aside>
      <section class="column">
        <div class="documents__index ">
          <ul id="preview-cards" >
            <li v-for="doc in documents" :key="doc.id">
              <document-preview-card :doc_id="doc.id"></document-preview-card>
            </li>
          </ul>
        </div>
      </section>
    </section>

  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import DocumentPreviewCard from './DocumentPreviewCard';

  export default {

    name: 'DocumentIndex',
    components: {DocumentPreviewCard},
    props: ["page_id", "page_size"],
    created () {
      this.$store.dispatch('document/fetchAll', {pageId: this.page_id, pageSize: this.page_size});
      /*this.$store.dispatch('user/setAuthToken', this.auth_token).then(() => {
          this.$store.dispatch('user/getCurrentUser').then(() => {
            return this.$store.dispatch('document/fetch', this.doc_id)
          });
      });
       */
    },
    computed: {
      ...mapState('document', ['documents'])
    }
  }
</script>

<style scoped>
  #main {
    padding-top: 40px;
    background: #FFFFFF;
  }

  h2.title {
    font: 90%/140% 'Oxygen', sans-serif;
  }

  aside {
    margin-left: 14px;
  }
</style>