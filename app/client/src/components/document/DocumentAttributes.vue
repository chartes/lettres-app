<template>
  <div class="document__attributes">

    <header class="document__attributes--title subtitle">
      <title-field-in-place
              :tabulation-index="0"
              label="Titre"
              name="title"
              not-set="Non renseigné"
              :initial-value="document.title"
              :editable="editable"
              :status="titleStatus"
              specific-class="field-title__input"
              v-on:changed="titleChanged"
      />
    </header>

    <div class="columns is-multiline subtitle" v-if="editAttributes">
      <div class="column">
        <multiselect-field
                :editable="editable"
                label="Langues"
                :add-colons="false"
                :optionsList="allLanguages"
                :selectedItems="languages"
                :onChange="languagesChanged"/>
      </div>
    </div>

  </div>
</template>
<script>
  import { mapState } from 'vuex';
  import MultiselectField from '../forms/fields/MultiselectField';
  import TitleFieldInPlace from '../forms/fields/TitleFieldInPlace';

  export default {
    name: 'DocumentAttributes',
    components: {TitleFieldInPlace,  MultiselectField },
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
      })
    }
  }
</script>

<style scoped>
</style>
