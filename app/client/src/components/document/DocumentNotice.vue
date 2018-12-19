<template>
  <section class="document__notice section">

    <header class="title">
      <h1 class="title">{{ document.title }}</h1>
    </header>

    <document-attributes></document-attributes>
    <!-- v-if="document.collections && document.collections.length > 0" -->
    <div class="document__collections" v-if="collections.length > 0">
      <h2 class="document__collections--title subtitle">Collections</h2>
      <div class="document__collections--content">
        <ul v-for="collection in collections">
          <li><a href="#">{{collection.title}}</a></li>
        </ul>
      </div>
    </div>

    <div class="document__argument">
      <h2 class="document__argument--title subtitle">Argument</h2>
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
      ...mapState('document', ['document', 'collections'])
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