<template>
  <v-container class="collection-list-container" grid-list-md fluid fill-height>
  
      <v-layout row wrap>
        <v-flex xs5>
          <v-treeview
              v-model="tree"
              :items="items"
              item-text="title"
              activatable
              active-class="grey lighten-4 red--text"
              selected-color="red"
              open-all
              selectable
              :transition="true"
              expand-icon="arrow_drop_down"
              on-icon="fa fa-check-square"
              off-icon="far fa-check-square">
    
            <template v-slot:prepend="{ item, active, value, open, selected }">
              <!-- {{active}} & {{selected}} -->
              <v-icon class="collection-list-container__checkbox">far fa-check-square</v-icon>
            </template>
          </v-treeview>
        </v-flex>
        <v-flex xs7 v-if="selections && selections.length > 0" class="collection-list-container__tabs">
          <v-tabs
              v-model="active"
              color="darkgrey"
              dark
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
                <v-card-text v-if="active === i">
                  {{ selection.description }}
                  <document-list :page-size="1" :current-page="1" :go-to-page="goToDocPage"
                                 :nb-pages="1">
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
    
    export default {
        name: "collection-list",
        components: {DocumentList},
        props: {

        },
        data () {
            return {
                isLoading: false,
                tree: [],
                checkboxes: [],
                active: null,
                drawer: null,

                currentPage: 1,
                pageSize: 15,
            }
        },
        created() {
            this.$store.dispatch('user/fetchCurrent').then(resp => {
                this.$store.dispatch('collections/fetchAll');
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
            ...mapState('collections', ['fullHierarchy', 'allCollectionsWithParents']),
            ...mapState('document', ['documents']),

            filter() {
                return this.caseSensitive
                    ? (item, search, textKey) => item[textKey].indexOf(search) > -1
                    : undefined
            },
            items() {
                return [{
                    id: -1,
                    title: 'Toutes les collections',
                    children: this.fullHierarchy
                }]
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
               return this.active !== null && this.selections[this.active] ? this.selections[this.active].id : null;
            }
        },
        watch: {
            selections(val) {
                this.active = null;
            },
            selectedCollection(val) {
                if (val) {
                   this.goToDocPage(1);
                }
            }
        },
        
    }
</script>

