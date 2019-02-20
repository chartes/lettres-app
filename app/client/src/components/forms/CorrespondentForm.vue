<template>

  <modal-form
          :title="title"
          :cancel="cancelAction"
          :submit="submitAction"
          :remove="remove"
          :valid="validForm"
          :submitting="false"
  >
    <div class="correspondent-form">
      <form @submit.prevent="">
        <error-message v-if="error" :error="error"/>
        <field-text
                label="Prénom"
                placeholder="Prénom"
                v-model="form.firstname"
        />
        <field-text
                label="Nom"
                placeholder="Nom"
                v-model="form.lastname"
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
            :items="correspondentsWikidataSearchResults"
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
    name: "correspondent-form",
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
        //this.$store.dispatch('correspondents/searchOnWikidata', 'Catherine de Medicis')
    },
    methods: {
  
      submitAction () {
        this.form.key = `${this.form.lastname}, ${this.form.firstname}`;
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
          return this.$store.dispatch('correspondents/searchOnWikidata', who);
      }

    },
    computed: {

      ...mapState('correspondents', ['roles', 'correspondentsWikidataSearchResults']),

      validForm () {
        return (
          !!this.form.firstname && (this.form.firstname.length >= 1)
          &&
          !!this.form.lastname && (this.form.lastname.length >= 1)
        );
      },

    }
  }
</script>