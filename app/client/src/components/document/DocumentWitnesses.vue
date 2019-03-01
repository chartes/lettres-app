<template>
  <div class="witness-list">
    <header class="witness-list__header">
      <h2 class="witness-list__title subtitle">
        Témoins
        <a v-if="editable" class="tag" href="#" @click="openNewWitnessEdit">
          <icon-add/>
        </a>
      </h2>
    </header>
    <div class="witness-list__content">
      
      <ul class="witness-list__list">
        <li v-for="witness, index in list" class="witness-item">

          <div class="witness-item__content">
            <span class="witness-item__text" v-html="witness.content"></span>
            <span v-if="witness.status && witness.status.length > 0" class="tag">{{witness.status}}</span>
            <span v-if="witness.tradition && witness.tradition.length > 0" class="tag">{{witness.tradition}}</span>
            
            <a v-if="editable && list.length > 1" @click="reorderWitness(witness, 1)">
              <icon-arrow-down style="padding: 0"/>
            </a>
            <a v-if="editable && list.length > 1 && index > 0" @click="reorderWitness(witness, -1)">
              <icon-arrow-down style="padding: 0" class="is-upside-down"/>
            </a>
            <a v-if="editable" @click="openWitnessEdit(witness)" class="witness-item__edit">
              <icon-pen-edit/>
            </a>
            <a v-if="editable" @click="removeWitness(witness)" class="witness-item__delete">
              <icon-bin/>
            </a>
          </div>
        </li>
      </ul>
      
      <error-message :error="error"/>
    </div>
    <witness-form
            v-if="editMode === 'new' || editMode === 'edit'"
            :title="editMode === 'new' ? 'Nouveau témoin' : 'Éditer le témoin'"
            :witness="selectedWitness"
            :witnessId="selectedWitnessId"
            :submit="editMode === 'new' ? addWitness : updateWitness"
            :cancel="closeWitnessEdit"
    />
  </div>
</template>

<script>
  import IconPenEdit from '../ui/icons/IconPenEdit';
  import IconBin from '../ui/icons/IconBin';
  import WitnessForm from '../forms/WitnessForm';
  import LaunchButton from '../forms/LaunchButton';
  import ErrorMessage from '../ui/ErrorMessage';
  import IconArrowDown from '../ui/icons/IconArrowDown';
  import IconAdd from '../ui/icons/IconAdd';
  import {mapState} from 'vuex';

  export default {
    name: 'DocumentWitnesses',
    components: {ErrorMessage, LaunchButton, WitnessForm, IconBin, IconPenEdit, IconArrowDown, IconAdd},
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
    computed: {
    },
    mounted() {

    } ,
    watch: {

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