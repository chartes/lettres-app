<template>
  <v-container class="collection-list-container" grid-list-md fluid fill-height>
    
    <v-layout row wrap>
      <v-flex xs3>
        <v-sheet class="pa-3 collection-list-container__search">
          <v-text-field
              v-model="search"
              label="Chercher une collection"
              flat
              clearable
              clear-icon="fas fa-times-circle"
          ></v-text-field>
        </v-sheet>
        <div class="collection-list-container__treeview-container">
          <v-treeview
              v-model="tree"
              :items="items"
              item-text="title"
              :search="search"
              :filter="filter"
              selectable
              selected-color="red"
              :activatable="true"
              :active.sync="activeTreeItem"
              active-class="grey lighten-4 red--text"
              :open="open"
              :open-all="true"
              :transition="true"
              expand-icon="arrow_drop_down"
              on-icon="fa fa-check-square"
              off-icon="far fa-check-square">
            <!--
                       <template v-slot:prepend="{ item, active, value, open, selected }">
                        {{active}} & {{selected}}
              <v-icon class="collection-list-container__checkbox">far fa-check-square</v-icon>
            </template>
             -->
          </v-treeview>
        </div>
      </v-flex>
      <v-flex xs9 v-if="selections && selections.length > 0" class="collection-list-container__tabs">
        <v-tabs
            v-model="activeTab"
            height="64"
            slider-color="red"
            next-icon="$vuetify.icons.nextstep"
            prev-icon="$vuetify.icons.previousstep"
        >
          <v-tab
              v-for="(selection, i) in selections"
              :key="i"
              ripple
              class="collection-list-container__tab"
          >
            {{ selection.title }}
          </v-tab>
          <v-tab-item
              v-for="(selection, i) in selections"
              :key="i"
          >
            <v-card flat fill-height>
              <v-card-text v-if="activeTab === i">
                <p>{{ selection.description }}</p>
                <v-divider></v-divider>
                <document-list :page-size="pageSize" :current-page="currentPage" :go-to-page="goToDocPage"
                               :nb-pages="nbPages">
                </document-list>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs>
      </v-flex>
    </v-layout>
  
  </v-container>
</template>

<script>
    import { mapState } from 'vuex';
    import DocumentList from "./DocumentList";
    import {getUrlParameter} from "../../modules/utils";

    export default {
        name: "collection-list",
        components: {DocumentList},
        props: {

        },
        data () {
            return {
                tree: [],
                checkboxes: [],
                activeTab: null,
                activeTreeItem: null,
                drawer: null,
                search: null,
                caseSensitive: false,
                open: [],
                
                currentPage: 1,
                pageSize: 15,
            }
        },
        created() {
            this.$store.dispatch('user/fetchCurrent').then(resp => {
                this.$store.dispatch('collections/fetchAll').then(resp => {
                   this.open =  this.allCollectionsWithParents.map( c => c.id);
                });
            });
        },
        methods: {
            fetchSearch() {
                this.$store.dispatch('document/fetchSearch', {
                    pageId: this.currentPage,
                    pageSize: this.pageSize,
                    query: `collections.id:${this.selectedCollection}`,
                    filters: `sort=id${this.current_user ? '' : '&filter[is-published]=1'}`
                })
            },
            goToDocPage(num) {
                this.currentPage = num;
                this.fetchSearch();
            }
        },
        computed: {
            ...mapState('user', ['current_user']),
            ...mapState('collections', ['fullHierarchy', 'allCollectionsWithParents',]),
            ...mapState('document', ['documents', 'links']),

            filter() {
                return this.caseSensitive
                    ? (item, search, textKey) => item[textKey].indexOf(search) > -1
                    : undefined
            },
            items() {
                return this.fullHierarchy
            },
            nbPages() {
                return parseInt(this.links.last ? getUrlParameter(this.links.last, "page%5Bnumber%5D") : 1);
            },
            selections() {
                const selections = [];
                for (const leaf of this.tree) {
                    const collection = this.allCollectionsWithParents.find(collection => {
                        return collection.id === leaf
                    });
                    if (!collection) continue;
                    selections.push(collection)
                }
                return selections
            },
            selectedCollection(){
                return this.activeTab !== null && this.selections[this.active] ? this.selections[this.activeTab].id : null;
            },
            
        },
        watch: {
            activeTreeItem(val) {
              if (val && val.length > 0) {
                  this.tree = [val[0]]
              } else {
                  this.tree = [];
              }
            },
            selections(val) {
                this.activeTab = null;
            },
            selectedCollection(val) {
                if (val) {
                    this.goToDocPage(1);
                }
            }
        },

    }
</script>

