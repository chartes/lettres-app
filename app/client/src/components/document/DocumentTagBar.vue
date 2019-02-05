<template>
   <span v-if="documentPreview" class="tags has-addons">
       <a :href="`${baseUrl}/documents/${documentPreview.id}`" class="tag document-preview-card__doc-tag">
           <span>Document {{documentPreview.id}}</span>
       </a>
       <badge v-if="current_user && isBookmarked !== null"
              fontawesomeIcon="bookmark"
              classes-active="red-bookmark tag"
              classes-inactive="red-bookmark tag"
              :action-when-on="addBookmark"
              :action-when-off="removeBookmark"
              :starts-on="isBookmarked"
       />
       <span v-if="current_user && documentPreview.currentLock.id" class="tag is-warning">
           <i class="fas fa-lock"></i>
       </span>
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
        if (this.documentsPreview[this.docId] === undefined) {
          this.$store.dispatch('document/fetchPreview', this.docId).then(() => {
              this.documentPreview = this.documentsPreview[this.docId];
          });
        } else {
          this.documentPreview = this.documentsPreview[this.docId];
        }

        if (this.current_user) {
            const http = http_with_csrf_token();
            http.get(`/users/${this.current_user.id}/relationships/bookmarks`).then(response => {
                this.isBookmarked = response.data.data.filter(d => d.id === this.docId).length > 0;
            });
      }
    },
    data() {
      return {
        baseUrl: baseAppURL,
        documentPreview: null,
        isBookmarked: null
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
</style>