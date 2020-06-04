<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">

  <modal-form class="person-list-form"
          :title="title"
          :cancel="cancelAction"
          :remove="remove ? removeAction : null"
          :valid="validForm"
          :submit="submitAction"
          :submitting="false"
  >
    <div class="person-list-form">
       <select-autocomplete-field
         v-model="form"
         :items="personsSearchResults"
         :is-async="true"
         @search="searchPerson"
         label-key="label"
         notSet="Rechercher une personne"
       >
       <template v-slot:inputActions>
         <a class="witness-item__delete" style="font-size: small;" href="#"
            @click="openNewPersonForm">
           <span>Ajoutez une nouvelle personne en cliquant ici.</span>
         </a>
       </template>
       
       <template v-slot:outputActions>
         <a class="witness-item__delete" style="vertical-align: bottom;" href="#"
            @click="openNewPersonForm">
           <icon-add/>
         </a>
       </template>

       </select-autocomplete-field>
       
       <div class="mt-4">
         <field-text
             label="Fonction occupée à ce moment"
             placeholder="ex : Duc d'Anjou, prince marchand, etc."
             v-model="form.function"
             :disabled="!validForm"
         />
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
  import IconAdd from "../ui/icons/IconAdd";

  export default {
    name: "PersonListForm",
    components: {
      PersonForm,
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
        personForm: false,
        newPersonError: null
      }
    },
    methods: {

      searchPerson (search) {
        this.$store.dispatch('persons/search', search)
      },

      submitAction() {
        this.$props.submit(this.form);
        this.closeNewPersonForm();
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
          	this.form = {
		          id: corr.id,
		          ...corr.attributes
	          };
	          this.closeNewPersonForm();
	
          })
          .catch(error => {
            this.newPersonError = error.toString()
          })
      },
    },
    watch: {
      form (val, oldVal) {
        //this.submitAction()
      },
    },
    computed: {

      ...mapState('persons', ['personsSearchResults']),
      validForm () {
        return !!this.form.label && (this.form.label.length >= 1);
      },

    }
  }
</script>
