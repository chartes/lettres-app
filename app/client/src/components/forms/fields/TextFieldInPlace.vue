<template>
  <div class="field-title">
    <field-label v-if="!!label" :label="label"/>

    <div class="field field-text__field" v-if="editable && editMode" ref="hover">
      <div class="control">
        <rich-text-editor
                ref="input"
                :multiline="false"
                v-model="value"
                :formats="[['italic','superscript','note']]"
                :tabindex="tabulationIndex"
                @change="inputChanged"
                @on-keyup-enter="clickSave"
                @on-keyup-escape="cancelInput"
        >
          <button
                  class="button is-small"
                  :class="saveButtonClass"
                  :disabled="status === 'disabled'"
                  @click="clickSave"
          >
            <component :is="saveButtonIcon"/>
          </button>
        </rich-text-editor>
      </div>
    </div>

    <div v-else-if="editable && !editMode"  class="field" ref="hover"
         :tabindex="tabulationIndex"
         @click="enterEditMode"
         @mouseover="overField"
         @mouseout="outField">
      <div class="field-text__control control">
        <span class="field-text__input field-text__input--fake" :class="unknownClass" v-html="value || notSet"/>
        <component class="field-text__icon" :is="editButtonIcon"/>
      </div>
    </div>

    <div v-else>
      <span  :class="unknownClass" v-html="value || notSet"></span>
    </div>

  </div>
</template>

<script>
  import FieldLabel from './FieldLabel';
  import TextFieldMixins from './TextFieldMixins';
  import RichTextEditor from './RichTextEditor';
  import IconSave from '../../ui/icons/IconSave';
  import IconPenEdit from '../../ui/icons/IconPenEdit';
  import IconError from '../../ui/icons/IconError';
  import IconSuccess from '../../ui/icons/IconSuccess';
  export default {
    name: 'TextFieldInPlace',
    components: {IconSuccess, IconError, IconSave, RichTextEditor, IconPenEdit, FieldLabel},
    mixins: [TextFieldMixins],
    props: {
      status: {
        validator: function (value) {
          return ['normal', 'success', 'error', 'loading', 'disabled' ].indexOf(value) !== -1
        },
        default: 'normal'
      }
    },
    methods: {
      clickSave () {
        if (this.status === 'error' || this.status === 'success') return;
        this.$emit('changed', { value: this.value, name: this.name, oldValue: this.initialValue })
      },
    },
    computed: {
      saveButtonClass () {
        switch (this.status) {
          case 'normal':
          case 'disabled':
            return 'is-success'
            break
          case 'success':
            return 'is-success'
            break
          case 'error':
            return 'is-danger'
            break
          case 'loading':
            return 'is-loading'
        }
      },
      saveButtonIcon () {
        switch (this.status) {
          case 'normal':
          case 'loading':
          case 'disabled':
            return IconSave;
            break;
          case 'success':
            return IconSuccess;
            break;
          case 'error':
            return IconError;
            break;
        }
      },
    },
    watch: {
      initialValue (val, oldVal) {
        this.value = val
      },
      status (val) {
        if (val === 'success') {
          this.exitEditMode(true)
        }
      }
    }
  }
</script>

<style scoped>
</style>