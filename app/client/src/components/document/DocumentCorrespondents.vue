<template>
  <section v-if="correspondents.length > 0" class="document__correspondents section">
    <header>
      <h2 class="subtitle">Correspondants</h2>
    </header>
    <ul>
      <li v-for="c in correspondents" :key="c.correspondent.id">
        <a :href="c.correspondent.ref" target="_blank">{{ c.correspondent.firstname + ' ' + c.correspondent.lastname }}</a> <span class="tag">{{ c.role.label }}</span>
      </li>
    </ul>
  </section>
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
  h2 {
    margin-top: 20px;
  }
  .section {
    padding-top: 10px;
    padding-bottom: 10px;
  }
</style>