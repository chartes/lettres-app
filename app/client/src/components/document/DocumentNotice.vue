<template>
  <section class="document__notice section">

    <header class="title">
      <h1 class="title">{{ document.title }}</h1>
    </header>

    <document-attributes></document-attributes>

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
      ...mapState('document', ['document'])
    }
  }
</script>

<style scoped>
  h1.title {
    font: 90%/140% 'Oxygen', sans-serif;
  }
</style>