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
      
      <v-container>
        <v-layout >
          <v-img  src="/lettres/static/images/logo-ecole-nationale-des-chartes-header.png"
                  :max-height="260" :max-width="260">
          </v-img>
        </v-layout>
      </v-container>
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
        <span class="hidden-sm-and-down"><v-btn flat href="/lettres/documents">Projet Lettres</v-btn></span>
      </v-toolbar-title>

      <search-box id="search-box" :action="performSearch" :value="searchedTerm" :loading="documentLoading"/>
      <v-spacer></v-spacer>

    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <v-layout>
          <document v-if="displayedDocId" :doc_id="displayedDocId">
          
          </document>
          <document-list v-else :page-size="pageSize" :current-page="currentPage" :go-to-page="goToDocPage" :nb-pages="nbPages">
          
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
    import Document from "./Document";
    
    export default {
        name: 'HomePage',
        components: {Document, DocumentList, SearchBox},
        props: {
            searchedTerm: String,
            docId: Number
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
                displayedDocId: this.$props.docId,

                dialog: false,
                drawer: null,
                items: [
                    {icon: 'info', text: 'À propos'},

                    {icon: 'content_copy', text: 'Parcourir les collections'},
                    {icon: 'history', text: 'Recherches récentes'},
                    {
                        icon: 'keyboard_arrow_up',
                        'icon-alt': 'keyboard_arrow_down',
                        text: 'Mon compte',
                        model: true,
                        children: [
                            {icon: 'content_copy',text: 'Mon profil'},
                            {icon: 'content_copy',text: 'Mes favoris'},
                            {icon: 'content_copy',text: 'Mon historique'},
                            {icon: 'content_copy',text: 'Mes documents verouillés'},
                        ]
                    },
                    {
                        icon: 'keyboard_arrow_up',
                        'icon-alt': 'keyboard_arrow_down',
                        text: 'Paramétrage',
                        model: false,
                        children: [
                            {icon: 'contacts', text: 'Contributeurs'},
                            {icon: 'content_copy', text: 'Référentiels de données'},
                            {icon: 'content_copy', text: 'Collections de documents'},
                        ]
                    },
                    {icon: 'info', text: 'Documentation'}
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
                if (this.searchedTerm) {
                    this.performSearch(this.searchedTerm, this.currentPage);
                } else {
                    this.fetchAll();
                }
            },
            performSearch(searchedValue, numPage = 1) {
                const term = searchedValue ? searchedValue : '';
                if (searchedValue.length > 1) {
                    this.displayedDocId = null;

                    this.$store.dispatch('document/fetchSearch', {
                        pageId: numPage,
                        pageSize: this.pageSize,
                        query: term
                    });
                    this.currentPage = numPage;
                } else {
                    //document.getElementById("search-box").value = null;
                    this.goToDocPage(1);
                }
            }
        }
    }
</script>

<style scoped>

</style>