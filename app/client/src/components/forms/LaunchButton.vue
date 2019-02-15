<template>
  <button class="button" @click="clickHandler">{{label}}</button>
</template>

<script>
  export default {
    name: 'LaunchButton',
    props: { label:String, required: true},
    methods: {
      clickHandler () {
        this.$el.blur()
        this.$emit('click')
      }
    }
  }
</script>

<style scoped>

</style>