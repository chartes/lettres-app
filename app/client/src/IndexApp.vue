<template>
    <div id="app">
        <documentIndex></documentIndex>
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
