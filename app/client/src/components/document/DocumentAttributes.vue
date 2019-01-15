<template>
  <div class="document__attributes columns is-multiline">
      <div class="column is-one-third">
        <p><label>creation :</label></p>
        <p v-if="!!document['creation']" >{{ document['creation'] }}</p>
        <p v-else class="unknown">Inconnue</p>
      </div>
      <div v-if="!!document['creation-not-after']" class="column is-one-third">
        <p><label>Avant :</label></p>
        <p >{{ document['creation-not-after'] }}</p>
      </div>
      <div class="column is-one-third">
        <p><label>creation-label :</label></p>
        <p v-if="!!document['creation-label']" v-html="document['creation-label']"></p>
        <p v-else class="unknown">Inconnue</p>
      </div>
      <div class="column is-one-third">
        <p><label>Date de lieu de (émission) :</label></p>
        <p v-if="!!document['location-date-from-ref']" v-html="document['location-date-from-ref']"></p>
        <p v-else class="unknown">Inconnue</p>
      </div>
      <div class="column is-one-third">
        <p><label>Date de lieu de (réception) :</label></p>
        <p v-if="!!document['location-date-to-ref']" v-html="document['location-date-to-ref']"></p>
        <p v-else class="unknown">Inconnue</p>
      </div>
      <div class="column is-one-third">
        <p><label>Langues :</label></p>
        <p v-if="languages.length > 0" >{{ languagesConcat }}</p>
        <p v-else class="unknown">Inconnues</p>
      </div>
    </div>
</template>
<script>
  import { mapState } from 'vuex';

  export default {
    name: 'DocumentAttributes',
    props: {
      data: {

      }
    },
    computed: {
      ...mapState('document', ['document', 'languages']),
      languagesConcat: function () {
        return this.languages.map(lang => lang.label).join(', ')
      }
    }
  }
</script>

<style scoped>
    .unknown {
        color: grey;
    }
</style>