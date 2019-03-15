<template>
  <div v-if="!isLoading" class="document">
    <article class="document__content">
      <document-attributes :editable="true" :edit-attributes="false" class="document__subsection"/>
      <document-witnesses :editable="true" :list="witnesses"/>
    </article>
    <loading-indicator :active="documentLoading" :full-page="true"/>
  </div>
</template>

<script>
    import {mapState} from 'vuex'
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

    export default {

        name: 'NewDocument',
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
        
        },
        created() {
            /*
            const uvLayout = document.getElementById('uv-layout');
            const uv = document.getElementById('uv');
            uvLayout.appendChild(uv);
            */
        },
        mounted() {
            this.isLoading = true;
            this.$store.dispatch('user/fetchCurrent').then(response => {
                
                this.$store.dispatch('document/fetch', this.docId).then(r => {
                    this.isLoading = false;
                }).catch(e => {
                    console.warn("ERROR", e);
                    //window.location.replace(baseAppURL);
                });
            });
        },
        data() {
            return {
                docId: -1,
                isLoading: true
            }
        },
        computed: {
            ...mapState('document', ['document', 'documentLoading', 'witnesses']),
            ...mapState('user', ['current_user', 'isUserLoaded']),

            collectionURL() {
                const baseUrl = window.location.origin
                    ? window.location.origin + '/'
                    : window.location.protocol + '/' + window.location.host;
                return `${baseUrl}${baseApiURL.substr(1)}/iiif/documents/${this.docId}/collection/default`;
            },

        },
        watch: {
        
        },
        methods: {
        
        }
    }
</script>

