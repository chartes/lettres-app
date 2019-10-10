<template>
  <div>
    <v-btn @click="opened = true" :disabled="opened">
      <v-icon small left>fas fa-plus</v-icon>
      Ajouter un nouveau document à la collection
    </v-btn>
    <v-slide-y-transition>
    <v-card flat v-show="opened" trans>
      <v-card-text >
        <v-card-title>
          <span class="title">Témoin de base du document</span>
        </v-card-title>
        <v-container fluid>
          <v-layout wrap>
            <loading-indicator :active="loading"/>
            <div class="witness-form textinput-form" v-if="!loading">
              <form @submit.prevent="">
      
                <div class="columns">
                  <div class="column">
                  <field-select
                      label="Statut"
                      :options="statusesList"
                      v-model="witness.status"
                  />
                  </div>
                  <div class="column">
                  <field-select
                      label="Tradition"
                      :options="traditionsList"
                      v-model="witness.tradition"
                  />
                  </div>
                  <div class="column">
                    <institution-list-form :witness="witness"></institution-list-form>
                  </div>
                </div>

                <rich-text-editor
                    label="Témoin"
                    v-model="witness.content"
                    :formats="[['italic','superscript'], ['note','link']] "
                    :options="{placeholder: 'Ex. Bibl. nat. Fr., Français 3512, fol. 53r'}"
                />
                <rich-text-editor
                    label="Cote / unité de conservation"
                    v-model="witness['classification-mark']"
                    :formats="[['italic','superscript'], ['link']]"
                    :options="{placeholder: 'Ex. Français 3512, Ms. 564, K 35'}"
                />
              </form>
            </div>
            
          </v-layout>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="normal"  large @click="cancel">Annuler</v-btn>
        <v-btn  color="normal"  large @click="submit" >Créer le document</v-btn>
      </v-card-actions>
      <v-divider></v-divider>
    </v-card>
    </v-slide-y-transition>
  </div>
</template>

<script>
    import {mapState} from 'vuex';
    import LoadingIndicator from "../ui/LoadingIndicator";
    import SelectAutocompleteField from "./fields/SelectAutocompleteField";
    import RichTextEditor from "./fields/RichTextEditor";
    import FieldLabel from "./fields/FieldLabel";
    import FieldText from "./fields/TextField";
    import FieldSelect from "./fields/SelectField";
    import {statuses, traditions} from './data';
    import {baseAppURL} from "../../modules/http-common";
    import InstitutionListForm from "./InstitutionListForm";

    export default {
        name: "add-document-button",
        components: {
            InstitutionListForm,
            LoadingIndicator,
            SelectAutocompleteField,
            RichTextEditor,
            FieldLabel,
            FieldSelect,
            FieldText,
        },
        props: {
            collection: {
                required: true,
                type: Object
            }
        },
        data() {
            return {
              opened: false,
              witness: {content: 'Ceci est le témoin de base. Éditez-le !'},
              loading: false,
              institutionForm: false,
              institutionError: null,
            }
        },
        created() {
            this.opened = false;
        },
        mounted() {
            this.opened = false;
        },
        methods: {
            cancel() {
                this.opened = false;
            },
            submit() {
            	  // fix bug
                if (this.witness.tradition === '') {
	                this.witness.tradition = null;
                }
            	
                this.opened = false;
                this.$store.dispatch('user/fetchCurrent').then(response => {
                    const defaultData = {
                        relationships: {
                            collections: {
                                data: [
                                    {type: "collection", id: this.collection.id}
                                ]
                            }
                        }
                    };
                    return this.$store.dispatch('document/initializeDummyDocument', defaultData).then(r => {
                        this.isLoading = false;
                        console.warn("submitting", this.document, this.witness);
                        console.warn("must create the doc");
                        this.$store.dispatch('document/add').then(r => {
                            console.warn("then the witness");
                            this.$store.dispatch('document/addWitness', this.witness).then(w => {
                                window.location.href = `${baseAppURL}/documents/${this.document.id}`;
                            });
                        });
                    }).catch(e => {
                        console.warn("ERROR", e);
                    });
                })
            },

            searchInstitution(search) {
                this.$store.dispatch('institutions/search', search)
            },

            submitInstitutionForm(inst) {
                this.institutionError = null;
                this.$store.dispatch('institutions/addOne', inst)
                    .then(response => {
                        this.witness.institution = response
                        this.closeInstitutionForm()
                    })
                    .catch(error => {
                        console.log(error)
                        this.institutionError = error.toString()
                    })
            },
            openInstitutionForm() {
                this.institutionForm = true
            },
            closeInstitutionForm() {
                this.institutionForm = false
            },

        },
        computed: {
            ...mapState('document', ['document', 'documentLoading', 'witnesses']),
            ...mapState('witnesses', ['currentWitness']),
            ...mapState('institutions', ['institutionsSearchResults']),
            statusesList() {
                return statuses;
            },
            traditionsList() {
                return traditions;
            },
            isValid() {
                return this.witness.content && this.witness.content.length >= 1 && this.witness.content !== '<p><br></p>'
            }
        },
        watch: {
            currentWitness(val) {
                this.witness = {...val}
                this.loading = false
            }
        },
    }
</script>
