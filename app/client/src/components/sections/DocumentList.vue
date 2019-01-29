<template>
  <div>
    <pagination :current="currentPage" :end="nbPages" :size="pageSize" :action="onPageChange"/>
      <ul id="preview-cards" >
        <li v-for="doc in documents" :key="doc.id">
          <document-preview-card :doc_id="doc.id"></document-preview-card>
        </li>
      </ul>
    <pagination :current="currentPage" :end="nbPages" :size="pageSize" :action="onPageChange"/>
  </div>
</template>

<script>
  import DocumentPreviewCard from '../DocumentPreviewCard';
  import Pagination from '../ui/Pagination';

  export default {
    name: "document-list",
    components: {DocumentPreviewCard, Pagination},
    props: {
      documents: {required: true},

      currentPage : {default:1},
      nbPages: {required: true},
      pageSize : {required: true},
      onPageChange: {required: true}
    },
    data () {
      return {

      }
    },
    created() {
    },
    methods: {

    },
    computed: {

    }
  }
</script>

<style scoped>

</style>
