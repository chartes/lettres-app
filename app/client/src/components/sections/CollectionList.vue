<template>
  <v-container class="collection-list-container" fluid>
    <v-toolbar
        card
        color="grey lighten-3"
    >
      <v-toolbar-title>Les collections de documents</v-toolbar-title>
    </v-toolbar>
    
    <v-layout>
      <v-flex xs6>
          <v-treeview
              v-model="tree"
              :load-children="fetch"
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
              off-icon="far fa-check-square"
          >
            <template v-slot:prepend="{ item, active, value, open, selected }">
              {{active}} & {{selected}}
              <v-icon style="font-size:20px">far fa-check-square</v-icon>
            </template>
          </v-treeview>
      </v-flex>
      
      <v-divider vertical></v-divider>
      
      <v-flex xs6>
          <div v-if="selections.length === 0" class="title font-weight-light grey--text pa-3 text-xs-center">
            Sélectionnez une collection pour afficher ses documents
          </div>
          
          <v-scroll-x-transition group hide-on-leave>
            <div class="tag"
                v-for="(selection, i) in selections"
                :key="i"
            >
              {{ selection.title }}
            </div>
          </v-scroll-x-transition>
      </v-flex>
    </v-layout>
    <v-divider></v-divider>
  </v-container>
</template>

<script>
    import { mapState } from 'vuex';
    
    export default {
        name: "collection-list",
        components: {},
        props: {

        },
        data () {
            return {
                isLoading: false,
                tree: [],
                checkboxes: []
            }
        },
        created() {
            this.$store.dispatch('collections/fetchAll').then(r => {
            
            });
        },
        methods: {
          fetch() {
      
          }
        },
        computed: {
            ...mapState('user', ['current_user']),
            ...mapState('collections', ['fullHierarchy', 'allCollectionsWithParents']),

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
            }
        },
        watch: {
            selections() {
            
            }
        },
    }
</script>

