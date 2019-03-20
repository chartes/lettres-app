<template>
    <main-layout :section="section" :data="data"/>
</template>

<script>
  import MainLayout from './components/MainLayout';
  export default {
      props: {
          section: {type: String, default: null},
          data: {type: Object, default: () => {return {}}}
      },
    components: {MainLayout}
  }
</script>

<style lang="scss">
  @import "styles/styles.scss";
</style>