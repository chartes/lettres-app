<template>

  <modal-form class="person-list-form"
          :title="title"
          :cancel="cancelAction"
          :remove="remove ? removeAction : null"
          :valid="validForm"
          :submitting="false"
          :submit="submitAction"
  >
    <div class="person-list-form">
          <select-autocomplete-field
            v-model="form"
            :items="placenamesSearchResults"
            :is-async="true"
            @search="searchPlacename"
            label-key="label"
            notSet="Rechercher un lieu"
          >
            <template v-slot:inputActions>
              <a class="witness-item__delete" style="font-size: small;" href="#"
                 @click="openNewPlacenameForm">
                <span>Ajoutez un nouveau lieu en cliquant ici.</span>
              </a>
            </template>
  
            <template v-slot:outputActions>
              <a class="witness-item__delete" style="vertical-align: bottom;" href="#"
                 @click="openNewPlacenameForm">
                <icon-add/>
              </a>
            </template>
            
          </select-autocomplete-field>
      
          <div class="mt-4">
            <field-text
                label="Description du lieu"
                placeholder="ex : Depuis le camp militaire aux abords de la ville"
                v-model="form.function"
                :disabled="!validForm"
            />
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
  import IconAdd from "../ui/icons/IconAdd";

  export default {
    name: "PlacenameListForm",
    components: {
      PlacenameForm,
      LaunchButton,
      SelectAutocompleteField,
      FieldText,
      ModalForm,
      IconAdd
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
        //this.submitAction()
      },
    },
    computed: {

      ...mapState('placenames', ['placenamesSearchResults']),
	
	    validForm() {
		    return !!this.form.label && (this.form.label.length >= 1);
	    },
    }
  }
</script>
