<template>

  <modal-form
          :title="title"
          :cancel="hasCancelAction"
          :remove="remove"
          :valid="true"
          :submitting="false"
  >
    <div class="collection-list-form">
      
      <article v-if="current_user.isAdmin" class="message">
        <div class="message-body">
          <p>
            Pour créer une nouvelle collection ou en modifier une existante, utilisez plutôt la
            <a href="/lettres/collections">page de gestion des collections</a>
          </p>
        </div>
      </article>
      
      <list-autocomplete-field
        search-placeholder="Rechercher une collection"
        v-model="form"
        :items="collectionsSearchResults"
        :is-async="true"
        @search="searchCollection"
        label-key="title"
      />

    </div>
  </modal-form>

</template>

<script>

  import { mapState } from 'vuex';
  import ModalForm from './ModalForm';
  import FieldText from './fields/TextField';
  import ListAutocompleteField from './fields/ListAutocompleteField';

  export default {
    name: "CollectionListForm",
    components: {
      ListAutocompleteField,
      FieldText,
      ModalForm
    },
    props: {
      title: { type: String, default: '' },
      label: { type: String, default: '' },
      cancel: { type: Function },
      submit: { type: Function },
      remove: { type: Function },
    },
    data() {
      return {
        form: {},
        loading: false,
      }
    },
    methods: {

      searchCollection (search) {
        console.log('searchCollection', search)
        this.$store.dispatch('collections/search', search)
      },

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
    watch: {
      form (val, oldVal) {
        console.log('watch form', this.form)
        this.submitAction()
      },
    },
    computed: {

      ...mapState('collections', ['collectionsSearchResults']),
      ...mapState('user', ['current_user']),

        hasCancelAction () {
        return this.cancel ? this.cancelAction : null
      },
      validForm () {
        return !!this.form.id;
      },

    }
  }
</script>