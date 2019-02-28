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
        v-model="currentValue"
        @keyup.enter="action(currentValue)"
    ></v-text-field>
  </div>
</template>

<script>

    export default {
        name: "search-box",
        components: {},
        props: {
            action: { required: true },
            value: {type: String, default: ""},
            loading: {
                type: Boolean,
                default: false
            },
        },
        data() {
            return {
                currentValue: this.$props.value
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
