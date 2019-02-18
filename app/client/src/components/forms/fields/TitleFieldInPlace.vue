<template>
  <div class="field-text">
    <field-label :label="label"/>

    <div class="field field-text__field" v-if="editable && editMode" ref="hover">
      <div class="control">
        <input ref="input" class="input field-text__input" type="text" v-model="value"
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
      <div class="field-text__control control">
        <span class="field-text__input field-text__input--fake" :class="unknownClass" v-html="value || notSet"/>
        <icon-pen-edit class="field-text__icon" />
      </div>
    </div>

    <div v-else>
      <span :class="unknownClass">{{ value || notSet }}</span>
    </div>

  </div>
</template>

<script>
  import FieldLabel from './FieldLabel';
  import IconPenEdit from '../../ui/icons/IconPenEdit';
  import TextFieldMixins from './TextFieldMixins';
  export default {
    name: 'TextFieldInPlace',
    components: {IconPenEdit, FieldLabel},
    mixins: [TextFieldMixins],
  }
</script>

<style scoped>
</style>