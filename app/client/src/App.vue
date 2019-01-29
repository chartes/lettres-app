<template>
    <div id="app">
        <document :doc_id="doc_id"></document>
    </div>
</template>

<script>
  import Document from './components/Document';
  export default {
    props: {
      doc_id : {required: true}
    },
    components: {Document}
  }
</script>

<style lang="scss">
    @import "styles/styles.scss";
</style>