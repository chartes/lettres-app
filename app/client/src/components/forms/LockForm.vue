<template>
  
  <modal-form
      :title="title"
      :cancel="cancelAction"
      :submit="submitAction"
      :valid="true"
      :submitting="false"
  >
    <loading-indicator :active="loading"/>
    <div class="location-form textinput-form" v-if="!loading">
      <form @submit.prevent="">
        <field-select
                      label="Propriétaire du verrou"
                      :options="userList"
                      v-model="nextLockOwnerId"
        />
      </form>
    </div>
  </modal-form>

</template>

<script>

    import { mapState } from 'vuex';

    import ModalForm from './ModalForm';
    import FieldLabel from './fields/FieldLabel';
    import FieldSelect from './fields/SelectField';
    import FieldText from './fields/TextField';
    import SelectAutocompleteField from './fields/SelectAutocompleteField';
    import LoadingIndicator from '../ui/LoadingIndicator';
    import http_with_csrf_token from "../../modules/http-common";

    export default {
        name: "lock-form",
        components: {
            LoadingIndicator,
            SelectAutocompleteField,
            FieldLabel,
            FieldSelect,
            FieldText,
            ModalForm
        },
        props: {
            docId: {required: true},
            currentLock: { type: Object, default: null },
            cancel: { type: Function},
            submit: { type: Function}
        },
        data() {
            return {
                title: 'Verrouillage du document',
                
                lock: {...this.$props.currentLock},
                lockOwner: null,
                nextLockOwnerId: null,
                
                loading: true
            }
        },
        created () {
            this.fetchLock();
            this.nextLockOwnerId = this.current_user.id;
        },
        methods: {
            submitAction () {
                if (this.nextLock) {
                    this.saveLock().then(resp => {
                        this.$props.submit();
                    });
                }
            },
            cancelAction () {
                this.$props.cancel();
            },
            fetchLock() {
                this.lock = this.$props.currentLock;
                /* fetch lock user info*/
                if (this.lock && this.lock.id) {
                    const http = http_with_csrf_token();
                    http.get(`/locks/${this.lock.id}/user`).then(response => {
                        this.lockOwner = response.data.data;
                        this.loading = false;
                    });
                } else {
                    this.loading = false;
                }
            },
            saveLock() {
               const http = http_with_csrf_token();
               return http.post(`/locks`, {data: this.nextLock}).then(response => {
                   console.warn("LOCK SAVED", response);
               });
            }
        },
        watch: {
            currentLock: () => {this.fetchLock();},
        },
        computed: {
            ...mapState('user', ['current_user']) ,
            userList() {
                if (this.current_user.isAdmin) {
                    return [{id: 1, label: 'admin'},
                        {id: 2, label: 'contributor'}]
                } else {
                    return [{id: this.current_user.id, label: this.current_user.username}]
                }
            },
            nextLock() {
                if (this.nextLockOwnerId) {
                    return {
                        type: 'lock',
                        attributes: {
                            description: 'NEXT LOCK',
                            'object-type': 'document',
                            'object-id' : this.docId
                        },
                        relationships: {
                            user: {
                                data: [{type: 'user', id: this.nextLockOwnerId}]
                            }
                        }
                    }
                }
            }
        }
    }
</script>