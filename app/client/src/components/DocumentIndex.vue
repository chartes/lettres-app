<template>
  <section class="documents">
    <ul>
      <li v-for="doc in documents" :key="doc.id">

      </li>
    </ul>
    <loading-indicator :active="documentLoading" :full-page="true"/>
  </section>
</template>

<script>
  import { mapState } from 'vuex'
  import LoadingIndicator from './ui/LoadingIndicator';

  export default {

    name: 'DocumentIndex',
    components: {LoadingIndicator},
    props: [],
    created () {
      this.$store.dispatch('document/fetchAll');
      /*this.$store.dispatch('user/setAuthToken', this.auth_token).then(() => {
          this.$store.dispatch('user/getCurrentUser').then(() => {
            return this.$store.dispatch('document/fetch', this.doc_id)
          });
      });
       */
    },
    computed: {
      ...mapState('document', ['documents', 'documentLoading'])
    }
  }
</script>

<style scoped>

</style>