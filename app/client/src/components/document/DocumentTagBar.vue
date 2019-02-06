<template>
   <span v-if="documentPreview" class="tags has-addons">
       <a :href="`${baseUrl}/documents/${documentPreview.id}`" class="tag document-preview-card__doc-tag">
           <span>Document {{documentPreview.id}}</span>
       </a>

       <badge v-if="current_user && isBookmarked !== null"
              classesActive="red-bookmark tag"
              classesInactive="red-bookmark tag"
              :action-when-on="addBookmark"
              :action-when-off="removeBookmark"
              :starts-on="isBookmarked"
       >
           <template #active>
               <font-awesome-icon :icon="['fas', 'bookmark']"/>
           </template>
           <template #inactive>
               <font-awesome-icon :icon="['far', 'bookmark']"/>
           </template>
       </badge>

       <badge v-if="current_user && lockOwner !== null"
              classesActive="tag is-warning"
              classesInactive="tag"
              :starts-on="documentPreview.currentLock.id"
       >
           <template #active>
               <font-awesome-icon :icon="['fas', 'lock']"/>
           </template>
           <template #activeLabel>
               <span class="badge-label">{{lockOwner.attributes.username}}</span>
           </template>
           <template #inactive>
               <font-awesome-icon :icon="['fas', 'unlock']"/>
           </template>
       </badge>

   </span>
</template>

<script>
  import { mapState } from 'vuex'
  import Badge from "../ui/Badge";
  import {baseAppURL} from '../../modules/http-common';
  import http_with_csrf_token from "../../modules/http-common";

  export default {
    name: 'DocumentTagBar',
    components: {Badge},
    props: {
        docId : {required: true},
    },
    computed: {
      ...mapState('user', ['current_user']),
      ...mapState('document', ['documentsPreview']),
    },
    created() {
      const http = http_with_csrf_token();

      if (this.documentsPreview[this.docId] === undefined) {
        this.$store.dispatch('document/fetchPreview', this.docId).then(() => {
            this.documentPreview = this.documentsPreview[this.docId];
        });
      } else {
        this.documentPreview = this.documentsPreview[this.docId];

        /* fetch lock user info*/
        if (this.documentPreview.currentLock.id) {
            console.log(this.documentPreview.currentLock);
            http.get(`/locks/${this.documentPreview.currentLock.id}/user`).then(response => {
              this.lockOwner = response.data.data;
            });
        }
      }

      /* isBookmarked */
      if (this.current_user) {
          http.get(`/users/${this.current_user.id}/relationships/bookmarks`).then(response => {
              this.isBookmarked = response.data.data.filter(d => d.id === this.docId).length > 0;
          });
      }
    },
    data() {
      return {
        baseUrl: baseAppURL,
        documentPreview: null,

        isBookmarked: null,
        lockOwner: null
      }
    },
    methods: {
      addBookmark() {
        return this.$store.dispatch('bookmarks/postUserBookmark', {
           userId: this.current_user.id,
           docId: this.docId,
        }).then(resp => {
           this.isBookmarked = true;
           return Promise.resolve(resp);
        })
      },
      removeBookmark() {
        return this.$store.dispatch('bookmarks/deleteUserBookmark', {
           userId: this.current_user.id,
           docId: this.docId,
        }).then(resp => {
           this.isBookmarked = false;
           return Promise.resolve(resp);
        })
      }
    },
  }
</script>

<style scoped>
  .red-bookmark {
    color: #9C1A1C;
  }

  .document-preview-card__doc-tag {
    float: left;
    margin-right: 20px;
  }
  .badge-label{
      margin-left: 4px;
  }
</style>