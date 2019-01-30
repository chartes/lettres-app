<template>
   <section>
      <header v-if="!compact">
         <h2 class="section__title subtitle">Historique des modifications</h2>
      </header>

      <table class="table is-narrow" :class="!compact ? 'is-bordered is-striped is-hoverable' : ''">
        <thead>
          <tr>
             <th style="min-width: 180px;">
                 <button class="button is-white " disabled>Date</button>
             </th>
             <th v-if="!compact">
                 <input-filter label="Objet" place-holder="Numéro de document" :action="filterDoc"/>
             </th>
             <th>
                 <button class="button is-white " disabled>Description</button>
             </th>
             <th style="min-width: 130px;">
                 <input-filter v-if="current_user.isAdmin" label="Utilisateur" place-holder="nom d'utilisateur" :action="filterUsername"/>
                 <button v-else class="button is-white " disabled>Utilisateur</button>
             </th>
          </tr>
        </thead>

         <tbody v-for="change in fullChangelog" :key="change.id">
            <tr>
              <td>{{change.data.attributes["event-date"]}}</td>
              <td v-if="!compact">
                 <a :href="url(change.data)">
                    <span class="tag">
                        {{change.data.attributes["object-type"]}} {{change.data.attributes["object-id"]}}
                    </span>
                 </a>
              </td>
              <td>{{change.data.attributes["description"]}}</td>
              <td><span class="tag">{{change.user.username}}</span></td>
           </tr>
         </tbody>
      </table>
   </section>
</template>

<script>
  import { mapState } from 'vuex';

  import InputFilter from '../ui/InputFilter';
  import http_with_csrf_token from "../../modules/http-common";

  export default {
    name: "changelog",
    components : {InputFilter},
    props: {
      compact: {default: false}
    },
    data() {
      return {
        filteredDocId: null,
        filteredUsername: null
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
      ...mapState('changelog', ['fullChangelog'])
    },
    methods: {
       url: (entry) => `documents/${entry.attributes["object-id"]}`,
       computeFilters() {
           let _f = [];
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
             this.$store.dispatch('changelog/fetchFullChangelog', filters);
           });
       },
       filterDoc(docId) {
           this.filteredDocId = parseInt(docId);
           this.applyFilters();
       },
       filterUsername(username) {
           this.filteredUsername = username;
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
</style>
