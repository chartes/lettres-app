<template>

  <modal-form class="person-form__add-new__form"
          :title="title"
          :cancel="cancelAction"
          :submit="submitAction"
          :remove="remove"
          :valid="validForm"
          :submitting="false"
  >
    <div class="person-form">
      <form @submit.prevent="">
        <error-message v-if="error" :error="error"/>
        <field-text
                label="Étiquette *"
                placeholder="ex : Nom, Prénom"
                v-model="form.label"
        />
        <field-text
                label="Description"
                placeholder="ex : Duc d'Anjou, prince marchand, etc."
                v-model="form.description"
        />

        <div class="person-form__link-to-ref">
          <div class="columns">
            <div class="column is-5">
              <select-autocomplete-field
                  class="person-form__search-ref"
                  label="Lier la personne via un référentiel"
                  v-model="form.ref"
                  :items="personsWikidataSearchResults"
                  :is-async="true"
                  @search="searchPersonOnWikidata"
                  label-key="label"
                  not-set="Rechercher sur wikidata"
              />
            </div>
            <div class="column is-1 person-form__separator">
              <p><em>ou</em></p>
            </div>
            <div class="column is-5 person-form__input-ref">
              <field-text
                  label="Lier la personne à un identifiant de référence"
                  :placeholder="form.ref ? form.ref.label : 'ex: https://data.bnf.fr/ark:/12148/cb123351707'"
                  v-model="form.ref && form.ref.uriForDisplay ? form.ref.uriForDisplay : form.ref"
              />
            </div>
          </div>
        </div>
      </form>
    </div>
  </modal-form>

</template>

<script>

  import { mapState } from 'vuex';

  import ModalForm from './ModalForm';
  import FieldText from './fields/TextField';
  import ErrorMessage from '../ui/ErrorMessage';
  import SelectAutocompleteField from "./fields/SelectAutocompleteField";

  export default {
    name: "person-form",
    components: {
      ErrorMessage,
      FieldText,
      ModalForm,
      SelectAutocompleteField
    },
    props: {
      title: { type: String, default: '' },
      label: { type: String, default: '' },
      institution: { type: Object, default: null },
      cancel: { type: Function },
      submit: { type: Function },
      remove: { type: Function },
      error: { type: Object, default: null },
    },
    data() {
      return {
        form: { ...this.$props.institution },
        loading: false,
      }
    },
    mounted () {

    },
    methods: {
  
      submitAction () {
        this.form.ref = this.form.ref && this.form.ref.uriForDisplay ? this.form.ref.uriForDisplay : this.form.ref;
        this.$props.submit(this.form);
      },
      cancelAction () {
        this.$props.cancel();
      },
      removeAction () {
        this.$props.cancel();
      },
      searchPersonOnWikidata(who) {
          return this.$store.dispatch('persons/searchOnWikidata', who);
      }

    },
    computed: {

      ...mapState('persons', ['roles', 'personsWikidataSearchResults']),

      validForm () {
        return (
          !!this.form.label && (this.form.label.length >= 1)
        );
      },

    }
  }
</script>