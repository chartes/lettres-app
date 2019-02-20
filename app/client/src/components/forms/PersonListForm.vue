<template>

  <modal-form
          :title="title"
          :cancel="cancelAction"
          :remove="remove"
          :valid="validForm"
          :submitting="false"
  >
    <div class="person-list-form">


      <list-autocomplete-field
        search-placeholder="Rechercher une personne"
        v-model="form"
        :items="personsSearchResults"
        :is-async="true"
        @search="searchPerson"
        label-key="label"
      />

      <footer class="person-list-form__footer has-text-centered">
        <p>&mdash; <em>ou</em> &mdash; </p>
        <p>
          <launch-button
                  label="Ajouter une nouvelle personne"
                  @click="openNewPersonForm"
          />
        </p>
      </footer>


    </div>

    <person-form v-if="personForm"
            label="Ajouter une nouvelle personne"
            :error="newPersonError"
            :submit="createNewPerson"
            :cancel="closeNewPersonForm"
    />

  </modal-form>

</template>

<script>

  import { mapState } from 'vuex';
  import ModalForm from './ModalForm';
  import FieldText from './fields/TextField';
  import ListAutocompleteField from './fields/ListAutocompleteField';
  import LaunchButton from './LaunchButton';
  import PersonForm from './PersonForm';

  export default {
    name: "PersonListForm",
    components: {
      PersonForm,
      LaunchButton,
      ListAutocompleteField,
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
        this.$props.cancel();
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