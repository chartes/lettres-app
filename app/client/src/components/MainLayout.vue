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
            <v-list-tile slot="activator" @click="item.action ? item.action() : null">
              <v-list-tile-content :class="menuItemClasses(item)">
                <v-list-tile-title>
                  {{ item.text }}
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>

            <!-- menu children-->
            <v-list-tile
                v-for="(child, i) in item.children"
                :key="i"
                @click="child.action ? child.action() : null"
            >
              <v-list-tile-action v-if="child.icon">
                <v-icon>{{ child.icon }}</v-icon>
              </v-list-tile-action>
              <v-list-tile-content :class="menuItemClasses(child)">
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
            <v-list-tile-content :class="menuItemClasses(item)">
              <v-list-tile-title>
                {{ item.text }}
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>
  
      <v-container grid-list-md text-xs-center class="main-layout__sponsors">
        <v-layout row wrap>
          <v-flex xs12>
            <a href="http://www.cths.fr">
            <img src="/lettres/static/images/Comité_des_travaux_historiques_et_scientifiques_logo.svg"
                   alt="cths" width="90"/>
            </a>
          </v-flex>
          <v-flex xs12>
            <a href="http://www.chartes.psl.eu">
              <img src="/lettres/static/images/logo-ecole-nationale-des-chartes-header.png"
                   alt="chartes" width="210"/>
            </a>
          </v-flex>
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
        <v-toolbar-side-icon @click.stop="drawer = !drawer">
          <v-icon>fas fa-bars</v-icon>
        </v-toolbar-side-icon>
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
          <!-- SINGLE DOCUMENT -->
          <div v-if="template" v-html="template"> </div>
          <div v-else>
            <div v-if="displayedDocId">
              <document :doc_id="displayedDocId"></document>
            </div>
            <div v-else>
              <!-- DOCUMENT LIST -->
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
        <!-- LOCKS -->
        <v-layout v-else-if="section === 'locks'">
          <div v-if="template" v-html="template"></div>
          <locks :compact="false" pageSize="40"></locks>
        </v-layout>
        <!-- BOOKMARKS -->
        <v-layout v-else-if="section === 'bookmarks'">
          <div v-if="template" v-html="template"></div>
          <bookmarks pageSize="40"></bookmarks>
        </v-layout>
        <!-- CHANGELOG -->
        <v-layout v-else-if="section === 'changelog'">
          <div v-if="template" v-html="template"></div>
          <changelog pageSize="40"></changelog>
        </v-layout>
        <!-- ERRORS -->
        <v-layout v-else-if="section === 'errors'">
          <div v-if="template" v-html="template"></div>
        </v-layout>
      </v-container>
    </v-content>
    
    <div>
      <v-navigation-drawer right  :mini-variant="!showIIIFViewer" v-if="docId"
                           class='mt-5 homepage__iiif-viewer' width="768px" app>
        <v-container>
          <v-layout id="uv-layout">
            <!-- MOVE THE UV HERE WHEN THE VUE IS MOUNTED-->
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
    import Locks from "./sections/Locks";
    import Bookmarks from "./sections/Bookmarks";
    import Changelog from "./sections/Changelog";
    
    export default {
        name: 'MainLayout',
        components: {Document, DocumentList, CollectionList, SearchBox, Locks, Bookmarks, Changelog},
        props: {
            section: String,
            data: Object
        },
        created() {
            this.$store.dispatch('user/fetchCurrent').then(resp => {
                this.loaded = true;
                if (this.docId !== undefined)
                    this.goToDocPage(parseInt(this.currentPage));
                
                if (this.current_user === null){
                    //remove sections from the menu
                    this.items.splice(this.findMenuItem('last_searches'), 1)
                    this.items.splice(this.findMenuItem('account'), 1);
                    this.items.splice(this.findMenuItem('params'), 1);
                }
            });
        },
        mounted() {
            const selected = this.highlightMenuItem(this.items, this.section);
            console.warn(this.section, selected);

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
                    {name: 'documents', icon: 'search', text: 'Parcourir les documents',
                        action: () => this.goToPage(baseAppURL)},
                    {name: 'last_searches', icon: 'history', text: 'Recherches récentes',
                        action: () => this.goToPage(`${baseAppURL}/recherches-recentes`)},
                    {name: 'collections', icon: 'search', text: 'Parcourir les collections',
                        action: () => this.goToPage(`${baseAppURL}/collections`)},
                    {
                        icon: 'keyboard_arrow_up',
                        'icon-alt': 'keyboard_arrow_down',
                        text: 'Mon compte',
                        model: true,
                        name: 'account',
                        children: [
                            {name: 'profile', icon: 'content_copy',text: 'Mon profil'},
                            {name: 'bookmarks', icon: 'content_copy',text: 'Mes favoris',
                                action: () => this.goToPage(`${baseAppURL}/favoris`)},
                            {name: 'changelog', icon: 'content_copy',text: 'Mon historique',
                                action: () => this.goToPage(`${baseAppURL}/historique`)},
                            {name: 'locks', icon: 'content_copy',text: 'Mes documents verouillés',
                                action: () => this.goToPage(`${baseAppURL}/verrous`)},
                        ]
                    },
                    {
                        icon: 'keyboard_arrow_up',
                        'icon-alt': 'keyboard_arrow_down',
                        text: 'Paramétrage',
                        model: false,
                        name: 'params',
                        children: [
                            {name: 'users', icon: 'contacts', text: 'Contributeurs',
                                action: () => this.goToPage(`${baseAppURL}/contributeurs`)},
                            {name: 'refs', icon: 'content_copy', text: 'Référentiels de données',
                                action: () => this.goToPage(`${baseAppURL}/referentiels`)},
                        ]
                    },
                    {name: 'about', icon: 'info', text: 'À propos', action: () => this.goToPage(`${baseAppURL}/a-propos`)},
                    {icon: 'info', text: 'Documentation', action: () => this.goToPage(`${baseAppURL}/documentation`)}
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
                    filters: !!this.current_user ? '' : 'filter[is-published]=1'
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
            },
            highlightMenuItem(items, name) {
                for (let item of items) {
                    if (item.name === name) {
                        item.selected = true;
                        return true;
                    } else if (item.children) {
                        return this.highlightMenuItem(item.children, name);
                    }
                }
                return false;
            },
            findMenuItem(name) {
                let i = 0;
                for (let item of this.items) {
                    if (item.name === name)
                        return i;
                    i += 1;
                }
                return null;
            },
            menuItemClasses(item) {
                if (item.selected) {
                    return "red--text";
                } else {
                    return "";
                }
            }
        }
        
    }
</script>
