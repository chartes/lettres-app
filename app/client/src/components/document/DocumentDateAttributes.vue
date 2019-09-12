<template>
  <div class="document-date__attributes">

    <header class="document-date__attributes--title">
      <u>Dates de temps</u>
    </header>

    <div class="columns is-multiline" v-if="editAttributes">
      <div class="column is-one-third">
        <date-field
                :tabulation-index="0"
                label="Date de rédaction"
                name="creation"
                not-set="Inconnue"
                :initial-value="document['creation']"
                :editable="editable"
                v-on:changed="fieldChanged"/>
      </div>
      <div class="column is-one-third">
        <date-field
                :tabulation-index="0"
                label="Date de rédaction (rédigée avant le ...)"
                name="creation-not-after"
                :initial-value="document['creation-not-after']"
                :editable="editable"
                v-on:changed="fieldChanged"/>
      </div>
      <div class="column is-one-third">
        <text-field-in-place
                :tabulation-index="0"
                label="Date de rédaction (étiquette)"
                name="creation-label"
                not-set="Inconnue"
                :initial-value="document['creation-label']"
                :editable="editable"
                v-on:changed="fieldChanged"/>
      </div>
    </div>
  </div>
</template>
<script>
  import { mapState } from 'vuex';
  import TextFieldInPlace from '../forms/fields/TextFieldInPlace';
  import DateField from '../forms/fields/DateField';
  import DocumentPlacenames from "./DocumentPlacenames";

  export default {
    name: 'DocumentAttributes',
    components: {DateField, TextFieldInPlace, DocumentPlacenames },
    props: {
      editable: {
        type: Boolean,
        default: false
      },
      editAttributes: {
          type: Boolean, default: true
      }
    },
    data() {
      return {
        titleStatus: 'normal'
      }
    },
    methods: {
      fieldChanged (fieldProps) {
        const data = { id: this.document.id, attributes: {} };
        data.attributes[fieldProps.name] = fieldProps.value;
        this.$store.dispatch('document/save', data)
      },

    },
    computed: {
      ...mapState('document', ['document']),
    }
  }
</script>

<style scoped>
</style>
