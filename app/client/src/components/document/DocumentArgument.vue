<template>
  <div v-if="(document.argument && document.argument.length)  || editable> 0"
       class="panel mt-5">

    <header class="panel-heading argument__header">
      <h2 class="argument__title subtitle">Analyse de la lettre</h2>
    </header>
    
    <div class="panel-block">
      <rich-text-editor
          v-if="editable"
          v-model="form"
          :enabled="editorEnabled"
          :formats="[['italic','superscript'],['person','location'],['note','link']]"
      >
        <editor-save-button
            :doc-id="document.id"
            name="argument"
            :value="form"/>
      </rich-text-editor>
      <div v-else class="argument__content" v-html="form"></div>

    </div>

  </div>
</template>

<script>

  import { mapState } from 'vuex'
  import RichTextEditor from '../forms/fields/RichTextEditor';
  import EditorSaveButton from '../forms/fields/EditorSaveButton';
  export default {
    name: 'DocumentArgument',
    components: {EditorSaveButton, RichTextEditor},
    props: {
      editable: {
        type: Boolean,
        default: false
      },
    },
    data() {
      return {
        editorEnabled: true,
        form: ''
      }
    },
    mounted () {
      this.form = this.document.argument || ''
    },
    computed: {
      ...mapState('document', ['document']),
    },
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
