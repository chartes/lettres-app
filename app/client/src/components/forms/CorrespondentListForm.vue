<template>

  <modal-form
          :title="title"
          :cancel="cancelAction"
          :remove="remove"
          :valid="validForm"
          :submitting="false"
  >
    <div class="correspondent-list-form">


      <list-autocomplete-field
        search-placeholder="Rechercher un correspondant"
        v-model="form"
        :items="correspondentsSearchResults"
        :is-async="true"
        @search="searchCorrespondent"
        label-key="key"
      />

      <footer class="correspondent-list-form__footer has-text-centered">
        <p>&mdash; <em>ou</em> &mdash; </p>
        <p>
          <launch-button
                  label="Créer un nouveau correspondant"
                  @click="openNewCorrespondentForm"
          />
        </p>
      </footer>


    </div>

    <correspondent-form v-if="correspondentForm"
            label="Créer un nouveau correspondant"
            :error="newCorrespondentError"
            :submit="createNewCorrespondent"
            :cancel="closeNewCorrespondentForm"
    />

  </modal-form>

</template>

<script>

  import { mapState } from 'vuex';
  import ModalForm from './ModalForm';
  import FieldText from './fields/TextField';
  import ListAutocompleteField from './fields/ListAutocompleteField';
  import LaunchButton from './LaunchButton';
  import CorrespondentForm from './CorrespondentForm';

  export default {
    name: "CorrespondentListForm",
    components: {
      CorrespondentForm,
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
        correspondentForm: false,
        newCorrespondentError: null
      }
    },
    methods: {

      searchCorrespondent (search) {
        this.$store.dispatch('correspondents/search', search)
      },

      submitAction () {
        this.$props.submit(this.form);
      },
      cancelAction () {
        if (this.correspondentForm) return;
        this.$props.cancel();
      },
      removeAction () {
        this.$props.cancel();
      },

      openNewCorrespondentForm () {
        this.correspondentForm = true
      },
      closeNewCorrespondentForm () {
        this.correspondentForm = false
      },
      createNewCorrespondent (correspondent) {
        this.$store.dispatch('correspondents/addOne', correspondent)
          .then(corr => {
            this.$props.submit({
              id: corr.id,
              ...corr.attributes
            });
          })
          .catch(error => {
            this.newCorrespondentError = error.toString()
          })
      },

    },
    watch: {
      form (val, oldVal) {
        this.submitAction()
      },
    },
    computed: {

      ...mapState('correspondents', ['correspondentsSearchResults']),

      validForm () {
        return !!this.form.name && (this.form.name.length >= 1);
      },

    }
  }
</script>