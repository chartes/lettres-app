<template>
  <div>
    <section class="documents-index columns">

      <aside class="menu documents-index__collections column is-one-fifth">
        <hello-world></hello-world>
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

      <section v-if="loaded" class="column documents-index__main-column">
          <div v-if="!current_user" class="container is-fluid">
            <document-list :page-size="pageSize"/>
          </div>
          <tabs v-else tabsStyle="documents-index__main-column__tabs is-boxed is-centered">
            <tab name="Documents" :selected="true" icon-class="fas fa-file">
              <div class="container is-fluid">
                <document-list :page-size="pageSize"/>
              </div>
            </tab>
            <tab name="Mes favoris" icon-class="fas fa-bookmark">
              <div class="container is-fluid">
                <bookmarks page-size="25"/>
              </div>
            </tab>
            <tab :name="current_user.isAdmin ? 'Verrous' : 'Mes verrous'" icon-class="fas fa-lock">
              <div class="container is-fluid">
                <locks page-size="25"/>
              </div>
            </tab>
            <tab :name="current_user.isAdmin ? 'Historique' : 'Mon historique'" icon-class="fas fa-history">
              <div class="container is-fluid">
                <changelog page-size="25" :currentUserOnly="true" />
              </div>
            </tab>
            <tab v-if="current_user.isAdmin" name="Utilisateurs" icon-class="fas fa-users">
              <div class="container is-fluid">
              </div>
            </tab>
          </tabs>
      </section>

    </section>
  </div>
</template>

<script>
  import { mapState } from 'vuex';
  import '../plugins/vuetify';

  import Tab from './ui/Tab';
  import Tabs from './ui/Tabs';
  import Bookmarks from './sections/Bookmarks';
  import Changelog from './sections/Changelog';
  import Locks from './sections/Locks';
  import DocumentList from './sections/DocumentList';
  import HelloWorld from "./HelloWorld";

  export default {

    name: 'DocumentIndex',
    components: {DocumentList, Tab, Tabs, Changelog, Bookmarks, Locks, HelloWorld},
    props: {
    },
    created () {
      this.$store.dispatch('user/fetchCurrent').then(resp => {
          this.loaded = true;
      });
    },
    data: function() {
      return {
        pageSize: 15,

        loaded: false
      }
    },
    computed: {
      ...mapState('user', ['current_user']),
    },
    methods: {
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
    min-height: 700px;
  }

  a.is-active {
    background: #962D3E;
  }
  .container {
    margin-top: 70px;
  }

</style>