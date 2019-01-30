<template>
  <div class="field-date">
    <field-label :label="label"/>

    <div class="field" v-if="editable && editMode" ref="hover">
      <div class="control">
        <input ref="input" class="input" type="text" v-model="value"
           @change="inputChanged"
           @keyup.enter="exitEditMode(false)"
           @blur="exitEditMode(false)"
           @keyup.esc="cancelInput"
           placeholder="AAAA-MM-JJ"
           v-mask="{mask: '9999-99-99', placeholder: 'AAAA-MM-JJ'}"
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
        <span class="input fake-input" v-html="value || notSet"/></span>
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
  import IconPenEdit from '../IconPenEdit';
  export default {
    name: 'DateField',
    components: {IconPenEdit, FieldLabel},
    props: {
      name: { type: String, required: true },
      label: { type: String, required: true },
      notSet: { type: String, default: '&mdash;' },
      editable: { type: Boolean, default: false },
      initialValue: { type: String },
      tabulationIndex:  null,
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
          console.log(" => emit", this.value)
          this.$emit('changed', { value: this.value, name: this.name })
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
  .icon-pen-edit {
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: 1rem;
    height: 1rem;
    padding: .25rem;
    box-sizing: initial;
  }
  .unknown {
    color: grey;
  }

  .field {
    outline: none;
  }
</style>