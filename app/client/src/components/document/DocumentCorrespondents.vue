<template>
  <div class="document__correspondents section">

    <h3 class="subtitle">Correspondants</h3>

    <ul>
      <li v-for="c in correspondents" :key="c.correspondent.id">
        <a :href="c.correspondent.ref" target="_blank">{{ c.correspondent.firstname + ' ' + c.correspondent.lastname }}</a> <span class="tag">{{ c.role.label }}</span></li>
    </ul>

  </div>
</template>

<script>

  import { mapState } from 'vuex'
  export default {
    name: 'DocumentCorrespondents',
    computed: {
      ...mapState('document', ['correspondents'])
    }
  }

</script>

<style scoped>

</style>