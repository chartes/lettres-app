<template>
  <documentIndex :page_id="page_id" :page_size="page_size" :user_id="user_id"></documentIndex>
</template>

<script>
  import DocumentIndex from './components/DocumentIndex';
  export default {
    props: ["page_id", "page_size", "user_id"],
    components: {DocumentIndex}
  }
</script>

<style>

</style>
