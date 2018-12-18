<template>
    <div id="app">
        <documentIndex page_id="1"></documentIndex>
    </div>
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
