<template>
  <div class="document__notice">

    <document-attributes :editable="editable" class="document__subsection"/>

    <document-witnesses :editable="editable" class="document__subsection" :list="witnesses"/>

    <document-collections :editable="editable" class="document__subsection"/>

    <document-argument :editable="editable" class="document__subsection"/>

  </div>
</template>

<script>

  import { mapState } from 'vuex'
  import DocumentAttributes from './DocumentAttributes';
  import DocumentWitnesses from './DocumentWitnesses';
  import DocumentTagBar from "./DocumentTagBar";
  import DocumentCollections from './DocumentCollections';
  import DocumentArgument from './DocumentArgument';

  export default {
    name: 'DocumentNotice',
    components: {DocumentArgument, DocumentCollections, DocumentWitnesses, DocumentAttributes, DocumentTagBar},
    props: {
      data: {
        type: Object,
        default: null,
      },
      editable: {
        type: Boolean,
        default: false
      },
    },
    computed: {
      ...mapState('document', ['document', 'collections', 'witnesses', 'currentLock']),
      ...mapState('user', ['current_user'])
    },
    created() {
        this.titleContent = this.document.title;
    }
  }
</script>

<style scoped>
  h2 {
    margin: 1rem 0 .5rem 0;
  }
</style>