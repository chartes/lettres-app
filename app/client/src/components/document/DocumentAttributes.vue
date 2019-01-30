<template>
  <div class="document__attributes columns is-multiline">
    <div class="column is-one-third">
      <date-field
              :tabulation-index="0"
              label="creation"
              name="creation"
              not-set="Inconnue"
              :initial-value="document['creation']"
              :editable="userCanEdit"
              v-on:changed="fieldChanged"/>
    </div>
    <div class="column is-one-third">
      <date-field
              :tabulation-index="0"
              label="creation-not-after"
              name="creation-not-after"
              :initial-value="document['creation-not-after']"
              :editable="userCanEdit"
              v-on:changed="fieldChanged"/>
    </div>
    <div class="column is-one-third">
      <text-field
              :tabulation-index="0"
              label="creation-label"
              name="creation-label"
              not-set="Inconnue"
              :initial-value="document['creation-label']"
              :editable="userCanEdit"
              v-on:changed="fieldChanged"/>
    </div>
    <div class="column is-one-third">
      <text-field
              :tabulation-index="0"
              label="Date de lieu d'expédition"
              name="location-date-from-ref"
              not-set="Inconnue"
              :initial-value="document['location-date-from-ref']"
              :editable="userCanEdit"
              v-on:changed="fieldChanged"/>
    </div>
    <div class="column is-one-third">
      <text-field
              :tabulation-index="0"
              label="Date de lieu de réception"
              name="location-date-to-ref"
              not-set="Inconnue"
              :initial-value="document['location-date-to-ref']"
              :editable="userCanEdit"
              v-on:changed="fieldChanged"/>
    </div>
    <div class="column is-one-third">
      <multiselect-field
              :editable="userCanEdit"
              label="Langue(s)"
              :optionsList="allLanguages"
              :selectedItems="languages"
              :onChange="languagesChanged"/>
    </div>
  </div>
</template>
<script>
  import { mapState } from 'vuex';
  import TextField from '../forms/fields/TextField';
  import MultiselectField from '../forms/fields/MultiselectField';
  import DateField from '../forms/fields/DateField';

  export default {
    name: 'DocumentAttributes',
    components: {DateField, MultiselectField, TextField },
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
        console.log("fieldChanged", fieldProps);
        const data = { id: this.document.id, attributes: {} };
        data.attributes[fieldProps.name] = fieldProps.value;
        this.$store.dispatch('document/save', data)

      },
      languagesChanged () {
        console.log("languagesChanged")
      }
    },
    computed: {
      ...mapState('document', ['document', 'languages']),
      ...mapState({
        allLanguages: state => state.languages.languages
      }),
      languagesConcat: function () {
        return this.languages.map(lang => lang.label).join(', ')
      },
      languagesIds () {
        console.log("languageIds", this.document)
        return this.languages.map((lang) => lang.id)
      }
    }
  }
</script>

<style scoped>
</style>