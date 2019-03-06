import Vue from 'vue';
import App from './IndexApp.vue';

import store from './store';
import Vuetify from "vuetify";

/*
import '@fortawesome/fontawesome-free/css/all.css' // Ensure you are using css-loader
//import 'material-design-icons-iconfont/dist/material-design-icons.css'; // Ensure you are using css-loader

import {library} from '@fortawesome/fontawesome-svg-core'
//import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
//import {fas} from '@fortawesome/free-solid-svg-icons'
import {
 faBookmark as fasBookmark,
 faLock,
 faUnlock,
 faCheckCircle as fasCheckCircle
} from '@fortawesome/free-solid-svg-icons';
import {
  faBookmark as farBookmark,
  faCheckCircle as farCheckCircle
} from '@fortawesome/free-regular-svg-icons';

//Vue.component('font-awesome-icon', FontAwesomeIcon); // Register component globally
//library.add(fas); // Include needed icons.
//library.add(far); // Include needed icons.
library.add(fasBookmark, farBookmark, faLock, faUnlock);
library.add(fasCheckCircle, farCheckCircle);
*/

import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader

Vue.use(Vuetify, {
  iconfont: 'fa',
  icons: {
    // pagination
    'firststep': 'fas fa-step-backward',
    'laststep': 'fas fa-step-forward',
    'nextstep': 'fas fa-chevron-right',
    'previousstep': 'fas fa-chevron-left',

    //tag bar
    'active_check_circle': 'fas fa-check-circle',
    'inactive_check_circle': 'far fa-check-circle',

    'active_bookmark': 'fas fa-bookmark',
    'inactive_bookmark': 'far fa-bookmark',

    'lock': 'fas fa-lock',
    'unlock': 'fas fa-unlock',

    'show': 'fas fa-eye',
    'hide': 'fas fa-eye-slash',
  }
});

const VueInputMask = require('vue-inputmask').default;
Vue.use(VueInputMask);


new Vue({
  el: '#app',
  store,
  data: {
    documentId: undefined,
    searchedTerm: '',
    template: undefined,
  },
  beforeMount: function () {
    this.section = this.$el.dataset.section;
    this.template = this.$el.dataset.template;

    this.documentId = parseInt(this.$el.dataset.documentId);
    this.searchedTerm = this.$el.dataset.searchedTerm;
  },
  render(h) {
    return h(App, {
      props: {
        section: this.section,
        template: this.template,

        docId: this.documentId,
        searchedTerm: this.searchedTerm,
      }
    })
  }

});
