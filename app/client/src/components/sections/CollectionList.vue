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
              item-text="titleWithCount"
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
          <v-tab-item :transition="false" :reverse-transition="false"
              v-for="(selection, i) in selections"
              :key="i"
          >
            <v-card flat fill-height>
              <v-card-text>
                <v-card-actions>
                  <p>{{ selection.description }}</p>
                  <v-spacer vertical></v-spacer>
                </v-card-actions>
                
                <v-divider></v-divider>
                <add-document-button :key="selectedCollection" v-if="current_user"></add-document-button>
  
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
    import { mapState} from 'vuex';
    import DocumentList from "./DocumentList";
    import {getUrlParameter} from "../../modules/utils";
    import * as _ from "lodash";
    import AddDocumentButton from "../forms/AddDocumentButton";

    export default {
        name: "collection-list",
        components: {DocumentList, AddDocumentButton},
        props: {

        },
        data () {
            return {
                tree: [],
                checkboxes: [],
                activeTab: 0,
                activeTreeItem: [],
                search: null,
                caseSensitive: false,
                open: [],

                currentPage: 1,
                pageSize: 10,
            }
        },
        created() {
            this.$store.dispatch('user/fetchCurrent').then(resp => {
                this.$store.dispatch('collections/fetchAll').then(resp => {

                });
            });
        },
        methods: {
            fetchSearch() {
                if (this.selectedCollection !== null){
                    console.warn("FETCH SEARCH")
                    this.$store.dispatch('document/fetchSearch', {
                        pageId: this.currentPage,
                        pageSize: this.pageSize,
                        query: this.query,
                        filters: `sort=id`
                    })
                }
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
            query() {
                const collectionFilter = `collections.id:${this.selectedCollection}`;
                const publishedFilfer =  `${this.current_user ? '' : 'is-published:true'}`;
                if (publishedFilfer.length > 0) {
                    return `(${collectionFilter} AND ${publishedFilfer})`
                } else {
                    return collectionFilter;
                }
            },
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
                return this.activeTab !== null && this.selections[this.activeTab] ? this.selections[this.activeTab].id : null;
            },

        },
        watch: {
            allCollectionsWithParents(val) {
                if (val !== null) {
                    this.open = val.map(c => c.id);
                }
            },
            activeTreeItem(val) {
                if (val && val.length > 0) {
                    this.tree = [val[0]]
                } else {
                    this.tree = [];
                }
            },
            selections(val) {
                //this.goToDocPage(1);
            },
            activeTab(val, oldVal) {
                if (val !== oldVal) {
                    console.log("activeTab", val);
                    this.goToDocPage(1);
                }
            },
            tree(val, oldVal) {
                console.log("tree", val, oldVal, this.activeTreeItem);
                if ((val && val.length === 1) || val[val.length-1] === this.activeTreeItem[0]) {
                    if (!_.isEqual(_.sortBy(val), _.sortBy(oldVal))) {
                        this.goToDocPage(1);
                    }
                }
            }
        },

    }
</script>

