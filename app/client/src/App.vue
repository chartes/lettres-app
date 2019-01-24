<template>
    <div id="app">
        <document :doc_id="doc_id" :user_id="user_id"></document>
    </div>
</template>

<script>
  import Document from './components/Document';
  export default {
    props: {
      "doc_id" : {type: Number, required: true},
      "user_id" : {type: Number}
    },
    components: {Document}
  }
</script>

<style>
</style>
