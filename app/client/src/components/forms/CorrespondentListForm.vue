<template>

  <modal-form
          :title="title"
          :cancel="cancelAction"
          :submit="submitAction"
          :remove="remove"
          :valid="validForm"
          :submitting="false"
  >
    <div class="correspondent-list-form">

      <header class="correspondent-list-form__header has-text-centered">

        <p><button class="button">Créer un nouveau correspondant</button></p>
        <p>&mdash; <em>ou</em> &mdash; </p>

        <list-autocomplete-field
          search-placeholder="Rechercher un correspondant"
          v-model="form"
          :items="correspondentsSearchResults"
          :is-async="true"
          @search="searchCorrespondent"
          label-key="key"
        />

      </header>


    </div>
  </modal-form>

</template>

<script>

  import { mapState } from 'vuex';
  import ModalForm from './ModalForm';
  import FieldText from './fields/TextField';
  import ListAutocompleteField from './fields/ListAutocompleteField';

  export default {
    name: "CorrespondentListForm",
    components: {
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
      }
    },
    methods: {

      searchCorrespondent (search) {
        console.log('searchCorrespondent', search)
        this.$store.dispatch('correspondents/search', search)
      },

      submitAction () {
        this.$props.submit(this.form);
      },
      cancelAction () {
        this.$props.cancel();
      },
      removeAction () {
        this.$props.cancel();
      }

    },
    computed: {

      ...mapState('correspondents', ['correspondentsSearchResults']),

      validForm () {
        console.log('validForm', !!this.form.name && (this.form.name.length >= 1))
        return !!this.form.name && (this.form.name.length >= 1);
      },

    }
  }
</script>