<template>
  <section class="document__notice section">

    <document-attributes :editable="editable"/>

    <document-witnesses :editable="editable" :list="witnesses"/>

    <document-collections :editable="editable"/>

    <div v-if="!!document.argument" class="document__argument">
      <header>
        <h2 class="document__argument--title subtitle">Argument</h2>
      </header>
        <div class="document__argument--content">
        {{ document.argument }}
      </div>
    </div>

  </section>
</template>

<script>

  import { mapState } from 'vuex'
  import DocumentAttributes from './DocumentAttributes';
  import DocumentWitnesses from './DocumentWitnesses';
  import DocumentTagBar from "./DocumentTagBar";
  import DocumentCollections from './DocumentCollections';

  export default {
    name: 'DocumentNotice',
    components: {DocumentCollections, DocumentWitnesses, DocumentAttributes, DocumentTagBar},
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