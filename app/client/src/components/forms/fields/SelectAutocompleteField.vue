<template>
  <div class="field field-select-autocomplete">
    <field-label :label="label" :add-colons="label.length !== 0"/>

    <div class="field-select-autocomplete__wrapper">

      <div class="control">
        <a class="field-select-autocomplete__value" @click.prevent="openSearchBox">
          {{ labelString(value) }}
        </a>
      </div>


      <div class="field-select-autocomplete__searchbox" v-show="isOpen">

        <div class="field-select-autocomplete__search">
          <span class="control" :class="{ 'is-loading': isLoading }">
            <input ref="searchInput"
                class="input is-search"
                placeholder="Rechercher"
                type="text"
                @input="onChange"
                v-model="search"
                @keydown.down="onArrowDown"
                @keydown.up="onArrowUp"
                @keydown.enter="onEnter"
                @keydown.capture.esc="closeSearchBox"
            />
            <slot name="inputActions"></slot>
          </span>

        </div>
  
        <div class="field-select-autocomplete__results">
          <ul class="field-select-autocomplete__items">
            <li class="loading" v-if="isLoading">
              <loading-indicator :active="true"/>
            </li>
            <li v-else v-for="(result, i) in results"
                :key="i"
                @click="setResult(result)"
                class="field-select-autocomplete__item"
                :class="{ 'is-active': i === arrowCounter }"
            >
              {{ labelString(result) }}
            </li>
          </ul>

        </div>

        <div class="field-select-autocomplete__footer" v-if="slotNotEmpty">
          <slot></slot>
        </div>
      </div>
      
      <slot name="outputActions"></slot>

    </div>

  </div>
</template>

<script>
  import Vue from 'vue';
  import FieldLabel from './FieldLabel';
  import LoadingIndicator from '../../ui/LoadingIndicator';
  export default {
    name: 'SelectAutocompleteField',
    components: {LoadingIndicator, FieldLabel},
    props: {
      value: {},
      label: { type: String, default: '' },
      items: {
        type: Array,
        required: false,
        default: () => [],
      },
      isAsync: {
        type: Boolean,
        required: false,
        default: false,
      },
      valueKey: {
        type: String,
        default: 'id'
      },
      labelKey: {
        type: String,
        default: 'label'
      },
      notSet: {
        type: String,
        default: 'non renseigné'
      }
    },

    data() {
      return {
        isOpen: false,
        results: [],
        search: '',
        isLoading: false,
        arrowCounter: 0,
      };
    },

    mounted() {
      document.addEventListener('click', this.handleClickOutside)
    },
    destroyed() {
      document.removeEventListener('click', this.handleClickOutside)
    },

    methods: {
      onChange() {

        this.loading = true
        this.$emit('search', this.search);

        if (this.isAsync) {
          this.isLoading = true;
        } else {
          this.filterResults();
          this.isOpen = true;
        }
      },

      filterResults() {
        this.results = this.items.filter((item) => {
          return item.toLowerCase().indexOf(this.search.toLowerCase()) > -1;
        });
      },
      setResult(result) {
        this.$emit('input', result);
        this.isOpen = false;
      },
      onArrowDown(evt) {
        this.arrowCounter = (this.arrowCounter + 1) % this.results.length;
      },
      onArrowUp() {
        this.arrowCounter = (this.arrowCounter + this.results.length - 1) % this.results.length;
      },
      onEnter() {
        this.setResult(this.results[this.arrowCounter]);
        this.closeSearchBox()
      },
      handleClickOutside(evt) {
        if (!this.$el.contains(evt.target)) {
          this.closeSearchBox()
        }
      },
      openSearchBox () {
        this.search = '';
        this.isOpen = true;
        Vue.nextTick(() => {
          this.$refs.searchInput.focus()
          console.log("hello")
        })
      },
      closeSearchBox () {
        this.isOpen = false;
        this.arrowCounter = -1;
      },
      labelString (val) {
        if (!val) return this.notSet
        return val[this.labelKey] || this.notSet
      },
    },
    watch: {
      items: function (val, oldValue) {
        // actually compare the
        if (!!val || val.length !== oldValue.length) {
          this.results = val;
          this.isLoading = false;
          this.isOpen = true;
        }
      },
    },
    computed: {
      slotNotEmpty () {
        return !!this.$slots.default;
      },
    }
  };
</script>

<style>
</style>
