<template>
  <p><label>{{ label }} :</label></p>
</template>

<script>
  export default {
    name: 'FieldLabel',
    props: {
      label: {
        type: String,
        required: true,
      }
    }
  }
</script>

<style scoped>

</style>