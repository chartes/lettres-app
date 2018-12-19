<template>
  <section class="document__preview-card">
    <article v-if="documentPreview">

      <header class="title">
        <a :href="`${baseURL}/documents/${documentPreview.id}`">
          <h1>{{documentPreview.attributes.title}}</h1>
        </a>
      </header>

      <div class="content">
         <div class="columns">
           <div class="column is-three-quarters">
             <p>{{documentPreview.attributes.argument}}</p>
           </div>
           <div class="column correspondents">
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
    <loading-indicator :active="documentLoading" :full-page="true"/>
  </section>
</template>

<script>
  import { mapState } from 'vuex'
  import LoadingIndicator from './ui/LoadingIndicator';
  import DocumentAttributes from './document/DocumentAttributes';
  import {baseAppURL} from '../modules/http-common';

  export default {

    name: 'DocumentPreviewCard',
    components: {DocumentAttributes, LoadingIndicator},
    props: ['doc_id'],
    data() {
      return {
        documentPreview: null,
        baseURL: baseAppURL
      }
    },
    created () {

      this.$store.dispatch('document/fetchPreview', this.doc_id).then(() => {
          this.documentPreview = this.documentsPreview[this.doc_id];
      })
      /*this.$store.dispatch('user/setAuthToken', this.auth_token).then(() => {
          this.$store.dispatch('user/getCurrentUser').then(() => {
            return this.$store.dispatch('document/fetch', this.doc_id)
          });
      });
       */
    },
    computed: {
        ...mapState('document', ['documentsPreview', 'documentLoading']),
    },
    methods: {
      getCorrespondentFullname : function(obj){
          return `${obj.correspondent.firstname} ${obj.correspondent.lastname}`
      }
    },
  }
</script>

<style scoped>
  .correspondents ul {
    list-style: none;
  }

  article {
   margin-bottom: 1.5em;
  }

  h1{
    color: #AEAEAE;
  }

  h1:hover{
    color: #1BBC9B;
  }
</style>