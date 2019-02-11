import Vue from 'vue';

const TextFieldMixins = {

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
      Vue.nextTick(()=>this.$refs.input.focus())
    },
    exitEditMode (preventEmit = false) {
      if (!this.editMode) return;
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
  },
  computed: {
    unknownClass () {
      return { 'field-text--unknown': !this.value }
    }
  }

}

export default TextFieldMixins