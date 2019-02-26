<template>
  <div class="search-container">
    <v-text-field
        flat
        solo-inverted
        hide-details
        prepend-inner-icon="search"
        label="Search"
        class="hidden-sm-and-down"
        type="text"
        placeholder="Catherine de Medicis"
        v-model="value"
        @keyup.enter="action(value)"
    ></v-text-field>
  </div>
</template>

<script>
    export default {
        name: "search-box",
        props: {
            action: { required: true },
            loading: {
                type: Boolean,
                default: false
            },
        },
        data() {
            return {
                value: null
            }
        },
        created() {
        
        }
    }
</script>

<style scoped>
  .search-container {
    width: 400px;
  }
</style>
