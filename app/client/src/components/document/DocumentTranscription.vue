<template>
  <div class="">
    <div class="panel document__transcription">
    
      <header class="panel-heading">
        <h2 class="document__transcription--title subtitle">Transcription</h2>
      </header>
      
      <div class="panel-block" style="display: inline-block; width: 100%">
        <h3 class="subtitle mt-3">Adresse</h3>
        
        <rich-text-editor
            v-if="editable"
            v-model="addressContent"
            :formats="[['note'],['italic','superscript'],[]]"
        >
          <editor-save-button
              :doc-id="document.id"
              name="address"
              :value="addressContent"/>
        </rich-text-editor>
        <div v-else class="document__transcription--content" v-html="addressContent"></div>
      </div>
      
      <div class="panel-block document__transcription--tr-content" style="display: inline-block; width: 100%">
        <h3 class="subtitle mt-3">Lettre</h3>
        <rich-text-editor
            v-if="editable"
            v-model="transcriptionContent"
            :formats="[['note','page','link'],['italic','superscript'],['person','location']]"
        >
          <editor-save-button
              :doc-id="document.id"
              name="transcription"
              :value="transcriptionContent"/>
        </rich-text-editor>
        <div v-else class="document__transcription--content" v-html="transcriptionContent"></div>
      </div>
     
    </div>
    
    <document-notes :editable="editable"></document-notes>
    
  </div>
</template>

<script>

  import { mapState } from 'vuex'
  import RichTextEditor from '../forms/fields/RichTextEditor';
  import EditorSaveButton from '../forms/fields/EditorSaveButton';
  import DocumentNotes from './DocumentNotes';
  
  export default {
    name: 'DocumentTranscription',
    components: {EditorSaveButton, RichTextEditor, DocumentNotes},
    props: {
      editable: {
        type: Boolean,
        default: false
      },
    },
    data () {
      return {
        transcriptionContent: '',
	      addressContent: ''
      }
    },
    mounted() {
      this.transcriptionContent = this.document.transcription || '';
	    this.addressContent = this.document.address || ''
    },
    methods: {
    },
    computed: {
      ...mapState('document', ['document', 'witnesses']),
    },
    watch: {
    }
  }
</script>

<style scoped>
</style>
