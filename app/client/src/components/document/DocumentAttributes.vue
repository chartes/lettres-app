<template>
  <div class="document__attributes">

    <header class="document__attributes--title">
      <title-field-in-place
              :tabulation-index="0"
              label="Titre"
              name="title"
              not-set="Non renseigné"
              :initial-value="document.title"
              :editable="editable"
              :status="titleStatus"
              v-on:changed="titleChanged"
      />
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
      <div class="column">
        <multiselect-field
                :editable="editable"
                label="Langues"
                :optionsList="allLanguages"
                :selectedItems="languages"
                :onChange="languagesChanged"/>
      </div>
    </div>

  </div>
</template>
<script>
  import { mapState } from 'vuex';
  import TextFieldInPlace from '../forms/fields/TextFieldInPlace';
  import MultiselectField from '../forms/fields/MultiselectField';
  import DateField from '../forms/fields/DateField';
  import TitleFieldInPlace from '../forms/fields/TitleFieldInPlace';

  export default {
    name: 'DocumentAttributes',
    components: {TitleFieldInPlace,  DateField, MultiselectField, TextFieldInPlace },
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
      titleChanged (fieldProps) {
        const data = { id: this.document.id, attributes: {} };
        data.attributes[fieldProps.name] = fieldProps.value;
        this.titleSetStatusNormal()
        this.$store.dispatch('document/save', data).then(response => {
          this.titleSetStatusSuccess()
          setTimeout(this.titleSetStatusNormal, 3000)
        }).catch(() => {
          this.titleSetStatusError()
          setTimeout(this.titleSetStatusNormal, 3000)
        })
      },
      titleSetStatusNormal () {
        this.titleStatus = 'normal'
      },
      titleSetStatusSuccess () {
        this.titleStatus = 'success'
      },
      titleSetStatusError () {
        this.titleStatus = 'error'
      },
      languagesChanged (langs) {
        const data = { id: this.document.id,
          relationships: {
            languages: {
              data: langs.map(l => {
                return {
                  id: l.id,
                  type: "language"
                }
              })
            }
          }
        };

        this.$store.dispatch('document/save', data);
        console.log("lang data", data)
      },

    },
    computed: {
      ...mapState('document', ['document', 'languages']),
      ...mapState({
        allLanguages: state => state.languages.languages
      }),
      languagesConcat () {
        return this.languages.map(lang => lang.label).join(', ')
      },
      languagesIds () {
        return this.languages.map(lang => lang.id)
      }
    }
  }
</script>

<style scoped>
</style>