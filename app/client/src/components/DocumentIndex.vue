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

        <div v-if="current_user" class="documents-index__main-column__tabs tabs is-centered is-boxed">
          <ul>
            <li id="documents-index__main-column__documents__tab" class="tab">
              <a @click="goToTab('documents-index__main-column__documents')">
                <span class="icon is-small"><i class="fas fa-file" aria-hidden="true"></i></span>
                <span>Documents</span>
              </a>
            </li>
            <li id="documents-index__main-column__my-bookmarks__tab" class="tab">
              <a @click="goToTab('documents-index__main-column__my-bookmarks')">
                <span class="icon is-small"><i class="fas fa-bookmark" aria-hidden="true"></i></span>
                <span>Mes favoris</span>
              </a>
            </li>
            <li id="documents-index__main-column__my-locks__tab" class="tab">
              <a @click="goToTab('documents-index__main-column__my-locks')">
                <span class="icon is-small"><i class="fas fa-lock" aria-hidden="true"></i></span>
                <span>Mes verrous</span>
              </a>
            </li>
            <li id="documents-index__main-column__my-changelog__tab" class="tab">
              <a @click="goToTab('documents-index__main-column__my-changelog')">
                <span class="icon is-small"><i class="fas fa-history" aria-hidden="true"></i></span>
                <span>Mon historique</span>
              </a>
            </li>

            <li v-if="current_user && current_user.isAdmin">
              <span style="min-width: 80px; display: block;"></span>
            </li>
            <li v-if="current_user && current_user.isAdmin" id="documents-index__main-column__all-locks__tab" class="tab">
              <a @click="goToTab('documents-index__main-column__all-locks')">
                <span class="icon is-small"><i class="fas fa-lock" aria-hidden="true"></i></span>
                <span>Tous les verrous</span>
              </a>

            <li v-if="current_user && current_user.isAdmin" id="documents-index__main-column__all-changelog__tab" class="tab">
              <a @click="goToTab('documents-index__main-column__all-changelog')">
                <span class="icon is-small"><i class="fas fa-user-lock" aria-hidden="true"></i></span>
                <span>Historique général</span>
              </a>
            </li>
            <li v-if="current_user && current_user.isAdmin" id="documents-index__main-column__all-users__tab" class="tab">
              <a @click="goToTab('documents-index__main-column__all-users')">
                <span class="icon is-small"><i class="fas fa-users" aria-hidden="true"></i></span>
                <span>Utilisateurs</span>
              </a>
            </li>

          </ul>
        </div>

        <div id="documents-index__main-column__documents" class="tab-container">
          <pagination :current="currentPage" :end="nbPages" :size="page_size" :action="goToDocPage"/>
          <ul id="preview-cards" >
            <li v-for="doc in documents" :key="doc.id">
              <document-preview-card :doc_id="doc.id"></document-preview-card>
            </li>
          </ul>
          <pagination :current="currentPage" :end="nbPages" :size="page_size" :action="goToDocPage"/>
        </div>

        <div v-if="current_user" id="documents-index__main-column__my-bookmarks" class="tab-container">
        </div>
        <div v-if="current_user" id="documents-index__main-column__my-locks" class="tab-container">
        </div>
        <div v-if="current_user" id="documents-index__main-column__my-changelog" class="tab-container">
        </div>
        <div v-if="current_user && current_user.isAdmin" id="documents-index__main-column__all-locks tab-container" class="tab-container">
        </div>
        <div v-if="current_user && current_user.isAdmin" id="documents-index__main-column__all-changelog tab-container" class="tab-container">
        </div>
        <div v-if="current_user && current_user.isAdmin" id="documents-index__main-column__all-users tab-container" class="tab-container">
        </div>

      </section>

    </section>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import DocumentPreviewCard from './DocumentPreviewCard';
  import Pagination from './ui/Pagination';
  import SearchBox from './ui/SearchBox';

  function getUrlParameter(url, paramName) {
    paramName = paramName.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + paramName + '=([^&#]*)');
    var results = regex.exec(url);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
  }

  export default {

    name: 'DocumentIndex',
    components: {DocumentPreviewCard, Pagination, SearchBox},
    props: {
      "page_id" : {required: true},
      "page_size" : {required: true}
    },
    created () {

      this.$store.dispatch('user/fetchCurrent').then(response => {
        this.goToTab(this.currentTabName);
        this.goToDocPage(parseInt(this.page_id));
      });
    },
    data: function() {
      return {
        currentPage: 1,
        currentTabName: 'documents-index__main-column__documents'
      }
    },
    computed: {
      ...mapState('document', ['documents', 'links', 'documentLoading']),
      ...mapState('user', ['current_user']),
      nbPages() {
        return parseInt(this.links.last ? getUrlParameter(this.links.last, "page%5Bnumber%5D") : 1);
      }
    },
    methods: {
        goToTab(tabname) {
          /* hide everything */
          const tabContainers = document.getElementsByClassName('tab-container');
          for (let i = 0; i < tabContainers.length; ++i ) {
            tabContainers[i].classList.add('is-invisible');
          }
          const tabs = document.getElementsByClassName('tab');
          for (let i = 0; i < tabs.length; ++i ) {
            tabs[i].classList.remove('is-active');
          }
          /* then show selectively */
          const currentTab = document.getElementById(tabname+"__tab");
          if (currentTab) {
            currentTab.classList.add('is-active');
            document.getElementById(tabname).classList.remove('is-invisible');
            this.currentTabName = tabname;
          }
        },
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
    background: #962D3E ;
  }
  .documents-index__main-column__tabs {
    margin-bottom: 80px;
  }
  .documents-index__main-column__tabs  li.is-active a {
    color: #962D3E ;
  }
</style>