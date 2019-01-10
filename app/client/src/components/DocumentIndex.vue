<template>
  <div>
    <section class="documents-index columns">
      <aside class="documents-index__collections column is-2">
        <h2 class="documents-index__collections__title title is-size-3">Collections</h2>
      </aside>
      <section class="column documents-index__preview-column">
          <pagination :current="currentPage" :end="nbPages" :size="page_size" :action="goToPage"/>
          <ul id="preview-cards" >
            <li v-for="doc in documents" :key="doc.id">
              <document-preview-card :doc_id="doc.id"></document-preview-card>
            </li>
          </ul>
          <pagination :current="currentPage" :end="nbPages" :size="page_size" :action="goToPage"/>
      </section>
    </section>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import DocumentPreviewCard from './DocumentPreviewCard';
  import Pagination from './ui/Pagination';

  function getUrlParameter(url, paramName) {
    paramName = paramName.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + paramName + '=([^&#]*)');
    var results = regex.exec(url);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
  }

  export default {

    name: 'DocumentIndex',
    components: {DocumentPreviewCard, Pagination},
    props: ["page_id", "page_size"],
    created () {
      this.goToPage(1);
      /*this.$store.dispatch('user/setAuthToken', this.auth_token).then(() => {
          this.$store.dispatch('user/getCurrentUser').then(() => {
            return this.$store.dispatch('document/fetch', this.doc_id)
          });
      });
       */
    },
    computed: {
      ...mapState('document', ['documents', 'links']),
      nbPages() {
          return parseInt(this.links.last ? getUrlParameter(this.links.last, "page%5Bnumber%5D") : 1);
      }
    },
    methods: {
        goToPage(num){
            this.currentPage = num;
            this.$store.dispatch('document/fetchAll', {pageId: num, pageSize: this.page_size});
        }
    }
  }
</script>

<style scoped>
  .documents-index {
    padding-top: 40px;
    background: #FFFFFF;
  }

  .documents-index__collections {
      margin-left: 14px;
  }
  .documents-index__collections__title {
    font: 90%/140% 'Oxygen', sans-serif;
  }
  .documents-index__preview-column {
      padding-bottom: 80px;
  }
</style>