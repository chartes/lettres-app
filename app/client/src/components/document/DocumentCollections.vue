<template>


  <div class="document__collections" v-if="collections.length > 0">

    <header>
      <h2 class="document__collections--title subtitle">Collections</h2>
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
        <a
         href="#"
         class="button"
         @click.prevent="addCollection"
        >Ajouter une collection</a>
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
  import IconPenEdit from '../forms/icons/IconPenEdit';
  import IconBin from '../forms/icons/IconBin';
  import CollectionListForm from '../forms/CollectionListForm';
  export default {
    name: 'DocumentCollections',
    components: {CollectionListForm, IconBin, IconPenEdit},
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
        console.log('updateCollection', collection)
        this.$store.dispatch('document/addCollection', collection).then(response => {
          this.closeCollectionEdit()
        })
        .catch(error => {
          this.closeCollectionEdit()
          this.error = 'Une erreur est survenue';
        })
      },
      addCollection () {
        console.log('addCollection')
        this.openCollectionEdit({
          content: '',
          institution: null,
        })
      },
      removeCollection (collection) {
        console.log('removeCollection', collection)
        this.$store.dispatch('document/removeCollection', collection).then(response => {
            this.closeCollectionEdit()
          })
          .catch(error => {
            this.closeCollectionEdit()
            this.error = 'Une erreur est survenue';
          })
      },
      openCollectionEdit () {
        console.log('openCollectionEdit')
        this.editMode = true
      },
      closeCollectionEdit () {
        console.log('closeCollectionEdit')
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