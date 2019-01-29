<template>
  <div>

    <div class="tabs" :class="tabsStyle">
      <ul>
        <li v-for="tab in tabs" :class="{ 'is-active': tab.isActive }">
          <div v-if="tab.spacer" class="spacer"></div>
          <a v-else @click="selectTab(tab)">
            <i v-if="tab.iconClass" :class="`icon ${tab.iconClass}`"></i>
            {{ tab.name }}
          </a>
        </li>
      </ul>
    </div>

    <div class="tabs-content is-flex-fill">

      <slot></slot>

    </div>

  </div>
</template>

<script>

  import tab from './Tab.vue';

  export default {

    name: "tabs",

    props: {
      tabsStyle: {
        type: String,
        default: ''
      },
      onTabChange: {
        type: Function,
        default: null
      }
    },

    components: { tab },

    data() {
      return {
        tabs: null
      }
    },

    created () {
      this.tabs = this.$children;
    },

    methods: {
      selectTab (selectedTab) {
        let oldTab;
        this.tabs.forEach(t => {
          t.isActive = t.name === selectedTab.name;
          if (t.isActive) oldTab = t;
        });
        selectedTab.isActive = true;
        if (this.onTabChange) this.onTabChange(oldTab.name, selectedTab.name)
      }
    }

  }
</script>

<style scoped>
  .icon {
    margin-right: 12px;
  }
  li.is-active a {
    color: #962D3E;
  }
  .spacer {
    min-width: 100px;
  }
</style>
