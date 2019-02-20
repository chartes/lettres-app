<template>
  <div class="witness-list">
    <header class="witness-list__header">
      <h2 class="witness-list__title subtitle">Témoins</h2>
    </header>
    <div class="witness-list__content">
      <ul class="witness-list__list">
        <li v-for="witness, index in list" class="witness-item">
          <div class="witness-item__order" v-if="editable && list.length > 1">
            <button
                    v-if="index < list.length-1"
                    class="witness-item__order-button"
                    @click="reorderWitness(witness, 1)"
            >
              <icon-arrow-down/>
            </button>
            <button
                    v-if="index > 0"
                    class="witness-item__order-button witness-item__order-button-up"
                    @click="reorderWitness(witness, -1)"
            >
              <icon-arrow-down class="is-upside-down"/>
            </button>
          </div>
          <div class="witness-item__content">
            <p class="witness-item__text" v-html="witness.content"/>
            <a v-if="editable" @click="openWitnessEdit(witness)" class="witness-item__edit"><icon-pen-edit/></a>
            <a v-if="editable" @click="removeWitness(witness)" class="witness-item__delete"><icon-bin/></a>
          </div>
        </li>
      </ul>
      <lauch-button v-if="editable" label="Ajouter un témoin" @click="openNewWitnessEdit"/>
      <error-message :error="error"/>
    </div>
    <witness-form
            v-if="editMode == 'new' || editMode == 'edit'"
            :title="editMode == 'new' ? 'Nouveau témoin' : 'Éditer le témoin'"
            :witness="selectedWitness"
            :witnessId="selectedWitnessId"
            :submit="editMode == 'new' ? addWitness : updateWitness"
            :cancel="closeWitnessEdit"
    />
  </div>
</template>

<script>
  import IconPenEdit from '../ui/icons/IconPenEdit';
  import IconBin from '../ui/icons/IconBin';
  import WitnessForm from '../forms/WitnessForm';
  import LauchButton from '../forms/LaunchButton';
  import ErrorMessage from '../ui/ErrorMessage';
  import IconArrowDown from '../ui/icons/IconArrowDown';
  export default {
    name: 'DocumentWitnesses',
    components: {ErrorMessage, LauchButton, WitnessForm, IconBin, IconPenEdit, IconArrowDown},
    props: {
      editable: {
        type: Boolean,
        default: false
      },
      list: {
        type: Array,
        default: []
      }
    },
    data() {
      return {
        editMode: null,
        selectedWitness: null,
        selectedWitnessId: null,
        error: null
      }
    },
    methods: {
      updateWitness (witness) {
        this.removeError()
        this.$store.dispatch('document/updateWitness', witness)
          .then( response => {
            this.closeWitnessEdit()
          })
          .catch(error => {
            console.log('error', error)
          })
      },
      addWitness (witness) {
        this.removeError()
        this.$store.dispatch('document/addWitness', witness)
          .then( response => {
            this.closeWitnessEdit()
          })
          .catch(error => {
            console.log('error', error)
          })
      },
      removeWitness (witness) {
        this.removeError()
        this.$store.dispatch('document/removeWitness', witness)
          .then( response => {
            this.closeWitnessEdit()
          })
          .catch(error => {
            console.log('error', error)
          })
      },
      reorderWitness (witness, dir) {
        console.log('reorderWitness', witness, dir)
        this.$store.dispatch('document/reorderWitnesses', {witness, dir})

      },

      removeError () {
        this.error = null
      },

      openNewWitnessEdit (evt) {
        this.openWitnessEdit({
          content: '',
          institution: null,
        })
      },
      openWitnessEdit (witness) {
        this.selectedWitness = witness
        this.editMode = !!witness.id ? 'edit' : 'new'
      },
      closeWitnessEdit () {
        this.selectedWitness = null
        this.editMode = null
      },
    }
  }
</script>

<style scoped>

</style>