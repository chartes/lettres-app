<template>
  <div class="document__attributes">

    <header class="document__attributes--title">
      <h1 class="title" v-html="document.title"></h1>
    </header>

    <div class="columns is-multiline">
      <div class="column is-one-third">
        <date-field
                :tabulation-index="0"
                label="creation"
                name="creation"
                not-set="Inconnue"
                :initial-value="document['creation']"
                :editable="editable"
                v-on:changed="fieldChanged"/>
      </div>
      <div class="column is-one-third">
        <date-field
                :tabulation-index="0"
                label="creation-not-after"
                name="creation-not-after"
                :initial-value="document['creation-not-after']"
                :editable="editable"
                v-on:changed="fieldChanged"/>
      </div>
      <div class="column is-one-third">
        <text-field-in-place
                :tabulation-index="0"
                label="creation-label"
                name="creation-label"
                not-set="Inconnue"
                :initial-value="document['creation-label']"
                :editable="editable"
                v-on:changed="fieldChanged"/>
      </div>
      <div class="column">
        <multiselect-field
                :editable="editable"
                label="Langue(s)"
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
  import IconBin from '../ui/icons/IconBin';
  import LaunchButton from '../forms/LaunchButton';
  import PlacenameListForm from "../forms/PlacenameListForm";

  export default {
    name: 'DocumentAttributes',
    components: {
        TextFieldInPlace, DateField, MultiselectField,
        LaunchButton, IconBin
    },
    props: {
        editable: {
            type: Boolean,
            default: false
        },
    },
    methods: {
      fieldChanged (fieldProps) {
        const data = { id: this.document.id, attributes: {} };
        data.attributes[fieldProps.name] = fieldProps.value;
        this.$store.dispatch('document/save', data)
      },
      languagesChanged (langs) {
        console.log("languagesChanged", langs);

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
      languagesConcat: function () {
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