<template>
  <div class="witness-list">
    <header class="witness-list__header">
      <h2 class="witness-list__title subtitle">Témoins</h2>
    </header>
    <div class="witness-list__content">
      <ul class="witness-list__list">
        <li v-for="witness, index in list" class="witness-item">
          <div class="witness-item__order">
            <button v-if="index < list.length-1" class="witness-item__order-button"><icon-arrow-down/></button>
            <button v-if="index > 0" class="witness-item__order-button witness-item__order-button-up"><icon-arrow-down class="is-upside-down"/></button>
          </div>
          <div class="witness-item__content">
            <p class="witness-item__text" v-html="witness.content"/>
            <a if="userCanEdit" @click="openWitnessEdit(witness)" class="witness-item__edit"><icon-pen-edit/></a>
            <a if="userCanEdit" class="witness-item__delete"><icon-bin/></a>
          </div>
        </li>
      </ul>
      <lauch-button if="userCanEdit" label="Ajouter un témoin" @click="addWitness"/>
      <error-message :error="error"/>
    </div>
    <witness-form
            v-if="editMode == 'new' || editMode == 'edit'"
            :title="editMode == 'new' ? 'Nouveau témoin' : 'Éditer le témoin'"
            :witness="selectedWitness"
            :witnessId="selectedWitnessId"
            :submit="updateWitness"
            :cancel="closeWitnessEdit"
    />
  </div>
</template>

<script>
  import IconPenEdit from '../forms/icons/IconPenEdit';
  import IconBin from '../forms/icons/IconBin';
  import WitnessForm from '../forms/WitnessForm';
  import LauchButton from '../forms/LaunchButton';
  import ErrorMessage from '../ui/ErrorMessage';
  import IconArrowDown from '../forms/icons/IconArrowDown';
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
        userCanEdit: true,
        selectedWitness: null,
        selectedWitnessId: null,
        error: null
      }
    },
    methods: {
      updateWitness (witness) {
        console.log('updateWitness', witness)
        this.$store.dispatch('document/addWitness', witness)
          .catch(error => {

          })
      },
      addWitness (evt) {
        console.log('addWitness')
        this.openWitnessEdit({
          content: '',
          institution: null,
        })
      },
      openWitnessEdit (witness) {
        console.log('openWitnessEdit', witness)
        this.selectedWitness = witness
        this.editMode = !!witness ? 'edit' : 'new'
      },
      closeWitnessEdit () {
        console.log('closeWitnessEdit')
        this.selectedWitness = null
        this.editMode = null
      },
    }
  }
</script>

<style scoped>

</style>