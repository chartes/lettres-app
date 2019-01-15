<template>
  <documentIndex page_id="1" page_size="10"></documentIndex>
</template>

<script>
  import DocumentIndex from './components/DocumentIndex';
  export default {
    props: ['auth_token'],
    components: {DocumentIndex}
  }
</script>

<style>

</style>
