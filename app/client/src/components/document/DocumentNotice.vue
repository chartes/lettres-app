<template>
  <section class="document__notice section">

    <header class="title">
      <h1 class="title">{{ document.title }}</h1>
    </header>

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
        <p><a :href="institution.name" target="_blank" v-if="!!institution">{{ institution.name }}</a></p>
      </div>
      <div class="column is-one-third">
        <p><label>Tradition :</label></p>
        <p v-if="!!tradition">{{ tradition.label }}</p>
      </div>
      <div class="column is-one-third">
        <p><label>Langues :</label></p>
        <p v-if="!!languages">{{ languagesConcat }}</p>
      </div>
    </div>

    <div class="document__argument">

      <h3 class="document__argument--title subtitle">Argument</h3>
      <div class="document__argument--content">
        {{ document.argument }}
      </div>

    </div>

  </section>
</template>

<script>

  import { mapState } from 'vuex'
  import DocumentAttributes from './DocumentAttributes';
  export default {
    name: 'DocumentNotice',
    components: {DocumentAttributes},
    props: {
      data: {
        type: Object,
        default: null,
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