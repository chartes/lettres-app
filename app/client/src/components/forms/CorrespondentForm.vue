<template>

  <modal-form
          :title="title"
          :cancel="cancelAction"
          :submit="submitAction"
          :remove="remove"
          :valid="validForm"
          :submitting="false"
  >
    <div class="institution-form">
      <form @submit.prevent="">
        <field-text
                label="Nom"
                placeholder="Nom de l'institution"
                v-model="form.name"
        />
        <field-text
                label="Référence"
                placeholder="Référence de l'institution"
                v-model="form.ref"
        />
      </form>
    </div>
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

  export default {
    name: "institution-form",
    components: {
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
        form: { ...this.$props.institution },
        loading: false,
      }
    },
    mounted () {

    },
    methods: {

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

      ...mapState('correspondents', ['roles']),

      validForm () {
        console.log('validForm', !!this.form.name && (this.form.name.length >= 1))
        return !!this.form.name && (this.form.name.length >= 1);
      },

    }
  }
</script>