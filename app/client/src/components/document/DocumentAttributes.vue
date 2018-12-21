<template>
  <div class="document__attributes columns is-multiline">

      <div class="column is-one-third">
        <p><label>witness-label :</label></p>
        <p>{{ document['witness-label'] }}</p>
      </div>
      <div class="column is-one-third">
        <p><label>classification-mark :</label></p>
        <p>{{ document['classification-mark'] }}</p>
      </div>
      <div class="column is-one-third">
        <p><label>creation :</label></p>
        <p>{{ document['creation'] }}</p>
      </div>
      <div class="column is-one-third">
        <p><label>creation-label :</label></p>
        <p>{{ document['creation-label'] }}</p>
      </div>
      <div class="column is-one-third">
        <p><label>location-date-label :</label></p>
        <p>{{ document['location-date-label'] }}</p>
      </div>
      <div class="column is-one-third">
        <p><label>location-date-ref :</label></p>
        <p>{{ document['location-date-ref'] }}</p>
      </div>
      <div class="column is-one-third">
        <p><label>Institution :</label></p>
        <p v-if="!!institution.id"><a :href="institution.name" target="_blank">{{ institution.name }}</a></p>
        <p v-else>Inconnue</p>
      </div>
      <div class="column is-one-third">
        <p><label>Tradition :</label></p>
        <p v-if="!!tradition.id">{{ tradition.label }}</p>
        <p v-else>Inconnue</p>
      </div>
      <div class="column is-one-third">
        <p><label>Langues :</label></p>
        <p v-if="languages.length > 0" >{{ languagesConcat }}</p>
        <p v-else>Inconnues</p>
      </div>
    </div>
</template>
<script>
  import { mapState } from 'vuex';

  export default {
    name: 'DocumentAttributes',
    props: {
      data: {
        type: Object,
        default: null
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

</style>