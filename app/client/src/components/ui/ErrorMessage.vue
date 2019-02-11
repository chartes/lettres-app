<template>
  <div v-if="error" class="notification is-danger">
    {{error}}
  </div>
</template>

<script>
  export default {
    name: 'ErrorMessage',
    props: {
      error: { type: String, default: null }
    }
  }
</script>

<style scoped>

</style>