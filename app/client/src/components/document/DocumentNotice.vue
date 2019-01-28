<template>
  <section class="document__notice section">

    <header class="title">
      <span class="tag doc-tag">Document {{document.id}}</span>
      <span><h1 class="title" v-html="titleContent"></h1></span>
    </header>

    <document-attributes></document-attributes>

    <!-- TODO: placer les composants document-witness ici -->
    <div class="document__witnesses" v-if="witnesses.length > 0">
      <header>
        <h2 class="document__witnesses--title subtitle">Témoins</h2>
      </header>
      <div class="document__witnesses--content">
        <ul v-for="witness in witnesses">
          <li><span v-html="witness.content"></span></li>
        </ul>
      </div>
    </div>

    <div class="document__collections" v-if="collections.length > 0">
      <header>
        <h2 class="document__collections--title subtitle">Collections</h2>
      </header>
      <div class="document__collections--content">
        <ul v-for="collection in collections">
          <li><a href="#">{{collection.title}}</a></li>
        </ul>
      </div>
    </div>

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
  export default {
    name: 'DocumentNotice',
    components: {DocumentAttributes},
    props: {
      data: {
        type: Object,
        default: null,
      }
    },
    computed: {
      ...mapState('document', ['document', 'collections', 'witnesses'])
    },
    created() {
        this.titleContent = this.document.title;
    }
  }
</script>

<style scoped>
  h1.title {
    font: 90%/140% 'Oxygen', sans-serif;
    margin-bottom: 40px;
  }
  h2 {
    margin-top: 20px;
  }
</style>