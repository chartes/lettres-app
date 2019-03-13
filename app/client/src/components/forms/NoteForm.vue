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
    props: ['title', 'noteId', 'note', 'cancel', 'submit'],
    beforeCreate: function () {
      this.$options.components.RichTextEditor = require('./fields/RichTextEditor').default
    },
    data() {
      return {
        form: Object.assign({}, this.note),
        textLength: 0,
        loading: false,
      }
    },
    methods: {

      submitAction () {
        if (!this.noteId) {
          this.loading = true;
        }
        this.submit(this.form)

      },
      cancelAction () {
        this.$props.cancel();
      }
    },
    computed: {
        isValid () {
          console.log("isValid", this.form.content)
            return !!this.form && !!this.form.content && this.form.content.length > 1
        }
    }
  }
</script>