<template>
  <div v-if="!isLoading" class="document">
    <document-tag-bar v-if="isUserLoaded" :doc-id="doc_id"/>
    
    <article v-if="document && documentsPreview[doc_id]" class="document__content" >
  
      <!-- titre et langue -->
      <document-attributes :editable="canEdit"/>
  
      <!-- dates de lieux et de temps -->
      <div class="panel mt-5">
        <p class="panel-heading">Dates</p>
        <div class="panel-block">
          <document-date-attributes :editable="canEdit"/>
        </div>
        <div class="panel-block">
          <document-placenames :editable="canEdit"/>
        </div>
      </div>
  
      <!-- correspondents -->
      <document-persons :editable="canEdit"/>
     
      <!-- témoins -->
      <document-witnesses :editable="canEdit" :list="witnesses"/>

      <!-- collections -->
      <document-collections :editable="canEdit"/>

      <div class="mt-5">
        <!-- analyse -->
        <document-argument :editable="canEdit"/>
  
        <!-- transcription -->
        <document-transcription :editable="canEdit"/>
      </div>

      <div class="mt-5" style="margin-left: 0;">
        <changelog v-if="current_user" v-bind:compact="true" :doc-id="doc_id" :currentUserOnly="false" page-size="10"/>
      </div>
    </article>
    
    <loading-indicator :active="documentLoading" :full-page="true"/>
  </div>
</template>

<script>
    import { mapState } from 'vuex'
    import LoadingIndicator from '../ui/LoadingIndicator';
    import Changelog from './Changelog';
    import DocumentPersons from '../document/DocumentPersons';
    import DocumentTranscription from '../document/DocumentTranscription';
    import DocumentTagBar from "../document/DocumentTagBar";
    import DocumentPlacenames from "../document/DocumentPlacenames";
    import {baseApiURL, baseAppURL} from "../../modules/http-common";
    import DocumentArgument from "../document/DocumentArgument";
    import DocumentWitnesses from "../document/DocumentWitnesses";
    import DocumentCollections from "../document/DocumentCollections";
    import DocumentAttributes from "../document/DocumentAttributes";
    import DocumentDateAttributes from "../document/DocumentDateAttributes";

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
            DocumentAttributes,
            DocumentDateAttributes,
        },
        props: {
            doc_id : {required: true, type: Number}
        },
        created () {
            const uvLayout = document.getElementById('uv-layout');
            const uv = document.getElementById('uv');
            uvLayout.appendChild(uv);
        },
        mounted () {
            this.isLoading = true;
            this.$store.dispatch('user/fetchCurrent').then(response => {
                this.$store.dispatch('document/fetch', this.doc_id).then(r => {
                    
                    this.computeCanEdit();
                    this.isLoading = false;
                }).catch(e => {
                    console.warn("ERROR", e);
                    //window.location.replace(baseAppURL);
                });
            });
        },
        data() {
            return {
                canEdit: false,
                isLoading: true
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
            },
            documentsPreview() {
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
                this.canEdit = (this.documentsPreview[this.doc_id] && this.documentsPreview[this.doc_id].currentLock.id === null) || (this.lockOwner[this.doc_id] && this.lockOwner[this.doc_id].id === this.current_user.id);
            }
        }
    }
</script>

