<template>
  <div class="document__attributes columns is-multiline">
    <div class="column is-one-third">
      <p><label>creation :</label></p>
      <p v-if="!!document['creation']" >{{ document['creation'] }}</p>
      <p v-else class="unknown">Inconnue</p>
    </div>
      <div class="column is-one-third">
        <text-field
                label="creation-label"
                name="creation-label"
                not-set="Inconnue"
                :initial-value="document['creation-label']"
                :editable="userCanEdit"
                v-on:changed="fieldChanged"/>
      </div>
      <div class="column is-one-third">
        <text-field
              label="location-date-label"
              name="location-date-label"
              not-set="Inconnue"
              :initial-value="document['location-date-label']"
              :editable="userCanEdit"
              v-on:changed="fieldChanged"/>
      </div>
      <div class="column is-one-third">

        <p><label>location-date-ref :</label></p>
        <p v-if="!!document['location-date-ref']" v-html="document['location-date-ref']"></p>
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
  import TextField from '../forms/fields/TextField';

  export default {
    name: 'DocumentAttributes',
    components: {TextField},
    props: {
      editable: {
        type: Boolean,
        default: false
      },
      data: {

      },
    },
    data() {
      return {
        userCanEdit: true,
      }
    },
    methods: {
      fieldChanged (fieldProps) {
        console.log("fieldChanged", fieldProps)
        const data = { id: this.document.id }
        data[fieldProps.name] = fieldProps.value
        this.$store.dispatch('document/save', data)

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
</style>