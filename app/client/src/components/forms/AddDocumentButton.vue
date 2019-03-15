<template>
  <div>
    <v-btn @click="opened = true" :disabled="opened">
      <v-icon small left>fas fa-plus</v-icon>
      Ajouter un nouveau document à la collection
    </v-btn>
    <v-slide-y-transition>
    <v-card flat v-if="opened" trans>
      <v-card-text >
        <v-container fluid>
          <v-layout wrap>
            <new-document :defaultCollection="collection"></new-document>
          </v-layout>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="normal"  large @click="cancel">Annuler</v-btn>
        <v-btn color="normal"  large @click="submit">Ajouter</v-btn>
      </v-card-actions>
      <v-divider></v-divider>
    </v-card>
    </v-slide-y-transition>
  </div>
</template>

<script>
    import {mapState} from 'vuex';
    import NewDocument from "../sections/NewDocument";

    export default {
        name: "add-document-button",
        components: {
          NewDocument
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
                this.opened = false;
                console.log("dummy doc must be transform into proper doc:", this.document);
            }
        },
        computed: {
            ...mapState('document', ['document', 'documentLoading', 'witnesses']),

        }
    }
</script>