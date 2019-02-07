<template>
  
  <modal-form class="lock-form"
      :title="title"
      :cancel="cancelAction"
      :submit="submitAction"
      :remove="lock.id ? removeAction: undefined"
      :valid="true"
      :submitting="false"
      submit-text="Verrouiller"
      remove-text="Déverrouiller"
  >
     <!-- Non-admin features -->
     <div>
       <div v-if="lock.id && !loading">
         <p>
           Le <b>document {{docId}}</b> est actuellement verrouillé par <b>{{lockOwner.attributes.username}}</b>.
         </p>
         <article class="message lock-form__description">
           <div class="message-body">
             <u>
               Raison invoquée :</u>
            
             {{lock.description}}
           </div>
         </article>
       </div>
       <div v-else>
         <p>
           Vous pouvez verrouiller le <b>document {{docId}}</b> pour une période renouvelable de sept
           jours.
         </p>
       </div>
     </div>
     <!-- Admin features -->
     <div v-if="current_user.isAdmin">
       <loading-indicator :active="loading"/>
       <div class="" v-if="!loading">
         <form @submit.prevent="">
           
           <select-autocomplete-field
               label="Choisir le propriétaire du verrou"
               v-model="nextLockOwner"
               :items="usersSearchResults"
               :is-async="true"
               @search="searchUser"
               label-key="username"
           >
           </select-autocomplete-field>
       
         </form>
       </div>
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
                nextLockOwner: null,
                
                loading: true
            }
        },
        mounted () {
            this.fetchLock();
            this.nextLockOwner = this.current_user;
        },
        methods: {
            submitAction() {
                if (this.nextLock) {
                    this.saveLock().then(resp => {
                        this.$props.submit();
                    });
                }
            },
            cancelAction() {
                this.$props.cancel();
            },
            removeAction() {
                this.removeLock().then(resp => {
                    this.$props.submit();
                });
            },
            fetchLock() {
                this.loading = true;
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
               /*
                const http = http_with_csrf_token();
               console.warn("Lock conflict management must be implemented in both back & front end!");
               return http.post(`/locks`, {data: this.nextLock}).then(response => {
                   console.warn("LOCK SAVED", response);
               });
               */
                return this.$store.dispatch('locks/saveLock', this.nextLock);
            },
            removeLock() {
                return this.$store.dispatch('locks/removeLock', this.lock);
            },
            searchUser(search) {
                return this.$store.dispatch('user/search', search);
            },
        },
        watch: {
            currentLock: () => {this.fetchLock();},
        },
        computed: {
            ...mapState('user', ['current_user', 'usersSearchResults']) ,
            nextLock() {
                if (this.nextLockOwner) {
                    return {
                        type: 'lock',
                        attributes: {
                            description: 'Ceci est la raison pour laquelle je décide de verouiller ce document.',
                            'object-type': 'document',
                            'object-id' : this.docId
                        },
                        relationships: {
                            user: {
                                data: [{type: 'user', id: this.nextLockOwner.id}]
                            }
                        }
                    }
                }
            }
        }
    }
</script>
