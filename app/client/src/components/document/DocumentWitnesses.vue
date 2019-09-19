<template>
  <section class="witness-list">
    <div class="panel mt-4">
      <header class="panel-heading">
        <h2 class="witness-list__title subtitle">
          Témoins
          <a v-if="editable" class="tag" href="#" @click="openNewWitnessEdit">
            <icon-add/>
          </a>
        </h2>
 
      </header>
     
      <div class="witness-list__content panel-block " style="display: inline-block; width: 100%">
        <witness-item
            v-for="witness, index in list"
            :editable="editable"
            :can-be-removed="list.length > 1"
            :list-index="index"
            :list-length="list.length"
            :witness="witness"
            :edit-action="openWitnessEdit"
            :reorder-action="reorderWitness"
            :delete-action="removeWitness"
            :key="index"
        />
        <error-message :error="error"/>

      </div>
    </div>
   
    <witness-form
            v-if="editMode === 'new' || editMode === 'edit'"
            :title="editMode === 'new' ? 'Nouveau témoin' : 'Éditer le témoin'"
            :witness="selectedWitness"
            :witnessId="selectedWitnessId"
            :submit="editMode === 'new' ? addWitness : updateWitness"
            :cancel="closeWitnessEdit"
    />
  </section>
</template>

<script>
  import WitnessForm from '../forms/WitnessForm';
  import LaunchButton from '../forms/LaunchButton';
  import ErrorMessage from '../ui/ErrorMessage';
  import IconAdd from '../ui/icons/IconAdd';
  import WitnessItem from './witnesses/WitnessItem';

  export default {
    name: 'DocumentWitnesses',
    components: {WitnessItem, ErrorMessage, LaunchButton, WitnessForm, IconAdd},
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
      	console.log("update witness", witness);
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
            console.error('error', error)
          })
      },
      removeWitness (witness) {
        this.removeError()
        this.$store.dispatch('document/removeWitness', witness)
          .then( response => {
            this.closeWitnessEdit()
          })
          .catch(error => {
            console.error('error', error)
          })
      },
      reorderWitness (witness, dir) {
        this.$store.dispatch('document/reorderWitnesses', { witness, dir })

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
