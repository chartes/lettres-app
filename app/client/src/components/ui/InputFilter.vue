<template>
    <span>
        <button class="button is-white" @click="toggle">{{label}}<i class="fas fa-filter"></i></button>
        <input class="input is-small"
               v-if="isActive"
               v-model="filterValue"
               :placeholder="placeHolder"
               @change="action(filterValue)"
        />
    </span>
</template>

<script>
  export default {
    name: "input-filter",
    props: {
        label: {required: true},
        placeHolder: {default: ''},
        action: {required: true}
    },
    data() {
        return {
            filterValue: null,
            isActive: false,
        }
    },
    computed: {

    },
    methods: {
        toggle() {
            this.isActive = !this.isActive;
            if (!this.isActive) {
                this.filterValue = null;
                this.action(this.filterValue);
            }
        }
    }
  }
</script>

<style scoped>
  .fa-filter {
   color: darkslategrey;
   height: 14px;
   margin-left: 12px;

  }

</style>