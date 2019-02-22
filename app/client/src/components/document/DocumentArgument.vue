<template>
  <div v-if="(document.argument && document.argument.length)  || editable> 0" class="document__argument">

    <header class="argument__header">
      <h2 class="argument__title subtitle">Argument</h2>
    </header>

    <rich-text-editor
            v-if="editable"
            v-model="form"
            :enabled="editorEnabled"
            :formats="[['note','link'],['bold','italic','superscript','underline'],['person','location','cite']]"
    >
      <button
              class="argument__save button is-small"
              :class="saveButtonClass"
              :disabled="status === 'disabled'"
              @click="clickSave"
      >
        <component :is="saveButtonIcon"/>
      </button>
    </rich-text-editor>
    <div v-else class="argument__content" v-html="form"></div>

  </div>
</template>

<script>

  import { mapState } from 'vuex'
  import RichTextEditor from '../forms/fields/RichTextEditor';
  import IconSave from '../ui/icons/IconSave';
  import IconError from '../ui/icons/IconError';
  import IconSuccess from '../ui/icons/IconSuccess';
  export default {
    name: 'DocumentArgument',
    components: {RichTextEditor},
    props: {
      editable: {
        type: Boolean,
        default: false
      },
    },
    data() {
      return {
        status: 'normal',
        editorEnabled: true,
        form: ''
      }
    },
    mounted () {
      this.form = this.document.argument || ''
    },
    methods: {
      clickSave () {
        if (this.status === 'error' || this.status === 'success') return;
        this.status = 'loading';
        const data = { id: this.document.id, attributes: { argument: this.form } };
        this.$store.dispatch('document/save', data)
          .then(response => {
            this.status = 'success'
            setTimeout(() => this.status = 'normal', 3000)
          }).catch(() => {
          this.status = 'error'
          setTimeout(() => this.status = 'normal', 3000)
        })
      },
    },
    computed: {
      ...mapState('document', ['document']),
      saveButtonClass () {
        switch (this.status) {
          case 'normal':
          case 'disabled':
            return 'is-success'
            break
          case 'success':
            return 'is-success'
            break
          case 'error':
            return 'is-danger'
            break
          case 'loading':
            return 'is-loading'
        }
      },
      saveButtonIcon () {
        switch (this.status) {
          case 'normal':
          case 'loading':
          case 'disabled':
            return IconSave;
            break;
          case 'success':
            return IconSuccess;
            break;
          case 'error':
            return IconError;
            break;
        }
      },
    },
    watch: {
      status () {
        this.editorEnabled =  !(this.status === 'loading' || this.status === 'error' || this.status === 'success')
      }
    }
  }
</script>

<style scoped>
  .notes {
    margin-top: 40px;
    margin-bottom: 40px;
    padding-top: 20px;
    border-top: solid 1px darkgrey;
    color: grey;
  }
  .section {
    padding-top: 24px;
    padding-bottom: 24px;
  }
</style>