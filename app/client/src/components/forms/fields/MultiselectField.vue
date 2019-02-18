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


            <div class="control field-multiselect__actions"
                 v-if="editable && optionsList.length > ids.length"
                 v-click-outside="hideList"
            >
                <a class="tag" href="#" @click.prevent="displayList">
                    <icon-add/>
                </a>
                <ul class="field-multiselect__options box" v-if="listVisible">
                    <li v-for="option in optionsNotSelected" :key="option[optionIdField]">
                        <a href="#" @click.prevent="addItem(option)" class="unselected-item" v-html="option[optionLabelField]"></a>
                    </li>
                </ul>

            </div>
        </div>
    </div>
</template>

<script>

  import ClickOutside from 'vue-click-outside';
  import FieldLabel from './FieldLabel';
  import IconAdd from '../../ui/icons/IconAdd';

  export default {
    name: "multiselect-field",
    components: {IconAdd, FieldLabel},
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
      return { listVisible: true, items: [], ids: []}
    },
    mounted () {
      this.updateAllItems();
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