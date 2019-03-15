<template>
  <div v-if="!isLoading" class="document">
    <article class="document__content">
      <document-attributes :editable="canEdit"  class="document__subsection"/>
      <small class="blue--text">Ajoutez au moins un témoin pour valider la création de ce document</small>
      <document-witnesses :editable="canEdit" :list="witnesses"/>
      <div class="document__subsection"></div>
      <document-collections :editable="canEdit" :refetch="false" class="document__subsection"/>
      <document-argument :editable="canEdit" class="document__subsection"/>
      <document-transcription :editable="canEdit"/>
    </article>
    <loading-indicator :active="documentLoading" :full-page="true"/>
  </div>
</template>

<script>
    import {mapState, mapGetters} from 'vuex'
    import LoadingIndicator from '../ui/LoadingIndicator';
    import DocumentWitnesses from "../document/DocumentWitnesses";
    import DocumentAttributes from "../document/DocumentAttributes";
    import DocumentPersons from "../document/DocumentPersons";
    import DocumentPlacenames from "../document/DocumentPlacenames";
    import DocumentArgument from "../document/DocumentArgument";
    import DocumentTranscription from "../document/DocumentTranscription";
    import DocumentCollections from "../document/DocumentCollections";

    export default {

        name: 'NewDocument',
        components: {
            DocumentPersons,
            DocumentPlacenames,
            DocumentArgument,
            DocumentTranscription,
            LoadingIndicator,
            DocumentCollections,
            DocumentWitnesses,
            DocumentAttributes
        },
        props: {
            defaultCollection: {
                required: true,
                type: Object
            }
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
                const defaultData = {
                    relationships: {
                        collections: {
                            data: [
                                {type:"collection", id: this.defaultCollection.id}
                            ]
                        }
                    }
                };
                return this.$store.dispatch('document/initializeDummyDocument', defaultData).then(r => {
                    const dummyDocId = this.getDummyDocument().data.id;
                    console.warn('dummy;', dummyDocId);
                    return this.$store.dispatch('document/fetch', dummyDocId).then(r => {
                        this.isLoading = false;
                    })
                }).catch(e => {
                    console.warn("ERROR", e);
                });
            })
        },
        data() {
            return {
                canEdit: true,
                isLoading: true
            }
        },
        computed: {
            ...mapState('document', [
                'document', 'documentLoading', 'collections', 'witnesses'
            ]),
            ...mapState('user', ['current_user']),
            ...mapGetters('document', ['getDummyDocument']),
        },
        watch: {
    
        },
        methods: {
    
        }
    }
</script>

