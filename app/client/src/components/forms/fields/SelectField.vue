<template>
  <div class="field field-select">
      <p class="control">
          <field-label :label="label" />
          <span class="select" :class="isLoading">
                <select ref="field" @change="updateValue">
                    <option
                            v-if="hasOptions"
                            v-for="opt, index in options"
                            :key="opt.id"
                            :value="opt.id"
                            :selected="opt.id === value"
                            v-html="opt.label"
                    />
                </select>
            </span>
        </p>
    </div>
</template>

<script>
  import FieldLabel from './FieldLabel';
  export default {
    name: "field-select",
      components: {FieldLabel},
      props: {
      options: {
        type: Array
      },
      label: {
        type: String
      },
      value: {},
    },
    data() {
      return {
        //val: this.$props.value || this.$props.options[0].id
      }
    },
    methods: {
      updateValue () {
          this.$emit('input', this.$refs.field.value)
      },
    },
    computed: {
      hasOptions () {
        return this.options && this.options.length > 0;
      },
      isLoading () {
        return !(this.options && this.options.length > 0) ? 'is-loading': false;
      },
    }
  }
</script>