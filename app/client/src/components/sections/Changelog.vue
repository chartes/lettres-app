<template>
   <section>
      <header v-if="!compact">
         <h2 class="section__title subtitle">Historique des modifications</h2>
      </header>

      <table class="table is-narrow" :class="!compact ? 'is-bordered is-striped is-hoverable' : ''">
        <thead :class="compact ? 'is-invisible' : ''">
          <tr>
             <th>Date</th>
             <th v-if="!compact">Objet</th>
             <th>Description</th>
             <th>Utilisateur</th>
          </tr>
        </thead>
         <tbody v-for="change in data" :key="change.id">
            <changelog-entry v-bind:compact="compact" :entry="change.data" :user="change.user"/>
         </tbody>
      </table>

   </section>
</template>

<script>
  import ChangelogEntry from '../ui/ChangelogEntry';

  export default {
    name: "changelog",
    components : {ChangelogEntry},
    props: {
      data: {required: true},
      compact: {default: false}
    },
    data () {
      return {

      }
    },
    created() {
    },
    computed: {

    }
  }
</script>

<style scoped>
  .section__title {
    margin-bottom: 20px;
  }
</style>
