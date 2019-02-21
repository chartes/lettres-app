<template>


  <div class="document__collections" v-if="collections.length > 0">

    <header class="collection-list__header">
      <h2 class="collection-list__title subtitle">Collections</h2>
    </header>

    <div class="document__collections--content">

      <ul v-if="collections.length"
          v-for="collection in collections"
          class="collection-list__list"
      >
        <li class="collection-item">
          <a :href="collection.ref" target="_blank">{{collection.title}}</a>
          <a v-if="editable" @click="removeCollection(collection)" class="collection-item__delete"><icon-bin/></a>
        </li>
      </ul>

      <div v-else class="collection-list__list">
        <p class="collection-item"><em>Aucune collection n'a été renseignée</em></p>
      </div>

      <div v-if="error" class="collection-list__error notification is-danger">
        {{error}}
      </div>

      <p v-if="editable">
        <launch-button label="Ajouter une collection" @click="openCollectionEdit"/>
      </p>

    </div>


    <collection-list-form
            v-if="editMode"
            title="Ajouter une collection"
            :submit="updateCollection"
            :cancel="closeCollectionEdit"
    />

  </div>

</template>

<script>
  import { mapState } from 'vuex';
  import IconPenEdit from '../ui/icons/IconPenEdit';
  import IconBin from '../ui/icons/IconBin';
  import CollectionListForm from '../forms/CollectionListForm';
  import LaunchButton from '../forms/LaunchButton';
  export default {
    name: 'DocumentCollections',
    components: {LaunchButton, CollectionListForm, IconBin, IconPenEdit},
    props: {
      editable: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        editMode: false,
        userCanEdit: true,
        error: ''
      }
    },
    methods: {
      updateCollection (collection) {
        this.error = '';
        this.$store.dispatch('document/addCollection', collection).then(response => {
          this.closeCollectionEdit()
        })
        .catch(error => {
          this.closeCollectionEdit()
          this.error = 'Une erreur est survenue';
        })
      },
      removeCollection (collection) {
        this.$store.dispatch('document/removeCollection', collection).then(response => {
            this.closeCollectionEdit()
          })
          .catch(error => {
            this.closeCollectionEdit()
            this.error = 'Une erreur est survenue';
          })
      },
      openCollectionEdit () {
        this.editMode = true
      },
      closeCollectionEdit () {
        this.editMode = false
      },
    },
    computed: {
      ...mapState('document', ['collections']),
    },
  }
</script>

<style scoped>

</style>