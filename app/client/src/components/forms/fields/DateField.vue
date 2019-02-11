<template>
  <div class="field-date">
    <field-label :label="label"/>


    <div class="field field-date__field" v-if="editable && editMode" ref="hover">
      <div class="control">
        <input ref="input" class="field-date__input" type="text" v-model="value"
           @keyup="maskCheck"
           @keyup.enter="exitEditMode(false)"
           @blur="exitEditMode(false)"
           @keyup.esc="cancelInput"
           v-mask="{mask: '(9999)|(9999-99)|(9999-99-99)', placeholder: 'AAAA-MM-DD', greedy: false}"
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
        <span class="field-date__input field-date__input--fake" :class="fieldClasses" v-html="value || notSet"/>
        <icon-pen-edit class="field-date__icon" />
      </div>
    </div>

    <div v-else>
      <span :class="unknownClass">{{ value || notSet }}</span>
    </div>

  </div>
</template>

<script>
  import Vue from 'vue';
  import FieldLabel from './FieldLabel';
  import IconPenEdit from '../icons/IconPenEdit';
  import TextFieldMixins from './TextFieldMixins';
  export default {
    name: 'DateField',
    components: {IconPenEdit, FieldLabel},
    mixins: [TextFieldMixins],
    data() {
      return {
        isValid: true
      }
    },
    methods: {
      maskCheck: function (field){
          this.isValid = !this.value || field.target.inputmask.isComplete()
      }
    },
    computed: {

      fieldClasses () {
        return {
          ...this.unknownClass,
          'field-text--invalid': !this.isValid
        }
      }
    }
  }
</script>

<style scoped>
  .invalid {
    color: #f00;
  }
</style>