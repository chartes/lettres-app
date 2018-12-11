<template>
    <div id="app">
        <document :doc_id="doc_id"></document>
    </div>
</template>

<script>
  import Document from './components/Document';
  export default {
    props: ['doc_id', 'auth_token'],
    components: {Document}
  }
</script>

<style>
</style>
