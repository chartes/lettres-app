<template>
  <div class="document">
    <document-tag-bar v-if="isUserLoaded" :doc-id="doc_id"/>
    
    <article v-if="document && documentsPreview[doc_id]" class="document__content" >
      <document-attributes :editable="canEdit" class="document__subsection"/>
      
      <document-witnesses :editable="canEdit" :list="witnesses"/>
      <div class="document__subsection"></div>
      <div class="columns">
        <div class="column">
          <document-persons :editable="canEdit"/>
        </div>
        <div class="column ">
          <document-placenames :editable="canEdit"/>
        </div>
      </div>
      
      <div class="document__subsection"></div>
      <document-collections :editable="canEdit" class="document__subsection"/>
      
      <document-argument :editable="canEdit" class="document__subsection"/>
      <document-transcription :editable="canEdit"/>
      
      <div style="margin-left: 0;">
        <changelog v-if="current_user" v-bind:compact="true" :doc-id="doc_id" :currentUserOnly="false" page-size="10"/>
      </div>
    </article>
    
    <loading-indicator :active="documentLoading" :full-page="true"/>
  </div>
</template>

<script>
    import { mapState } from 'vuex'
    import LoadingIndicator from './ui/LoadingIndicator';
    import Changelog from './sections/Changelog';
    import DocumentPersons from './document/DocumentPersons';
    import DocumentTranscription from './document/DocumentTranscription';
    import DocumentTagBar from "./document/DocumentTagBar";
    import DocumentPlacenames from "./document/DocumentPlacenames";
    import {baseApiURL, baseAppURL} from "../modules/http-common";
    import DocumentArgument from "./document/DocumentArgument";
    import DocumentWitnesses from "./document/DocumentWitnesses";
    import DocumentCollections from "./document/DocumentCollections";
    import DocumentAttributes from "./document/DocumentAttributes";

    export default {

        name: 'Document',
        components: {
            Changelog,
            DocumentPersons,
            DocumentPlacenames, DocumentArgument,
            DocumentTranscription,
            LoadingIndicator,
            DocumentTagBar,
            DocumentCollections,
            DocumentWitnesses,
            DocumentAttributes
        },
        props: {
            doc_id : {required: true, type: Number}
        },
        mounted () {
            this.$store.dispatch('user/fetchCurrent').then(response => {
                this.$store.dispatch('document/fetch', this.doc_id).then(r => {

                    for (let w of this.witnesses) {
               
                    }
                    
                    this.computeCanEdit();
                }).catch(e => {
                    window.location.replace(baseAppURL);
                });
            });
        },
        data() {
            return {
                canEdit: false
            }
        },
        computed: {
            ...mapState('document', [
                'document', 'documentLoading', 'documentsPreview',
                'collections', 'witnesses', 'currentLock'
            ]),
            ...mapState('user', ['current_user', 'isUserLoaded']),
            ...mapState('locks', ['lockOwner']),

            collectionURL() {
                const baseUrl = window.location.origin
                    ? window.location.origin + '/'
                    : window.location.protocol + '/' + window.location.host;
                return `${baseUrl}${baseApiURL.substr(1)}/iiif/documents/${this.doc_id}/collection/default`;
            },

        },
        watch: {
            lockOwner() {
                this.computeCanEdit();
            }
        },
        methods: {
            computeCanEdit() {
                /*
                 * Can edit if 1) You are connected 2) You are an admin or there is no active lock or the active lock is yours
                 * */
                if (!this.current_user) {
                    this.canEdit = false;
                    return;
                }

                if (this.current_user.isAdmin) {
                    this.canEdit = true;
                    return;
                }

                this.canEdit = (this.documentsPreview[this.doc_id].currentLock.id === null) || (this.lockOwner[this.doc_id] && this.lockOwner[this.doc_id].id === this.current_user.id);
            }
        }
    }
</script>

