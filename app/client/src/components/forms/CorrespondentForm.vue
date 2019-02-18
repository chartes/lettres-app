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
        <field-text
                label="Référence"
                placeholder="Référence"
                v-model="form.ref"
        />
      </form>
    </div>
  </modal-form>

</template>

<script>

  import { mapState } from 'vuex';

  import ModalForm from './ModalForm';
  import FieldText from './fields/TextField';
  import ErrorMessage from '../ui/ErrorMessage';

  export default {
    name: "correspondent-form",
    components: {
      ErrorMessage,
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
      error: { type: Object, default: null },
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
        this.form.key = `${this.form.lastname}, ${this.form.firstname}`
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
        return (
          !!this.form.firstname && (this.form.firstname.length >= 1)
          &&
          !!this.form.lastname && (this.form.lastname.length >= 1)
        );
      },

    }
  }
</script>