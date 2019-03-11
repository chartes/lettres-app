<template>
  <div>
    <pagination :current="currentPage" :end="nbPages" :size="pageSize" :action="goToPage">
      <ul id="preview-cards" >
        <li v-for="doc in documents" :key="doc.id">
          <document-preview-card
              :doc_id="doc.id"
              v-if="doc.attributes['is-published'] || current_user">
          </document-preview-card>
        </li>
      </ul>
    </pagination>
  </div>
</template>

<script>
  import DocumentPreviewCard from '../DocumentPreviewCard';
  import Pagination from '../ui/Pagination';
  import { mapState } from 'vuex';

  export default {
    name: "document-list",
    components: {DocumentPreviewCard, Pagination},
    props: {
      currentPage: {type: Number, default: 1} ,
      nbPages: {type: Number, default: 1},
      pageSize : {type: Number,required: true},
      goToPage : {type: Function, required: true},
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
      ...mapState('document', ['documents', 'links', 'documentLoading']),
      ...mapState('user', ['current_user']),
    }
  }
</script>

<style scoped>

</style>
