<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  
  <div class="document__collections" >
    
    <header class="collection-list__header">
      <h2 class="collection-list__title subtitle">
        Collections
        <a v-if="editable" class="tag" href="#" @click="openCollectionEdit">
          <icon-add/>
        </a>
      </h2>
      <h3 v-if="collectionsHierarchies.length > 0" >
        Ce document fait partie des collections suivantes :
      </h3>
    </header>
    

    <div class="document__collections--content">
        <span  v-for="hierarchy in collectionsHierarchies" :key="hierarchy.id">
          <v-layout row>
            <v-flex shrink pa-1>
              <v-breadcrumbs tag="span" :items="hierarchy" divider=">">
                <template v-slot:item="props">
                  <a :href="`/lettres/collections/${props.item.id}`">{{ props.item.title}}</a>
                </template>
              </v-breadcrumbs>
            </v-flex>
            <v-flex pa-1 :fill-height="true" :align-baseline="true">
              <a v-if="editable && collectionsHierarchies.length > 1" @click="removeCollection(hierarchy[hierarchy.length-1])" class="collection-item__delete">
                <icon-bin/>
              </a>
            </v-flex>
          </v-layout>
        </span>
        <div v-if="collectionsHierarchies.length === 0" class="collection-list__list">
          <p class="collection-item"><em>Aucune collection n'a été renseignée</em></p>
        </div>
      
      <div v-if="error" class="collection-list__error notification is-danger">
        {{error}}
      </div>
    
    </div>
    
    <collection-list-form
        v-if="editMode"
        title="Ajouter le document à une collection"
        :submit="updateCollection"
        :cancel="closeCollectionEdit"
    />
  
  </div>

</template>

<script>
    import { mapState, mapGetters } from 'vuex';
    import IconPenEdit from '../ui/icons/IconPenEdit';
    import IconBin from '../ui/icons/IconBin';
    import CollectionListForm from '../forms/CollectionListForm';
    import LaunchButton from '../forms/LaunchButton';
    import IconAdd from "../ui/icons/IconAdd";
    export default {
        name: 'DocumentCollections',
        components: {LaunchButton, CollectionListForm, IconBin, IconPenEdit, IconAdd},
        props: {
            editable: {
                type: Boolean,
                default: false
            },
            refetch: {
                type: Boolean,
                default: true
            }
        },
        data() {
            return {
                editMode: false,
                userCanEdit: true,
                error: '',

                collectionsHierarchies: []
            }
        },
        created() {
            if (this.refetch) {
                this.$store.dispatch('collections/fetchAll').then(r => {
                    this.refreshHierarchies();
                });
            } else {
                this.refreshHierarchies();
            }
        },
        methods: {
            updateCollection (collection) {
                this.error = '';
                this.$store.dispatch('document/addCollection', collection).then(response => {
                    this.closeCollectionEdit();
                })
                    .catch(error => {
                        this.closeCollectionEdit()
                        this.error = 'Une erreur est survenue';
                    })

            },
            removeCollection (collection) {
                this.isLoading = true;
                this.$store.dispatch('document/removeCollection', collection).then(response => {
                    this.closeCollectionEdit();
                })
                    .catch(error => {
                        this.closeCollectionEdit()
                        this.error = 'Une erreur est survenue';
                    })
            },
            openCollectionEdit () {
                this.editMode = true
            },
            closeCollectionEdit () {
                this.editMode = false
            },
            refreshHierarchies() {
                this.collectionsHierarchies = this.collections.map(c => {
                    let node = this.searchWithinTree(c.id);
                    let h;
                    if (node !== null && node.parents) {
                      h = node.parents.slice().reverse();
                      h.push(c);
                    } else {
                      h = [c];
                    }
                    return h;
                });

                this.collectionsHierarchies.sort(function (a, b) {
                    if ( a.length === b.length) return 0;
                    return a.length > b.length ? 1 : -1;
                });
            }
        },
        watch: {
            collections(val) {
                this.refreshHierarchies();
            },
            fullHierarchy(val) {
                this.refreshHierarchies();
            }
        },
        computed: {
            ...mapState('document', ['collections']),
            ...mapState('collections', ['allCollectionsWithParents', 'fullHierarchy']),
            ...mapGetters('collections', ['searchWithinTree']),

        },
    }
</script>

<style scoped>

</style>