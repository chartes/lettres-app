<template>
  <modal-form
        :title="title"
        :cancel="cancelAction"
        :submit="submitAction"
        :valid="isValid"
        :submittin="null"
  >
    <div class="note-form">
        <rich-text-editor
                :formats="[['bold','italic','superscript','underline','del'],['link','person','location','cite']]"
                v-model="form.content"
        ></rich-text-editor>
    </div>
  </modal-form>

</template>

<script>

  import ModalForm from './ModalForm';
  import LoadingIndicator from '../ui/LoadingIndicator';

  export default {
    name: "NoteForm",
    components: { LoadingIndicator, ModalForm,
        //RichTextEditor: () => import('./fields/RichTextEditor')
    },
    props: {
      title: { type: String },
      cancel: { type: Function },
      submit: { type: Function },
      note: { type: Object, default: () => {} },
    },
    beforeCreate: function () {
      this.$options.components.RichTextEditor = require('./fields/RichTextEditor').default
    },
    data() {
      return {
        form: {},
        textLength: 0,
        loading: false,
      }
    },
    mounted () {
      this.form = { ...this.$props.note }
    },
    methods: {

      submitAction () {
        this.loading = true;
        const action = this.note && this.note.id ? 'document/updateNote' : 'document/addNote'
        this.$store.dispatch(action, this.form).then( note => {
          this.submit(note)
        })

      },
      cancelAction () {
        this.$props.cancel();
      }
    },
    computed: {
      isValid () {
        return !!this.form && !!this.form.content && this.form.content.length > 1
      }
    }
  }
</script>