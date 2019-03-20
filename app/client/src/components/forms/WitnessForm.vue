<template>

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
            <field-select
                label="Statut"
                :options="statusesList"
                v-model="form.status"
            />
          </div>
          <div class="column">
            <field-select
                label="Tradition"
                :options="traditionsList"
                v-model="form.tradition"
            />
          </div>
          <div class="column">
            <select-autocomplete-field
                label="Institution"
                v-model="form.institution"
                :items="institutionsSearchResults"
                :is-async="true"
                @search="searchInstitution"
                label-key="name"
            >
              <button
                  class="button is-outlined is-link"
                  @click="openInstitutionForm">
                Ajouter une institution
              </button>
            </select-autocomplete-field>
          </div>
        </div>
        
        <rich-text-editor
                label="Témoin"
                v-model="form.content"
        />
        <rich-text-editor
                label="Côte du témoin"
                v-model="form['classification-mark']"
                :formats="[['italic','superscript','note']]"
        />
      </form>
    </div>
    <institution-form
            v-if="institutionForm"
            title="Ajouter une institution"
            :submit="submitInstitutionForm"
            :cancel="closeInstitutionForm"
            :error="institutionError"
    />
  </modal-form>

</template>

<script>

  import { mapState } from 'vuex';

  import ModalForm from './ModalForm';
  import FieldLabel from './fields/FieldLabel';
  import FieldSelect from './fields/SelectField';
  import FieldText from './fields/TextField';
  import { statuses, traditions } from './data';
  import RichTextEditor from './fields/RichTextEditor';
  import SelectAutocompleteField from './fields/SelectAutocompleteField';
  import LoadingIndicator from '../ui/LoadingIndicator';
  import InstitutionForm from './InstitutionForm';

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
      ModalForm
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

      searchInstitution (search) {
        this.$store.dispatch('institutions/search', search)
      },

      submitAction () {
        if (this.form.institution && this.form.institution.id === null) this.form.institution = null
        this.$props.submit(this.form);
      },
      cancelAction () {
        if (this.institutionForm) return;
        this.$props.cancel();
      },
      removeAction () {
        this.$props.cancel();
      },

      submitInstitutionForm (inst) {
        this.institutionError = null;
        this.$store.dispatch('institutions/addOne', inst)
          .then (response => {
            this.form.institution = response
            this.closeInstitutionForm()
          })
          .catch(error => {
            console.log(error)
            this.institutionError = error.toString()
          })
      },
      openInstitutionForm () {
        this.institutionForm = true
      },
      closeInstitutionForm () {
        this.institutionForm = false
      },
    },
    watch: {
      currentWitness (val) {
        this.form = { ...val }
        this.loading = false
      }
    },
    computed: {
      ...mapState('witnesses', ['currentWitness']),
      ...mapState('institutions', ['institutionsSearchResults']),
      statusesList () {
        return statuses;
      },
      traditionsList () {
        return traditions;
      },
      isValid () {
        return this.form.content && this.form.content.length >= 1 && this.form.content !== '<p><br></p>'
      }

    }
  }
</script>