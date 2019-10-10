<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  
  <modal-form
      :title="title"
      :cancel="cancelAction"
      :submit="submitAction"
      :remove="remove"
      :valid="isValid"
      :submitting="false"
  >
    <loading-indicator :active="loading"/>
    <div class="witness-form textinput-form" v-if="!loading">
      <form @submit.prevent="">
        
        <div class="columns">
          <div class="column">
            <field-select label="Statut" :options="statusesList" v-model="form.status"/>
          </div>
          <div class="column">
            <field-select label="Tradition" :options="traditionsList" v-model="form.tradition"/>
          </div>
          <div class="column">
          </div>
        </div>
        
        <rich-text-editor
            label="Témoin"
            v-model="form.content"
            :formats="[['italic','superscript'], ['note','link']] "
            :options="{placeholder: 'Ex. Bibl. nat. Fr., Français 3512, fol. 53r'}"/>
        
        
        <div style="margin-bottom: 1em;">
          <span style="margin-bottom: 1em;">
            Institution :
          </span>
          <div>
            <div class="institution-list-form">
              <select-autocomplete-field
                  v-model="form.institution"
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
        
        <rich-text-editor
            label="Cote / unité de conservation"
            v-model="form['classification-mark']"
            :formats="[['italic','superscript'], ['link']]"
            :options="{placeholder: 'Ex. Français 3512, Ms. 564, K 35'}"
        />
      </form>
    </div>
  
  </modal-form>

</template>

<script>
	
	import {mapActions, mapState} from 'vuex';
	import IconAdd from '../ui/icons/IconAdd';
	
	import ModalForm from './ModalForm';
	import FieldLabel from './fields/FieldLabel';
	import FieldSelect from './fields/SelectField';
	import FieldText from './fields/TextField';
	import { statuses, traditions } from './data';
	import RichTextEditor from './fields/RichTextEditor';
	import SelectAutocompleteField from './fields/SelectAutocompleteField';
	import LoadingIndicator from '../ui/LoadingIndicator';
	import InstitutionForm from './InstitutionForm';
	import LaunchButton from './LaunchButton';
	import IconBin from "../ui/icons/IconBin";
	
	export default {
		name: "witness-form",
		components: {
			InstitutionForm,
			LoadingIndicator,
			SelectAutocompleteField,
			RichTextEditor,
			FieldLabel,
			FieldSelect,
			FieldText,
			ModalForm,
			LaunchButton,
			IconAdd,
			IconBin
		},
		props: {
			title: { type: String, default: '' },
			label: { type: String, default: '' },
			witness: { type: Object, default: null },
			cancel: { type: Function },
			submit: { type: Function },
			remove: { type: Function },
		},
		data() {
			return {
				form: { ...this.$props.witness },
				loading: false,
				institutionForm: false,
				institutionError: null,
			}
		},
		mounted () {
			if (this.$props.witness.id) {
				this.$store.dispatch('witnesses/fetchOne', this.$props.witness.id)
				this.loading = true;
			}
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
        this.form.institution = null;
      },
			submitAction () {
				if (this.form.institution && this.form.institution.id === null) this.form.institution = null
				if (this.form.tradition === '') this.form.tradition = null;
				
				if (this.form.institution === null && !!this.currentWitness) {
					this.$store.dispatch('document/removeWitnessInstitution', this.currentWitness.id)
        }
				
				this.$props.submit(this.form);
			},
			cancelAction () {
				if (this.institutionForm) return;
				this.$props.cancel();
			},
			removeAction () {
				this.$props.cancel();
			},
		},
		watch: {
			currentWitness (val) {
				this.form = { ...val }
				this.loading = false
			},
			currentInstitution(val) {
				this.form.institution = val;
				this.loading = false
			}
		},
		computed: {
			...mapState('witnesses', ['currentWitness']),
			...mapState('institutions', ['currentInstitution', 'institutionsSearchResults']),
			
			statusesList () {
				return statuses;
			},
			traditionsList () {
				return traditions;
			},
			isValid () {
				console.log(this.form)
				return !!(this.form.content && this.form.content.length >= 1 && this.form.content !== '<p><br></p>')
			}
			
		}
	}
</script>
