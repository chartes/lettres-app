<template>

  <modal-form
          :title="title"
          :cancel="cancelAction"
          :submit="submitAction"
          :remove="remove"
          :valid="form.content && form.content.length >= 1"
          :submitting="false"
  >
    <loading-indicator :active="loading"/>
    <div class="location-form textinput-form" v-if="!loading">
      <form @submit.prevent="">
        <field-select
                label="Statut"
                :options="statusesList"
                v-model="form.status"
        />
        <field-select
                label="Tradition"
                :options="traditionsList"
                v-model="form.tradition"
        />
        <select-autocomplete-field
                label="Institution"
                v-model="form.institution"
                :items="institutionsSearchResults"
                :is-async="true"
                @search="searchInstitution"
                label-key="ref"
        >
          <button
                  class="button is-outlined is-link"
                  @click="openInstitutionForm">
            Ajouter une institution
          </button>
        </select-autocomplete-field>
        <rich-text-editor
                label="Contenu"
                v-model="form.content"
        />
        <rich-text-editor
                label="Classification mark"
                v-model="form['classification-mark']"
                :formats="[['italic','superscript','note']]"
        />
      </form>
    </div>
    <institution-form
            v-if="institutionForm"
            title="Ajouter une institution"
            :cancel="closeInstitutionForm"
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
      }
    },
    mounted () {
      if (this.$props.witness.id) {
        this.$store.dispatch('witnesses/fetchOne', this.$props.witness.id)
        this.loading = true;
      }
    },
    methods: {

      changeStatus (val) {
        console.log("changeStatus", val)
      },
      changeTradition (val) {
        console.log("changeTradition", val)
      },
      searchInstitution (search) {
        this.$store.dispatch('institutions/search', search)
      },

      submitAction () {
        this.$props.submit(this.form);
      },
      cancelAction () {
        this.$props.cancel();
      },
      removeAction () {
        this.$props.cancel();
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
        console.log("watch currentWitness", this.form)
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

    }
  }
</script>