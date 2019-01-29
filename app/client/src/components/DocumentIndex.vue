<template>
  <div>
    <section class="documents-index columns">

      <aside class="menu documents-index__collections column is-one-fifth">
        <p class="control has-icons-left">
          <search-box :action="performSearch" :loading="documentLoading"/>
        </p>
        <p class="menu-label">
          Les collections
        </p>
          <ul  class="menu-list">
            <li><a>Toutes les collections</a></li>
            <li>
              <a class="is-active">Catherine de Médicis</a>
              <ul >
                <li><a >Lettres à Monsieur d'Abain</a></li>
                <li><a >Lettres au roi</a></li>
              </ul>
            </li>
            <li><a >Charles de Lorraine</a></li>
            <li><a >Madame de Savoye</a></li>
          </ul>
      </aside>

      <section class="column documents-index__main-column">
        <document-list v-if="!current_user"
                    :documents="documents"
                    :nb-pages="nbPages"
                    :page-size="page_size"
                    :current-page="currentPage"
                    :on-page-change="goToDocPage"
        />
        <tabs v-else tabsStyle="documents-index__main-column__tabs is-boxed is-centered">
          <tab name="Documents" :selected="true" icon-class="fas fa-file">
            <document-list
                    :documents="documents"
                    :nb-pages="nbPages"
                    :page-size="page_size"
                    :current-page="currentPage"
                    :on-page-change="goToDocPage"
            />
          </tab>
          <tab name="Mes favoris" icon-class="fas fa-bookmark">
            <bookmarks/>
          </tab>
          <tab :name="current_user.isAdmin ? 'Verrous' : 'Mes verrous'" icon-class="fas fa-lock">
            <locks :data="current_user.isAdmin ? fullLocks : userLocks"/>
          </tab>
          <tab :name="current_user.isAdmin ? 'Historique' : 'Mon historique'" icon-class="fas fa-history">
            <changelog :data="current_user.isAdmin ? fullChangelog : userChangelog"/>
          </tab>
          <tab v-if="current_user.isAdmin" name="Utilisateurs" icon-class="fas fa-users">
          </tab>
        </tabs>

      </section>

    </section>
  </div>
</template>

<script>
  import { mapState } from 'vuex';

  import SearchBox from './ui/SearchBox';
  import Tab from './ui/Tab';
  import Tabs from './ui/Tabs';
  import Bookmarks from './sections/Bookmarks';
  import Changelog from './sections/Changelog';
  import Locks from './sections/Locks';
  import DocumentList from './sections/DocumentList';

  function getUrlParameter(url, paramName) {
    paramName = paramName.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    const regex = new RegExp('[\\?&]' + paramName + '=([^&#]*)');
    let results = regex.exec(url);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
  }

  export default {

    name: 'DocumentIndex',
    components: {DocumentList, SearchBox,  Tab, Tabs, Changelog, Bookmarks, Locks},
    props: {
      page_id : {required: true},
      page_size : {required: true}
    },
    created () {
      this.$store.dispatch('user/fetchCurrent').then(response => {
        this.goToDocPage(parseInt(this.page_id));

        if (this.current_user) {
          if (this.current_user.isAdmin) {
            this.$store.dispatch('changelog/fetchFullChangelog');
            this.$store.dispatch('locks/fetchFullLocks');
          } else {
            this.$store.dispatch('changelog/fetchUserChangelog', {user: this.current_user});
            this.$store.dispatch('locks/fetchUserLocks', {user: this.current_user});
          }
        }
      });
    },
    data: function() {
      return {
        currentPage: 1
      }
    },
    computed: {
      ...mapState('document', ['documents', 'links', 'documentLoading']),
      ...mapState('user', ['current_user']),
      ...mapState('changelog', ['fullChangelog', 'userChangelog']),
      ...mapState('locks', ['fullLocks', 'userLocks']),

      nbPages() {
        return parseInt(this.links.last ? getUrlParameter(this.links.last, "page%5Bnumber%5D") : 1);
      }
    },
    methods: {
      goToDocPage(num){
          this.currentPage = num;
          if (document.getElementById("search-box") && document.getElementById("search-box").value) {
            this.performSearch(this.currentPage);
          } else {
            this.$store.dispatch('document/fetchAll', {pageId: num, pageSize: this.page_size});
          }
        },
        performSearch(numPage = 1){
          const term = document.getElementById("search-box").value;
          if (term.length > 2) {
            this.$store.dispatch('document/fetchSearch', {pageId: numPage, pageSize: this.page_size, query: term});
            this.currentPage = numPage;
          }
        }
    }
  }
</script>

<style scoped>
  .documents-index {
    padding-top: 40px;
    background: #FFFFFF;
  }

  .documents-index__collections {
      margin-left: 14px;
  }
  .documents-index__main-column {
      padding-bottom: 60px;
  }

  a.is-active {
    background: #962D3E;
  }


</style>