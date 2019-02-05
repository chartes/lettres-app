<template>
   <section>
      <header v-if="!compact">
         <h2 class="section__title subtitle">Statut des verrouillages</h2>
      </header>

      <pagination :current="currentPage" :end="nbPages" :size="pageSize" :action="goToLocksPage" :bottom-widget="!compact">
          <table class="table container is-narrow" :class="!compact ? 'is-bordered is-striped is-hoverable' : ''">
            <thead>
              <tr>
                  <!--
                 <th style="min-width: 180px;">
                     <button class="button is-white " disabled>Date</button>
                 </th> -->
                 <th style="min-width: 180px;">
                     <button class="button is-white " disabled>Date d'expiration</button>
                 </th>
                 <th>
                     <input-filter label="Statut" place-holder="A ou E (Actif ou Expiré)" :action="filterStatus"/>
                 </th>
                 <th v-if="!compact">
                     <input-filter label="Objet" place-holder="Numéro de document" :action="filterDoc"/>
                 </th>
                 <th style="min-width: 130px;">
                     <input-filter v-if="current_user.isAdmin" label="Utilisateur" place-holder="nom d'utilisateur" :action="filterUsername"/>
                     <button v-else class="button is-white " disabled>Utilisateur</button>
                 </th>
                 <th>
                     <button class="button is-white " disabled>Description</button>
                 </th>
              </tr>
            </thead>

             <tbody v-for="lock in fullLocks" :key="lock.id">
                <tr>
                  <!--<td>{{lock.data.attributes["event-date"]}}</td> -->
                  <td>{{lock.data.attributes["expiration-date"]}}</td>
                  <td>
                      <span v-if="lock.data.attributes['is-active']" class="tag is-warning status">Actif</span>
                      <span v-else class="tag is-static status">Expiré</span>
                  </td>
                  <td v-if="!compact">
                     <a :href="url(lock.data)">
                        <span class="tag">
                            {{lock.data.attributes["object-type"]}} {{lock.data.attributes["object-id"]}}
                        </span>
                     </a>
                  </td>
                  <td><span class="tag">{{lock.user.username}}</span></td>
                  <td>{{lock.data.attributes["description"]}}</td>
               </tr>
             </tbody>
          </table>
      </pagination>

   </section>
</template>

<script>
  import { mapState } from 'vuex';

  import InputFilter from '../ui/InputFilter';
  import Pagination from '../ui/Pagination';

  import http_with_csrf_token from "../../modules/http-common";
  import {getUrlParameter} from "../../modules/utils";

  export default {
    name: "locks",
    components : {InputFilter, Pagination},
    props: {
      compact: {default: false},
      pageSize : {required: true},
    },
    data() {
      return {
        filteredDocId: null,
        filteredUsername: null,
        filteredStatus: null,

        currentPage: 1
      }
    },
    created() {
      if (this.current_user.isAdmin) {
        this.applyFilters();
      }  else {
        this.filterUsername(this.current_user.username);
      }
    },
    computed: {
      ...mapState('user', ['current_user']),
      ...mapState('locks', ['fullLocks', 'links']),
      nbPages() {
        return parseInt(this.links.last ? getUrlParameter(this.links.last, "page%5Bnumber%5D") : 1);
      }
    },
    methods: {
       url: (entry) => `documents/${entry.attributes["object-id"]}`,
       computeFilters() {
           let _f = [];
           /* compute the status filter */
           if (this.filteredStatus) {
              _f.push(this.filteredStatus.startsWith("E") ? `filter[!is-active]`: `filter[is-active]`);
           }
           /* compute the document filter */
           if (this.filteredDocId) {
              _f.push(`filter[object-type]=document&filter[object-id]=${this.filteredDocId}`);
           }
           /* compute the user filter by fetching the user id from a username */
           if (this.filteredUsername) {
             const http = http_with_csrf_token();
             return http.get(`users?filter[username]=${this.filteredUsername}&without-relationships`).then( response => {
                try {
                   const userId = response.data.data[0].id;
                   _f.push(`filter[user_id]=${userId}`);
                } catch(err) {
                  console.warn(`username \'${this.filteredUsername}\' unknown`);
                }
                return _f.join('&');
             });
           }
           return new Promise((resolve) => {resolve(_f.join('&'))});
       },
       applyFilters() {
           this.computeFilters().then(filters => {
             console.info(filters);
             this.$store.dispatch('locks/fetchFullLocks', {
               pageId: this.currentPage,
               pageSize: this.pageSize,
               filters :filters
             });
           });
       },
       filterDoc(docId) {
           this.filteredDocId = parseInt(docId);
           this.currentPage = 1;
           this.applyFilters();
       },
       filterUsername(username) {
           this.filteredUsername = username;
           this.currentPage = 1;
           this.applyFilters();
       },
       filterStatus(status) {
           this.filteredStatus = status ? status.toUpperCase() : '';
           this.currentPage = 1;
           this.applyFilters();
       },
       goToLocksPage(num) {
           this.currentPage = num;
           this.applyFilters();
       }
    }
  }
</script>

<style scoped>
  .section__title {
    margin-bottom: 20px;
  }
  td {
    color: #962D3E;
  }
  td a:hover span{
    background: #EBEBEB;
    color: #348899 ;
  }
  span.status {
      width: 80px;
  }
</style>
