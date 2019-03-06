<template>
  <v-card fill-height>
    <v-toolbar
        card
        color="grey lighten-3"
    >
      <v-toolbar-title>Les collections de documents</v-toolbar-title>
    </v-toolbar>
    
    <v-layout>
      <v-flex>
        <v-card-text>
          <v-treeview
              v-model="tree"
              :load-children="fetch"
              :items="items"
              item-text="title"
              activatable
              active-class="grey lighten-4 red--text"
              selected-color="red"
              open-on-click
              open-all
              selectable
              :transition="true"
              expand-icon="arrow_drop_down"
              on-icon="fa fa-check-square"
              off-icon="far fa-check-square"
          >
            <template v-slot:prepend="{ item, active, value, open, selected }">
              [ {{active}} & {{value}} & {{open}} & {{selected}}]
              <v-icon>fa fa-check-circle</v-icon>
            </template>
          </v-treeview>
        </v-card-text>
      </v-flex>
      
      <v-divider vertical></v-divider>
      
      <v-flex
          xs12
          md6
      >
        <v-card-text>
          <div
              v-if="selections.length === 0"
              class="title font-weight-light grey--text pa-3 text-xs-center"
          >
            Sélectionnez une collection
          </div>
          
          <v-scroll-x-transition
              group
              hide-on-leave
          >
            <v-chip
                v-for="(selection, i) in selections"
                :key="i"
                color="grey"
                dark
                small
            >
              <v-icon left small>mdi-beer</v-icon>
              {{ selection.title }}
            </v-chip>
          </v-scroll-x-transition>
        </v-card-text>
      </v-flex>
    </v-layout>
    <v-divider></v-divider>
  
    <v-card-actions>
      <v-btn
          flat
          @click="tree = []"
      >
        Reset
      </v-btn>
    
      <v-spacer></v-spacer>
    
      <v-btn
          class="white--text"
          color="green darken-1"
          depressed
      >
        Save
        <v-icon right>mdi-content-save</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
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
                tree: []
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
            ...mapState('collections', ['allCollectionsWithParents', 'fullHierarchy']),

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
                        console.log(collection, leaf, collection.id === leaf);
                        return collection.id === leaf
                    });
                    if (!collection) continue;
                    selections.push(collection)
                }
                return selections
            },
            shouldShowTree() {
                return this.collection.length > 0 && !this.isLoading
            }
        },
        watch: {
            breweries(val) {
            
            }
        },
    }
</script>

