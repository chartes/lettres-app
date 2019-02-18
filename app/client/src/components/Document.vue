<template>
  <div class="document">
  
    <document-tag-bar v-if="isUserLoaded" :doc-id="doc_id"/>
    
    <article v-if="document && documentsPreview[doc_id]" class="document__content" >
      <div class="columns">
        <div class="column">
          <document-notice :editable="canEdit"/>
          <document-correspondents :editable="canEdit"/>
          <document-transcription :editable="canEdit"/>
        </div>
        <div class="column is-one-quarter">
        
        </div>
      </div>
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
    import DocumentNotice from './document/DocumentNotice';
    import DocumentCorrespondents from './document/DocumentCorrespondents';
    import DocumentTranscription from './document/DocumentTranscription';
    import DocumentTagBar from "./document/DocumentTagBar";

    export default {

        name: 'Document',
        components: {Changelog, DocumentCorrespondents, DocumentNotice, DocumentTranscription, LoadingIndicator, DocumentTagBar},
        props: {
            doc_id : {required: true, type: Number}
        },
        created () {
            this.$store.dispatch('user/fetchCurrent').then(response => {
                this.$store.dispatch('document/fetch', this.doc_id).then(response => {
                    this.computeCanEdit();
                });
            });
        },
        data() {
            return {
                canEdit: false
            }
        },
        computed: {
            ...mapState('document', ['document', 'documentLoading', 'documentsPreview']),
            ...mapState('user', ['current_user', 'isUserLoaded']),
            ...mapState('locks', ['lockOwner']),
        },
        watch: {

        },
        methods: {
            computeCanEdit() {
                /*
                 * Can edit if 1) You are connected 2) You are an admin or there is no active lock or the active lock is yours
                 * */
                if (!this.current_user)
                    return false;
                if (this.current_user.isAdmin)
                    return true;
                this.canEdit = (this.documentsPreview[this.doc_id].currentLock.id === null) || (this.lockOwner[this.doc_id] && this.lockOwner[this.doc_id].id === this.current_user.id);
            }
        }
    }
</script>

