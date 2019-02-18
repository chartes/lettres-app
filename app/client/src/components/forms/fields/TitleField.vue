<template>
  <div class="field-title">
    <field-label :label="label"/>

    <div class="field" v-if="editable && editMode" ref="hover">
      <div class="control">
        <input ref="input" class="input" type="text" v-model="value"
           :tabindex="tabulationIndex"
           @change="inputChanged"
           @keyup.enter="exitEditMode(false)"
           @blur="exitEditMode(false)"
           @keyup.esc="cancelInput"
        />
      </div>
    </div>

    <div v-else-if="editable && !editMode"  class="field" ref="hover"
         :tabindex="tabulationIndex"
         @click="enterEditMode"
         @focus="enterEditMode"
         @mouseover="overField"
         @mouseout="outField">
      <div class="control">
        <span class="input fake-input" v-html="value || notSet"/>
        <icon-pen-edit />
      </div>
    </div>

    <div v-else>
      <span :class="{ unknown: !value}">{{ value || notSet }}</span>
    </div>

  </div>
</template>

<script>
  import Vue from 'vue';
  import FieldLabel from './FieldLabel';
  import IconPenEdit from '../../ui/icons/IconPenEdit';
  export default {
    name: 'TitleField',
    components: {IconPenEdit, FieldLabel},
    props: {
      name: { type: String, required: true },
      label: { type: String, required: true },
      notSet: { type: String, default: '&mdash;' },
      editable: { type: Boolean, default: false },
      tabulationIndex: { type: Number },
      initialValue: null,
    },
    data() {
      return {
        editMode: false,
        displayEditButton: false,
        value: null,
        enterEditModeValue: null,
        valueChanged: false
      }
    },
    mounted () {
      this.value = this.$props.initialValue
    },
    beforeDestroy () {
    },
    methods: {
      enterEditMode () {
        this.editMode = true
        this.enterEditModeValue = this.value;
        Vue.nextTick(()=>this.$refs.input.focus())
      },
      exitEditMode (preventEmit = false) {
        this.editMode = false
        if (this.valueChanged && !preventEmit) {
          console.log(" => emit", this.name, this.initialValue, '=>', this.value)
          this.$emit('changed', { value: this.value, name: this.name, oldValue: this.initialValue })
        }
        this.valueChanged = false
      },
      overField () {
        this.displayEditButton = true
      },
      outField () {
        this.displayEditButton = false
      },
      inputChanged () {
        this.valueChanged = true
      },
      cancelInput () {
        this.value = this.enterEditModeValue
        this.exitEditMode(true)
      }
    }
  }
</script>

<style scoped>
  .input {
    border-width: 0 0 1px 0;
    box-shadow: none;
    padding-left: 0;
    border-radius: 0;
  }
  .fake-input {
    padding-right: 44px;
  }

  .unknown {
    color: grey;
  }
  .field {
    outline: none;
  }
</style>