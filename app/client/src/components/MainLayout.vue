<template>
  <v-app id="inspire">
    
    <!-- NAVIGATION -->
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
            <!-- menu head-->
            <v-list-tile slot="activator">
              <v-list-tile-content>
                <v-list-tile-title>
                  {{ item.text }}
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>

            <!-- menu children-->
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
  
          <!-- root items-->
          <v-list-tile v-else :key="item.text" @click="item.action ? item.action() : null">
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
    
    <!-- TOOLBAR -->
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
  
      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn v-if="!current_user" flat href="/lettres/users/login">Connexion</v-btn>
        <v-btn v-else flat href="/lettres/users/logout">Déconnexion</v-btn>
      </v-toolbar-items>
    </v-toolbar>
    
    
    <!-- CONTENT -->
    <v-content v-if="loaded">
      <v-container fluid fill-height :class="section === 'collections' ? 'collection-list-container' : ''">
        <!-- TEMPLATE -->
        <v-layout v-if="section === 'template'">
          
          <div v-if="template" v-html="template"></div>
        </v-layout>
        <!-- DOCUMENTS -->
        <v-layout v-else-if="section === 'documents'">
          <div v-if="template" v-html="template"> </div>
          <div v-else>
            <div v-if="displayedDocId">
              <document :doc_id="displayedDocId"></document>
            </div>
            <div v-else>
              <div v-if="documents">
                <document-list :page-size="pageSize" :current-page="currentPage" :go-to-page="goToDocPage"
                               :nb-pages="nbPages">
                </document-list>
              </div>
            </div>
          </div>
        </v-layout>
        <!-- COLLECTIONS -->
        <v-layout v-else-if="section === 'collections'">
          <div v-if="template" v-html="template"></div>
          <collection-list v-else-if="!collectionId"></collection-list>
        </v-layout>
        <!-- ERRORS -->
        <v-layout v-else-if="section === 'errors'">
          <div v-if="template" v-html="template"></div>
        </v-layout>
      </v-container>
    </v-content>
    
    <div v-if="!!displayedDocId && document && document['iiif-collection-url'].length > 0">
      <v-navigation-drawer  right  :mini-variant="!showIIIFViewer"
                           class='mt-5 homepage__iiif-viewer' width="768px" app>
        <v-container>
          <v-layout>

            <div class="uv"
                 data-locale="en-GB:English (GB),fr-FR:Français"
                 :data-uri="document['iiif-collection-url']">
            </div>
          </v-layout>
        </v-container>
        <v-btn
            absolute
            fab
            top right
            fixed
            @click="showIIIFViewer = !showIIIFViewer"
            class="homepage__iiif-viewer__toggle-btn"
        >
          <v-icon  class="homepage__iiif-viewer__toggle-icon">
            {{this.showIIIFViewer ? this.$vuetify.icons.hide : this.$vuetify.icons.show}}
          </v-icon>
        </v-btn>
      </v-navigation-drawer>

    </div>

  </v-app>
</template>

<script>
    import {mapState} from 'vuex';
    import '../plugins/vuetify';
    import SearchBox from "./ui/SearchBox";
    import {getUrlParameter} from "../modules/utils";
    import DocumentList from "./sections/DocumentList";
    import CollectionList from "./sections/CollectionList";
    import Document from "./sections/Document";
    import {baseAppURL} from "../modules/http-common";
    
    export default {
        name: 'MainLayout',
        components: {Document, DocumentList, CollectionList, SearchBox},
        props: {
            section: String,
            data: Object
        },
        created() {
            this.$store.dispatch('user/fetchCurrent').then(resp => {
                this.loaded = true;
                if (!this.docId)
                    this.goToDocPage(parseInt(this.currentPage));
            });
        },
        mounted() {
        },
        data: function () {
            return {
                currentPage: 1,
                pageSize: 15,
                loaded: false,
                
                template: this.$props.data.template,
                searchedTerm: this.$props.data.searchedTerm,
                docId: this.$props.data.docId,
                displayedDocId: this.$props.data.docId,
                collectionId: this.$props.data.collectionId,
      
                dialog: false,
                drawer: null,
                showIIIFViewer: false,
                items: [
                    {icon: 'info', text: 'À propos'},

                    {icon: 'search', text: 'Parcourir les documents', action: () => this.goToPage(baseAppURL)},
                    {icon: 'history', text: 'Recherches récentes'},
                    {icon: 'search', text: 'Parcourir les collections', action: () => this.goToPage(`${baseAppURL}/collections`)},
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
                        ]
                    },
                    {icon: 'info', text: 'Documentation'}
                ]
            }
        },
        computed: {
            ...mapState('user', ['current_user']),
            ...mapState('document', ['documents', 'document', 'links', 'documentLoading']),
            nbPages() {
                return parseInt(this.links.last ? getUrlParameter(this.links.last, "page%5Bnumber%5D") : 1);
            }
        },
        methods: {
            goToPage(url) {
                window.location.replace(url);
            },
            fetchAll() {
                this.$store.dispatch('document/fetchAll', {
                    pageId: this.currentPage,
                    pageSize: this.pageSize,
                    filters: !!this.current_user ? '' : 'filter[is-published]=true'
                }).then(r => {

                });
            },
            goToDocPage(num) {
                this.currentPage = num;
                if (this.searchedTerm && this.searchedTerm.length > 1) {
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
                    this.goToDocPage(1);
                }
            }
        }
    }
</script>
