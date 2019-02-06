<template>
    <div class="document-preview-card" v-if="documentPreview">
        <aside class="document-preview-card__thumbnail">
            <a :href="`${baseUrl}/documents/${documentPreview.id}`">
                <img v-if='documentPreview.attributes["iiif-thumbnail-url"]'
                     :src='documentPreview.attributes["iiif-thumbnail-url"]'/>
           </a>
        </aside>
        <article>
          <header class="title">
              <document-tag-bar v-if="documentPreview" :doc-id="doc_id"/>
              <span><h1 class="document-preview-card__title" v-html="titleContent"></h1></span>
          </header>

          <div class="content">
             <div class="columns">
               <div class="column is-three-quarters">
                 <p class="document-preview-card__content" v-html="previewContent"></p>
               </div>
               <div class="column document-preview-card__correspondents">
                 <ul>
                   <li class="" v-for="obj in documentPreview.correspondents">
                     <a href="">{{getCorrespondentFullname(obj)}}</a>
                     <span class="tag is-light is-rounded">{{obj.role.label}}</span>
                   </li>
                 </ul>
               </div>
             </div>
          </div>
        </article>
    </div>
</template>

<script>
  import { mapState } from 'vuex'
  import LoadingIndicator from './ui/LoadingIndicator';
  import DocumentAttributes from './document/DocumentAttributes';
  import {baseAppURL} from '../modules/http-common';
  import DocumentTagBar from "./document/DocumentTagBar";

  export default {

    name: 'DocumentPreviewCard',
    components: {DocumentAttributes, LoadingIndicator, DocumentTagBar},
    props: ['doc_id'],
    data() {
      return {
        documentPreview: null,
        baseUrl: baseAppURL
      }
    },
    created () {
      this.titleContent = "";
      this.previewContent = "";

      this.$store.dispatch('document/fetchPreview', this.doc_id).then(() => {
          this.documentPreview = this.documentsPreview[this.doc_id];

          this.titleContent = this.documentPreview.attributes.title;
          this.previewContent = this.documentPreview.attributes.argument ? this.documentPreview.attributes.argument : this.documentPreview.attributes.transcription;
      });

    },
    computed: {
        ...mapState('document', ['documentsPreview', 'documentLoading'])
    },
    methods: {
      getCorrespondentFullname : function(obj){
          return `${obj.correspondent.firstname} ${obj.correspondent.lastname}`
      },

    },
  }
</script>

<style scoped>


  .document-preview-card__correspondents ul {
    list-style: none;
  }

  .document-preview-card {
    margin-bottom: 6em;
    margin-top: 2em;
  }
  .document-preview-card__thumbnail {
    float: left;
    margin-right: 40px;
    height: 150px;
  }

  .document-preview-card__title{
    color: #AEAEAE;
    font-size: large;
  }

  .document-preview-card__title:hover{
    color: #3273dc;
  }


    /* styles for '...' */
  .document-preview-card__content {
    /* hide text if it more than N lines  */
    overflow: hidden;
    /* for set '...' in absolute position */
    position: relative;
    /* use this value to count block height */
    line-height: 1.2em;
    /* max-height = line-height (1.2) * lines max number (3) */
    max-height: 3.6em;
    /* fix problem when last visible word doesn't adjoin right side  */
    text-align: justify;
    /* place for '...' */
    margin-right: -1em;
    padding-right: 1em;
  }
  /* create the ... */
  .document-preview-card__content:before {
    /* points in the end */
    content: '...';
    /* absolute position */
    position: absolute;
    /* set position to right bottom corner of block */
    right: 0;
    bottom: 0;
  }
  /* hide ... if we have text, which is less than or equal to max lines */
  .document-preview-card__content:after {
    /* points in the end */
    content: '';
    /* absolute position */
    position: absolute;
    /* set position to right bottom corner of text */
    right: 0;
    /* set width and height */
    width: 1em;
    height: 1em;
    margin-top: 0.2em;
    /* bg color = bg color under block */
    background: white;
  }
</style>