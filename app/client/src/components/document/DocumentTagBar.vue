<template>
  <span v-if="documentsPreview[docId]" class="tags has-addons document-tag-bar">
    <a :href="`${baseUrl}/documents/${docId}`"
       class="tag document-preview-card__doc-tag">
      <span>Document {{docId}}</span>
    </a>
  
    <!--
      Published
    -->
    <badge v-if="current_user && isPublished !== null"
           classesActive="is-published tag"
           classesInactive="tag"
           :action-when-on="publishDocument"
           :action-when-off="unpublishDocument"
           :starts-on="isPublished"
    >
      <template #active>
        <v-icon size="14">$vuetify.icons.active_check_circle</v-icon>
      </template>
      <template #inactive>
        <v-icon size="14">$vuetify.icons.inactive_check_circle</v-icon>
      </template>
    </badge>
  
    
    <!--
      Bookmark
    -->
    <badge v-if="current_user && isBookmarked !== null"
           classesActive="is-bookmarked tag"
           classesInactive="tag"
           :action-when-on="addBookmark"
           :action-when-off="removeBookmark"
           :starts-on="isBookmarked"
    >
      <template #active>
        <v-icon size="14">$vuetify.icons.active_bookmark</v-icon>
      </template>
      <template #inactive>
        <v-icon size="14">$vuetify.icons.inactive_bookmark</v-icon>
      </template>
    </badge>
  
    <!--
      Lock
    -->
    <badge v-if="current_user"
           classesActive="is-locked tag"
           classesInactive="tag"
           :action-when-on="startLockEditor"
           :action-when-off="startLockEditor"
           :starts-on="lockOwner[docId]"
    >
      <template #active>
        <v-icon size="14">$vuetify.icons.lock</v-icon>
      </template>
      <template #activeLabel>
        <span v-if="lockOwner[docId]" class="badge-label">{{lockOwner[docId].attributes.username}}</span>
      </template>
      <template #inactive>
        <v-icon size="14">$vuetify.icons.unlock</v-icon>
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
    import {mapState} from 'vuex'
    import Badge from "../ui/Badge";
    import {baseAppURL} from '../../modules/http-common';
    import http_with_csrf_token from "../../modules/http-common";
    import LockForm from "../forms/LockForm";

    export default {
        name: 'DocumentTagBar',
        components: {Badge, LockForm},
        props: {
            docId: {required: true, type: Number},
        },
        computed: {
            ...mapState('user', ['current_user']),
            ...mapState('document', ['documentsPreview']),
            ...mapState('locks', ['lockOwner'])
        },
        mounted() {
            this.fetchPreviewCard();
        },
        data() {
            return {
                baseUrl: baseAppURL,

                isBookmarked: null,
                isPublished: null,

                lockEditMode: false,
            }
        },
        watch: {},
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
            publishDocument() {
                return this.$store.dispatch('document/publish', this.docId,
                ).then(resp => {
                    this.isPublished = true;
                    return Promise.resolve(true);
                })
            },
            unpublishDocument() {
                return this.$store.dispatch('document/unpublish', this.docId,
                ).then(resp => {
                    this.isPublished = false;
                    return Promise.resolve(false);
                })
            },
            fetchPreviewCard() {
                this.$store.dispatch('document/fetchPreview', this.docId).then(() => {
                    /* fetch lock user info*/
                    if (this.current_user) {
                        /* isBookmarked */
                        const http = http_with_csrf_token();
                        http.get(`/users/${this.current_user.id}/relationships/bookmarks`).then(response => {
                            this.isBookmarked = response.data.data.filter(d => d.id === this.docId).length > 0;
                        });
                        /* isPublished */
                        this.isPublished = this.documentsPreview[this.docId].attributes['is-published'];

                        const lockId = this.documentsPreview[this.docId].currentLock.id;
                        if (lockId) {
                            this.fetchLockOwner(lockId);
                        }
                    }
                });
            },
            fetchLockOwner(lockId) {
                return this.$store.dispatch('locks/fetchLockOwner', {docId: this.docId, lockId: lockId});
            },
            startLockEditor() {
                this.lockEditMode = true;
                return Promise.resolve(!!this.lockOwner[this.docId]);
            },
            stopLockEditor() {
                this.lockEditMode = false;
                this.fetchPreviewCard();
                return Promise.resolve(!!this.lockOwner[this.docId]);
            }
        },
    }
</script>