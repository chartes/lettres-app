<template>
    <div class="field field-multiselect">
        <field-label :label="label"/>
        <div class="field selected-list is-grouped is-grouped-multiline">
            <div class="control" v-for="item in items" :key="item[optionIdField]">
                <div class="tags has-addons selected-item are-medium">
                    <span class="tag">{{item[optionLabelField]}}</span>
                    <a v-if="editable" class="tag is-delete" @click.prevent="deleteItem(item[optionIdField])"></a>
                </div>
            </div>


        </div>
        <div class="multiselect-actions" v-if="editable && optionsList.length > ids.length">
            <a class="icon is-large add-item" href="#" @click.prevent="displayList">
                <span class="fa-stack ">
                <i class="fas fa-circle fa-stack-2x"></i>
                <i class="fas fa-plus fa-stack-1x "></i>
              </span>
            </a>
            <ul class="box" v-if="listVisible" v-click-outside="hideList">
                <li v-for="option in optionsNotSelected" :key="option[optionIdField]">
                    <a href="#" @click.prevent="addItem(option)" class="unselected-item" v-html="option[optionLabelField]"></a>
                </li>
            </ul>

        </div>
    </div>
</template>

<script>

  import ClickOutside from 'vue-click-outside';
  import FieldLabel from './FieldLabel';

  export default {
    name: "multiselect-field",
    components: {FieldLabel},
    props: {
      editable: {
        type: Boolean, default: false
      },
      label: {
        type: String
      },
      selectedItems: {
        type: Array,
      },
      optionLabelField: {
        type: String, default: 'label'
      },
      optionIdField: {
        type: String, default: 'id'
      },
      optionsList: {
        type: Array
      },
      onChange: {
        type: Function, required: true
      }
    },
    directives: {
      ClickOutside
    },
    data () {
      return { listVisible: false, items: [], ids: []}
    },
    mounted () {
      this.updateAllItems();
      console.log('multiselect-field', this.items, this.ids)
    },
    methods: {
      addItem (item) {
        this.items.push(item);
        this.ids.push(item[this.optionIdField]);
        this.hideList();
        this.onChange(this.items);
      },
      deleteItem (itemId) {
        this.items = this.items.filter (it => it[this.optionIdField] !== itemId);
        this.ids = this.items.map (it => it[this.optionIdField]);
        this.onChange(this.items);
      },
      updateAllItems () {
        if (!this.selectedItems) return;
        this.items = this.selectedItems.map (it => ({...it}));
        this.ids = this.items.map (it => it[this.optionIdField]);
      },
      displayList () {
        this.listVisible = true;
      },
      hideList () {
        this.listVisible = false;
      }
    },
    watch: {
      selectedItems () {
        this.updateAllItems();
      }
    },
    computed: {

      optionsNotSelected () {
        if (!this.optionsList) return [];
        return this.optionsList.filter(op => !this.ids.includes(op[this.optionIdField]));
      }
    }
  }
</script>

<style scoped>

</style>