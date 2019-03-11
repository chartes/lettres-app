<template>
    <home-page :doc-id="docId" :searched-term="searchedTerm" :user-template="userTemplate"/>
</template>

<script>
  import HomePage from './components/HomePage';
  export default {
      props: {
          docId: {type: Number, default: null},
          searchedTerm: {type: String, default: null},
          userTemplate: {type: String, default: null},
      },
    components: {HomePage}
  }
</script>

<style lang="scss">
  @import "styles/styles.scss";
</style>