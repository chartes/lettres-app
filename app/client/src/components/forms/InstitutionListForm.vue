<template>
  <div>
     <span style="margin-bottom: 1em;">
            Institution :
          </span>
    <div>
      <div class="institution-list-form">
        <select-autocomplete-field
            v-model="witness.institution"
            :items="institutionsSearchResults"
            :is-async="true"
            @search="searchInstitution"
            label-key="name"
            notSet="Non renseignée"
        >
          <template v-slot:inputActions>
        
          </template>
          <template v-slot:outputActions>
            <a class="witness-item__delete" style="vertical-align: bottom;" href="#" @click="openNewInstitutionForm">
              <icon-add/>
            </a>
            <a class="witness-item__delete" style="vertical-align: bottom;" href="#" @click="clearInstitution">
              <icon-bin/>
            </a>
          </template>
        </select-autocomplete-field>


      </div>
      <institution-form v-if="institutionForm"
                        label="Ajouter une nouvelle institution"
                        :error="institutionError"
                        :submit="createNewInstitution"
                        :cancel="closeNewInstitutionForm"
                        title="Ajouter une nouvelle institution"
      />
    </div>
  </div>
</template>

<script>
	import SelectAutocompleteField from "./fields/SelectAutocompleteField";
	import InstitutionForm from "./InstitutionForm";
	import IconAdd from "../ui/icons/IconAdd";
	import IconBin from "../ui/icons/IconBin";
	import {mapState} from "vuex";
	
	export default {
		name: "InstitutionListForm",
    components: {
	    InstitutionForm,
	    SelectAutocompleteField,
	    IconAdd,
	    IconBin
    },
    props: ['witness'],
    data() {
			return {
        institutionForm: false,
        institutionError: null,
      }
    },
    mounted() {
      this.searchInstitution('*')
    },
		methods: {
	    createNewInstitution(institution) {
		    this.$store.dispatch('institutions/addOne', institution)
			    .then(corr => {
				    /*
            this.$props.submit({
              id: corr.id,
              institution: institution
            });
            */
			    })
			    .catch(error => {
				    this.institutionError = error.toString()
			    })
	    },
	    searchInstitution(search) {
		    this.$store.dispatch('institutions/search', search)
	    },
	    openNewInstitutionForm() {
		    this.institutionForm = true
	    },
	    closeNewInstitutionForm() {
		    this.institutionForm = false
	    },
	    clearInstitution() {
		    this.$props.witness.institution = null;
	    },
    },
    computed: {
	    ...mapState('institutions', ['currentInstitution', 'institutionsSearchResults']),
    }
	}
</script>

<style scoped>

</style>
