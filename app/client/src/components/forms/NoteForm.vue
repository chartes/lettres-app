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
        />
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
    methods: {

      submitAction () {

        console.log('NoteForm submitAction', this.form)
        this.loading = true;
        this.$store.dispatch('document/addNote', this.form).then( note => {
          console.log('added note', note)
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