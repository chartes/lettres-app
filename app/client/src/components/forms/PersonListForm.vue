<template>

  <modal-form class="person-list-form"
          :title="title"
          :cancel="cancelAction"
          :remove="remove ? removeAction : null"
          :valid="validForm"
          :submitting="false"
  >
    <div class="person-list-form">
      <div class="columns">
        <div class="column is-5">
          <select-autocomplete-field
            v-model="form"
            :items="personsSearchResults"
            :is-async="true"
            @search="searchPerson"
            label-key="label"
            notSet="Rechercher une personne"
          />
        </div>
        <div class="column is-1 person-list-form__separator">
          <div><p><em>ou</em></p></div>
        </div>
        <div class="column is-5">
          <div class="person-list-form__add-new has-text-centered">

            <p>
              <launch-button
                      label="Ajouter une nouvelle personne"
                      @click="openNewPersonForm"
              />
            </p>
          </div>
        </div>
      </div>
    </div>

    <person-form v-if="personForm"
            label="Ajouter une nouvelle personne"
            :error="newPersonError"
            :submit="createNewPerson"
            :cancel="closeNewPersonForm"
            title="Ajouter une nouvelle personne"
    />

  </modal-form>

</template>

<script>

  import { mapState } from 'vuex';
  import ModalForm from './ModalForm';
  import FieldText from './fields/TextField';
  import LaunchButton from './LaunchButton';
  import PersonForm from './PersonForm';
  import SelectAutocompleteField from "./fields/SelectAutocompleteField";

  export default {
    name: "PersonListForm",
    components: {
      PersonForm,
      LaunchButton,
      SelectAutocompleteField,
      FieldText,
      ModalForm
    },
    props: {
      title: { type: String, default: '' },
      label: { type: String, default: '' },
      institution: { type: Object, default: null },
      cancel: { type: Function },
      submit: { type: Function },
      remove: { type: Function },
    },
    data() {
      return {
        form: {},
        loading: false,
        personForm: false,
        newPersonError: null
      }
    },
    methods: {

      searchPerson (search) {
        this.$store.dispatch('persons/search', search)
      },

      submitAction () {
        this.$props.submit(this.form);
      },
      cancelAction () {
        if (this.personForm) return;
        this.$props.cancel();
      },
      removeAction () {
        this.$props.remove();
      },

      openNewPersonForm () {
        this.personForm = true
      },
      closeNewPersonForm () {
        this.personForm = false
      },
      createNewPerson (person) {
        this.$store.dispatch('persons/addOne', person)
          .then(corr => {
            this.$props.submit({
              id: corr.id,
              ...corr.attributes
            });
          })
          .catch(error => {
            this.newPersonError = error.toString()
          })
      },

    },
    watch: {
      form (val, oldVal) {
        this.submitAction()
      },
    },
    computed: {

      ...mapState('persons', ['personsSearchResults']),

      validForm () {
        return !!this.form.name && (this.form.name.length >= 1);
      },

    }
  }
</script>