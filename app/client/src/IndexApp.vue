<template>
    <home-page v-if="section === 'documents'"
               :section="section"
               :template="template"
               :doc-id="docId"
               :searched-term="searchedTerm"/>
    <home-page v-else-if="section === 'collections'"
               :section="section"
               :template="template"/>
    <home-page v-else-if="section === 'errors'"
               :section="section"
               :template="template"/>
</template>

<script>
  import HomePage from './components/HomePage';
  export default {
      props: {
          section: {type: String, default: null},
          template: {type: String, default: null},
    
          docId: {type: Number, default: null},
          searchedTerm: {type: String, default: null},
      },
    components: {HomePage}
  }
</script>

<style lang="scss">
  @import "styles/styles.scss";
</style>