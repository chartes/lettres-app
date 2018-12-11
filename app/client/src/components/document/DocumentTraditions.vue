<template>
  <div class="document__traditions section">

    <h3 class="subtitle">traditions</h3>

    <ul>
      <li v-for="t in traditions" :key="t.id">
        <a :href="t.ref" target="_blank">{{ t.firstname + ' ' + t.lastname }}</a> <span class="tag">{{ t.label }}</span></li>
    </ul>

  </div>
</template>

<script>

  import { mapState } from 'vuex'
  export default {
    name: 'DocumentTraditions',
    computed: {
      ...mapState('document', ['traditions'])
    }
  }

</script>

<style scoped>

</style>