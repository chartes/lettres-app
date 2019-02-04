<template>
   <section>
      <header>
         <h2 class="section__title subtitle">Mes documents mis en favoris</h2>
      </header>

      <pagination :current="currentPage" :end="nbPages" :size="pageSize" :action="goToBookmarkPage">
          <table class="table is-narrow is-bordered is-striped is-hoverable container" >
            <thead>
              <tr>
                 <th><button class="button is-white " disabled>Action</button></th>
                 <th>
                    <!--<input-filter label="Objet" place-holder="Numéro de document" :action="filterDoc"/>-->
                    <button class="button is-white " disabled>Document</button>
                 </th>
                 <th>
                    <button class="button is-white " disabled>Titre</button>
                 </th>
                 <th>
                    <button class="button is-white " disabled>Témoin(s)</button>
                 </th>
              </tr>
            </thead>
             <tbody>
                <tr v-for="bookmark in userBookmarks" :key="bookmark.id">
                  <td><button class="button" @click="removeBookmark(bookmark.id)">Retirer</button></td>
                  <td>
                     <a :href="url(bookmark)">
                        <span class="tag">
                            Document {{bookmark.id}}
                        </span>
                     </a>
                  </td>
                  <td  v-html="bookmark.attributes['title']"></td>
                  <td>
                     <ul>
                        <li v-for="witness in bookmark.witnesses" :key="witness.id"><span v-html="witness.attributes.content" style="font-size: 0.8em"></span></li>
                     </ul>
                  </td>
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

  import {getUrlParameter} from "../../modules/utils";

  export default {
    name: "bookmarks",
    components : {InputFilter, Pagination},
    props: {
      docId: {required: false},
      pageSize : {required: true},
    },
    data() {
      return {
        filteredDocId: null,

        currentPage: 1
      }
    },
    created() {
      this.applyFilters();
    },
    computed: {
      ...mapState('user', ['current_user']),
      ...mapState('bookmarks', ['userBookmarks', 'links']),
      nbPages() {
        return parseInt(this.links.last ? getUrlParameter(this.links.last, "page%5Bnumber%5D") : 1);
      }
    },
    methods: {
       url: (doc) => `documents/${doc.id}`,
       computeFilters() {
           let _f = [];
           /* compute the document filter */
           if (this.docId || this.filteredDocId) {
               const objectId = this.docId ? this.docId : this.filteredDocId;
              _f.push(`filter[bookmarks.id]=${objectId}`);
           }

           return new Promise((resolve) => {resolve(_f.join('&'))});
       },
       applyFilters() {
           return this.computeFilters().then(filters => {
             this.$store.dispatch('bookmarks/fetchUserBookmarks', {
               userId: this.current_user.id,
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

       goToBookmarkPage(num) {
          console.warn('GOT TO', num);

           this.currentPage = num;
           this.applyFilters();
       },

       removeBookmark(docId){
          this.$store.dispatch('bookmarks/deleteBookmark', {
             userId: this.current_user.id,
             docId: docId,
           }).then(response => {
             //refresh the bookmark list
             this.goToBookmarkPage(this.currentPage);
          });
       }
    }
  }
</script>

<style scoped>
  table {
    min-width: 75%;
  }
  .section__title {
    margin-bottom: 20px;
  }
  td {

  }
  td a:hover span{
    background: #EBEBEB;
    color: #348899 ;
  }
</style>
