<template>

  <li class="witness-item">

    <div class="witness-item__content">
      <span class="witness-item__text" v-html="me.content"></span>
      <span v-if="me.status && me.status.length > 0" class="tag">{{me.status}}</span>
      <span v-if="me.tradition && me.tradition.length > 0" class="tag">{{me.tradition}}</span>
      <span v-if="me.institution" class="tag">{{me.institution.name}}</span>

      <a v-if="editable && listLength > 1" @click="reorderAction(me, 1)">
        <icon-arrow-down style="padding: 0"/>
      </a>
      <a v-if="editable && listLength > 1 && listIndex > 0" @click="reorderAction(me, -1)">
        <icon-arrow-down style="padding: 0" class="is-upside-down"/>
      </a>
      <a v-if="editable" @click="editAction(me)" class="witness-item__edit">
        <icon-pen-edit/>
      </a>
      <a v-if="editable && canBeRemoved" @click="deleteAction(me)" class="witness-item__delete">
        <icon-bin/>
      </a>
    </div>
  </li>

</template>

<script>
  import IconPenEdit from '../../ui/icons/IconPenEdit'
  import IconBin from '../../ui/icons/IconBin'
  import IconArrowDown from '../../ui/icons/IconArrowDown'

  export default {
    name: 'WitnessItem',
    components: {IconArrowDown, IconBin, IconPenEdit},
    props: {
      editable: { type: Boolean, default: false },
      canBeRemoved: {type: Boolean, default: true},
      listIndex: { type: Number, default: 0 },
      listLength: { type: Number, default: 0 },
      witness: { type: Object, default: () => { return {} } },
      editAction: { type: Function },
      reorderAction: { type: Function },
      deleteAction: { type: Function }
    },
    data () {
      return {
        me: {...this.$props.witness}
      }
    },
    mounted () {
      this.$store.dispatch('document/fetchWitnessInstitution', this.me.id)
    },
    watch: {
      witness (newValue) {
        this.me = {...newValue}
      }
    }
  }
</script>

<style scoped>

</style>