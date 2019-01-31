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
  import {getUrlParameter} from "../../modules/utils";

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
      fetchAll() {
        this.$store.dispatch('document/fetchAll', {pageId: this.currentPage, pageSize: this.pageSize});
      },
      goToDocPage(num){
          this.currentPage = num;
          if (document.getElementById("search-box") && document.getElementById("search-box").value) {
            this.performSearch(this.currentPage);
          } else {
            this.fetchAll();
          }
        },
      performSearch(numPage = 1){
        const term = document.getElementById("search-box").value;
        if (term.length > 1) {
          this.$store.dispatch('document/fetchSearch', {pageId: numPage, pageSize: this.pageSize, query: term});
          this.currentPage = numPage;
        } else {
          document.getElementById("search-box").value = null;
          this.goToDocPage(1);
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
