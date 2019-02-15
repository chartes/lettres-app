<template>
  <span v-if="documentsPreview[docId]" class="tags has-addons">
    <a :href="`${baseUrl}/documents/${docId}`"
       class="tag document-preview-card__doc-tag">
      <span>Document {{docId}}</span>
    </a>
  
    <!--
      Bookmark
    -->
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
  
    <!--
      Lock
    -->
    <badge v-if="current_user"
           classesActive="tag is-warning"
           classesInactive="tag"
           :action-when-on="startLockEditor"
           :action-when-off="startLockEditor"
           :starts-on="lockOwner !== null"
    >
      <template #active>
        <font-awesome-icon :icon="['fas', 'lock']"/>
      </template>
      <template #activeLabel>
        <span v-if="lockOwner" class="badge-label">{{lockOwner.attributes.username}}</span>
      </template>
      <template #inactive>
        <font-awesome-icon :icon="['fas', 'unlock']"/>
      </template>
    </badge>
  
    <lock-form v-if="documentsPreview[docId] && lockEditMode"
               :doc-id="docId"
               :current-lock="documentsPreview[docId].currentLock"
               :cancel="stopLockEditor"
               :submit="stopLockEditor"
    />
  </span>
</template>

<script>
    import { mapState } from 'vuex'
    import Badge from "../ui/Badge";
    import {baseAppURL} from '../../modules/http-common';
    import http_with_csrf_token from "../../modules/http-common";
    import LockForm from "../forms/LockForm";

    export default {
        name: 'DocumentTagBar',
        components: {Badge, LockForm},
        props: {
            docId : {required: true},
        },
        computed: {
            ...mapState('user', ['current_user']),
            ...mapState('document', ['documentsPreview']),
        },
        mounted() {
            this.fetchPreviewCard();

            /* isBookmarked */
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

                isBookmarked: null,
                lockOwner: null,

                lockEditMode: false,
            }
        },
        methods: {
            addBookmark() {
                return this.$store.dispatch('bookmarks/postUserBookmark', {
                    userId: this.current_user.id,
                    docId: this.docId,
                }).then(resp => {
                    this.isBookmarked = true;
                    return Promise.resolve(true);
                })
            },
            removeBookmark() {
                return this.$store.dispatch('bookmarks/deleteUserBookmark', {
                    userId: this.current_user.id,
                    docId: this.docId,
                }).then(resp => {
                    this.isBookmarked = false;
                    return Promise.resolve(false);
                })
            },
            fetchPreviewCard() {
                this.$store.dispatch('document/fetchPreview', this.docId).then(() => {
                    /* fetch lock user info*/
                    if (this.documentsPreview[this.docId].currentLock.id) {
                        const http = http_with_csrf_token();
                        http.get(`/locks/${this.documentsPreview[this.docId].currentLock.id}/user`).then(response => {
                            this.lockOwner = response.data.data;
                        });
                    } else {
                        this.lockOwner = null;
                    }
                });
            },
            startLockEditor() {
                this.lockEditMode = true;
                return Promise.resolve(!!this.lockOwner);
            },
            stopLockEditor() {
                this.lockEditMode = false;
                this.fetchPreviewCard();
                return Promise.resolve(!!this.lockOwner);
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