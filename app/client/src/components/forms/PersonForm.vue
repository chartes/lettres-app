<template>

  <modal-form
          :title="title"
          :cancel="cancelAction"
          :submit="submitAction"
          :remove="remove"
          :valid="validForm"
          :submitting="false"
  >
    <div class="person-form">
      <form @submit.prevent="">
        <error-message v-if="error" :error="error"/>
        <field-text
                label="Label"
                placeholder="Label"
                v-model="form.label"
        />
        <field-text
                label="Description"
                placeholder="Description"
                v-model="form.description"
        />
        <!--
        <field-text
                label="Référence"
                placeholder="Référence"
                v-model="form.ref"
        />
        -->
        <select-autocomplete-field
            label="Référence"
            v-model="form.ref"
            :items="personsWikidataSearchResults"
            :is-async="true"
            @search="searchPersonOnWikidata"
            label-key="label"
        >
        </select-autocomplete-field>
      </form>
    </div>
  </modal-form>

</template>

<script>

  import { mapState } from 'vuex';

  import ModalForm from './ModalForm';
  import FieldText from './fields/TextField';
  import ErrorMessage from '../ui/ErrorMessage';
  import SelectAutocompleteField from "./fields/SelectAutocompleteField";

  export default {
    name: "person-form",
    components: {
      ErrorMessage,
      FieldText,
      ModalForm,
      SelectAutocompleteField
    },
    props: {
      title: { type: String, default: '' },
      label: { type: String, default: '' },
      institution: { type: Object, default: null },
      cancel: { type: Function },
      submit: { type: Function },
      remove: { type: Function },
      error: { type: Object, default: null },
    },
    data() {
      return {
        form: { ...this.$props.institution },
        loading: false,
      }
    },
    mounted () {
        //this.$store.dispatch('persons/searchOnWikidata', 'Catherine de Medicis')
    },
    methods: {
  
      submitAction () {
        this.form.ref = `${this.form.ref.uriForDisplay}`;
        this.$props.submit(this.form);
      },
      cancelAction () {
        this.$props.cancel();
      },
      removeAction () {
        this.$props.cancel();
      },
      searchPersonOnWikidata(who) {
          return this.$store.dispatch('persons/searchOnWikidata', who);
      }

    },
    computed: {

      ...mapState('persons', ['roles', 'personsWikidataSearchResults']),

      validForm () {
        return (
          !!this.form.label && (this.form.label.length >= 1)
        );
      },

    }
  }
</script>