<template>
    <span class="badge" :class="myclasses" @click="toggle">
        <font-awesome-icon :icon="[isActive ? 'fas' : 'far', fontawesomeIcon]"/>
    </span>
</template>

<script>
  export default {
    name: "badge",
    props: {
        fontawesomeIcon: {required: true},
        classesActive: {},
        classesInactive: {},
        actionWhenOn: {},
        actionWhenOff: {},
        startsOn: {default: false}
    },
    data() {
        return {
          isActive : this.startsOn
        }
    },
    created(){
      this.isActive = this.startsOn;
    },
    computed: {
        myclasses() {return this.isActive ? this.classesActive: this.classesInactive},
    },
    methods: {
        toggle() {
           if (this.isActive) {
               if (!this.actionWhenOff) {
                   this.isActive = false;
                   return
               }
               this.actionWhenOff().then(resp => {
                   this.isActive = false;
               }).catch(resp => {
                   console.warn(resp);
               });
           } else {
               if (!this.actionWhenOn) {
                   this.isActive = true;
                   return
               }
               this.actionWhenOn().then(resp => {
                   this.isActive = true;
               }).catch(resp => {
                   console.warn(resp);
               });
           }
        }
    }
  }
</script>

<style scoped>
    .badge:hover {
        cursor: pointer;
    }
</style>