<template>
  <p><label>{{ label }} {{ addColons ? ':' : ''}}</label></p>
</template>

<script>
  export default {
    name: 'FieldLabel',
    props: {
      label: {
        type: String,
        required: true,
      },
      addColons : {
          type: Boolean,
          default: true
      }
    }
  }
</script>

<style scoped>

</style>