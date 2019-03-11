import Vue from 'vue';

import IconPenEdit from '../../ui/icons/IconPenEdit';
import IconSuccess from '../../ui/icons/IconSuccess';

const TextFieldMixins = {
  components: {IconSuccess, IconPenEdit},
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
  methods: {
    enterEditMode () {
      this.editMode = true
      this.enterEditModeValue = this.value;
      if (this.$refs.input && this.$refs.input.focus) Vue.nextTick(()=>this.$refs.input.focus())
    },
    exitEditMode (preventEmit = false) {
      if (!this.editMode) return;
      this.editMode = false

      if (this.valueChanged && !preventEmit) {
        this.$emit('changed', { value: this.value === '' ? null : this.value, name: this.name, oldValue: this.initialValue })
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
  },
  computed: {
    unknownClass () {
      return { 'field-text--unknown': !this.value }
    },
    editButtonIcon () {
      if (this.status === 'success') {
        return IconSuccess;
      }
      return IconPenEdit;
    }
  }

}

export default TextFieldMixins