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
            :items="placenamesSearchResults"
            :is-async="true"
            @search="searchPlacename"
            label-key="label"
            notSet="Rechercher un lieu"
          />
        </div>
        <div class="column is-1 person-list-form__separator">
          <div><p><em>ou</em></p></div>
        </div>
        <div class="column is-5">
          <div class="person-list-form__add-new has-text-centered">
            <p>
              <launch-button label="Ajouter un nouveau lieu"  @click="openNewPlacenameForm"/>
            </p>
          </div>
        </div>
      </div>
    </div>

    <placename-form v-if="placenameForm"
            label="Ajouter un nouveau lieu"
            :error="newPlacenameError"
            :submit="createNewPlacename"
            :cancel="closeNewPlacenameForm"
            title="Ajouter un nouveau lieu"
    />

  </modal-form>

</template>

<script>

  import { mapState } from 'vuex';
  import ModalForm from './ModalForm';
  import FieldText from './fields/TextField';
  import LaunchButton from './LaunchButton';
  import PlacenameForm from './PlacenameForm';
  import SelectAutocompleteField from "./fields/SelectAutocompleteField";

  export default {
    name: "PlacenameListForm",
    components: {
      PlacenameForm,
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
        placenameForm: false,
        newPlacenameError: null
      }
    },
    methods: {

      searchPlacename (search) {
        this.$store.dispatch('placenames/search', search)
      },

      submitAction () {
        console.log('submitAction', this.form)
        this.$props.submit(this.form);
      },
      cancelAction () {
        if (this.placenameForm) return;
        this.$props.cancel();
      },
      removeAction () {
        this.$props.remove();
      },

      openNewPlacenameForm () {
        this.placenameForm = true
      },
      closeNewPlacenameForm () {
        this.placenameForm = false
      },
      createNewPlacename (placename) {
        this.$store.dispatch('placenames/addOne', placename)
          .then(corr => {
            this.$props.submit({
              id: corr.id,
              ...corr.attributes
            });
          })
          .catch(error => {
            this.newPlacenameError = error.toString()
          })
      },

    },
    watch: {
      form (val, oldVal) {
        this.submitAction()
      },
    },
    computed: {

      ...mapState('placenames', ['placenamesSearchResults']),

      validForm () {
        return !!this.form.name && (this.form.name.length >= 1);
      },

    }
  }
</script>