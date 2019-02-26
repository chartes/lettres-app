<template>
  <v-app id="inspire">
    <v-navigation-drawer
        v-model="drawer"
        :clipped="$vuetify.breakpoint.lgAndUp"
        fixed
        app
    >
      <v-list >
        <template v-for="item in items">
          <v-layout
              v-if="item.heading"
              :key="item.heading"
              row
              align-center
          >
          
          </v-layout>
          <v-list-group
              v-else-if="item.children"
              :key="item.text"
              v-model="item.model"
              :prepend-icon="item.model ? item.icon : item['icon-alt']"
              append-icon=""
          >
            <v-list-tile slot="activator">
              <v-list-tile-content>
                <v-list-tile-title>
                  {{ item.text }}
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile
                v-for="(child, i) in item.children"
                :key="i"
                @click=""
            >
              <v-list-tile-action v-if="child.icon">
                <v-icon>{{ child.icon }}</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>
                  {{ child.text }}
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list-group>
          <v-list-tile v-else :key="item.text" @click="">
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ item.text }}
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
        :clipped-left="$vuetify.breakpoint.lgAndUp"
        color="red darken-4"
        dark
        app
        fixed
    >
      <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
        <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        <span class="hidden-sm-and-down">Lettres</span>
      </v-toolbar-title>

      <search-box id="search-box" :action="performSearch" :loading="documentLoading"/>
      <v-spacer></v-spacer>

    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <v-layout>
          <document-list :page-size="pageSize" :current-page="currentPage" :go-to-page="goToDocPage" :nb-pages="nbPages">
          
          </document-list>
        </v-layout>
      </v-container>
    </v-content>
   
  </v-app>
</template>

<script>
    import {mapState} from 'vuex';
    import '../plugins/vuetify';
    import SearchBox from "./ui/SearchBox";
    import {getUrlParameter} from "../modules/utils";
    import DocumentList from "./sections/DocumentList";

    export default {
        name: 'HomePage',
        components: {DocumentList, SearchBox},
        props: {
            source: String
        },
        created() {
            this.goToDocPage(parseInt(this.currentPage));
            this.$store.dispatch('user/fetchCurrent').then(resp => {
                this.loaded = true;
            });
        },
        data: function () {
            return {
                currentPage: 1,
                pageSize: 15,
                loaded: false,

                dialog: false,
                drawer: null,
                items: [
                    { icon: 'contacts', text: 'Contacts'},
                    {icon: 'history', text: 'Frequently contacted'},
                    {icon: 'content_copy', text: 'Duplicates'},
                    {
                        icon: 'keyboard_arrow_up',
                        'icon-alt': 'keyboard_arrow_down',
                        text: 'Labels',
                        model: true,
                        children: [
                            {icon: 'add', text: 'Create label'}
                        ]
                    },
                    {
                        icon: 'keyboard_arrow_up',
                        'icon-alt': 'keyboard_arrow_down',
                        text: 'More',
                        model: false,
                        children: [
                            {text: 'Import'},
                            {text: 'Export'},
                            {text: 'Print'},
                            {text: 'Undo changes'},
                            {text: 'Other contacts'}
                        ]
                    },
                    {icon: 'settings', text: 'Settings'},
                    {icon: 'chat_bubble', text: 'Send feedback'},
                    {icon: 'help', text: 'Help'},
                    {icon: 'phonelink', text: 'App downloads'},
                    {icon: 'keyboard', text: 'Go to the old version'}
                ]
            }
        },
        computed: {
            ...mapState('user', ['current_user']),
            ...mapState('document', ['documents', 'links', 'documentLoading']),
            nbPages() {
                return parseInt(this.links.last ? getUrlParameter(this.links.last, "page%5Bnumber%5D") : 1);
            }
        },
        methods: {
            fetchAll() {
                this.$store.dispatch('document/fetchAll', {
                    pageId: this.currentPage,
                    pageSize: this.pageSize,
                    filters: this.current_user ? '' : 'filter[is-published]=true'
                });
            },
            goToDocPage(num) {
                this.currentPage = num;
                if (document.getElementById("search-box") && document.getElementById("search-box").value) {
                    this.performSearch(this.currentPage);
                } else {
                    this.fetchAll();
                }
            },
            performSearch(searchedValue, numPage = 1) {
                const term = searchedValue ? searchedValue : '';
                if (searchedValue.length > 1) {
                    this.$store.dispatch('document/fetchSearch', {
                        pageId: numPage,
                        pageSize: this.pageSize,
                        query: term
                    });
                    this.currentPage = numPage;
                } else {
                    document.getElementById("search-box").value = null;
                    this.goToDocPage(1);
                }
            }
        }
    }
</script>

<style scoped>

</style>