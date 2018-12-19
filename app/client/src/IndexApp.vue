<template>
  <documentIndex page_id="1" page_size="20"></documentIndex>
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
