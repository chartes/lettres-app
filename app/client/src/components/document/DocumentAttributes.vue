<template>
  <div class="document__attributes columns is-multiline">

      <div class="column is-one-third">
        <p><label>witness-label :</label></p>
        <p v-if="!!document['witness-label']" v-html="document['witness-label']"></p>
        <p v-else class="unknown">Inconnu</p>
      </div>
      <div class="column is-one-third">
        <p><label>classification-mark :</label></p>
        <p v-if="!!document['classification-mark']" v-html="document['classification-mark']"></p>
        <p v-else class="unknown">Inconnue</p>
      </div>
      <div class="column is-one-third">
        <p><label>creation :</label></p>
        <p v-if="!!document['creation']" >{{ document['creation'] }}</p>
        <p v-else class="unknown">Inconnue</p>
      </div>
      <div class="column is-one-third">
        <p><label>creation-label :</label></p>
        <p v-if="!!document['creation-label']" v-html="document['creation-label']"></p>
        <p v-else class="unknown">Inconnue</p>
      </div>
      <div class="column is-one-third">
        <p><label>location-date-label :</label></p>
        <p v-if="!!document['location-date-label']" v-html="document['location-date-label']"></p>
        <p v-else class="unknown">Inconnue</p>
      </div>
      <div class="column is-one-third">
        <p><label>location-date-ref :</label></p>
        <p v-if="!!document['location-date-ref']" v-html="document['location-date-ref']"></p>
        <p v-else class="unknown">Inconnue</p>
      </div>
      <div class="column is-one-third">
        <p><label>Institution :</label></p>
        <p v-if="!!institution.id"><a :href="institution.name" target="_blank">{{ institution.name }}</a></p>
        <p v-else class="unknown">Inconnue</p>
      </div>
      <div class="column is-one-third">
        <p><label>Tradition :</label></p>
        <p v-if="!!tradition.id">{{ tradition.label }}</p>
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
      ...mapState('document', ['document', 'institution', 'tradition', 'languages']),
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