<template>
  <div>
    <search-box :action="performSearch" :loading="documentLoading"/>
    <pagination :current="currentPage" :end="nbPages" :size="pageSize" :action="goToDocPage"/>
      <ul id="preview-cards" >
        <li v-for="doc in documents" :key="doc.id">
          <document-preview-card :doc_id="doc.id"></document-preview-card>
        </li>
      </ul>
    <pagination :current="currentPage" :end="nbPages" :size="pageSize" :action="goToDocPage"/>
  </div>
</template>

<script>
  import DocumentPreviewCard from '../DocumentPreviewCard';
  import Pagination from '../ui/Pagination';
  import SearchBox from '../ui/SearchBox';
  import { mapState } from 'vuex';

  function getUrlParameter(url, paramName) {
    paramName = paramName.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    const regex = new RegExp('[\\?&]' + paramName + '=([^&#]*)');
    let results = regex.exec(url);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
  }

  export default {
    name: "document-list",
    components: {DocumentPreviewCard, Pagination, SearchBox},
    props: {
      pageSize : {required: true},
    },
    data () {
      return {
        currentPage: 1
      }
    },
    created() {
      this.goToDocPage(parseInt(this.currentPage));
    },
    methods: {
      goToDocPage(num){
          this.currentPage = num;
          if (document.getElementById("search-box") && document.getElementById("search-box").value) {
            this.performSearch(this.currentPage);
          } else {
            this.$store.dispatch('document/fetchAll', {pageId: num, pageSize: this.pageSize});
          }
        },
      performSearch(numPage = 1){
        const term = document.getElementById("search-box").value;
        if (term.length > 2) {
          this.$store.dispatch('document/fetchSearch', {pageId: numPage, pageSize: this.pageSize, query: term});
          this.currentPage = numPage;
        }
      }
    },
    computed: {
      ...mapState('document', ['documents', 'links', 'documentLoading']),

      nbPages() {
        return parseInt(this.links.last ? getUrlParameter(this.links.last, "page%5Bnumber%5D") : 1);
      }
    }
  }
</script>

<style scoped>

</style>
