import Vue from 'vue';
import App from './App.vue';

import store from './store';
import Vuetify from "vuetify";


import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader

Vue.use(Vuetify, {
  iconfont: 'mdi',
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
    section: undefined,
    data : {}
  },
  beforeMount: function () {
    this.section = this.$el.dataset.section;
    this.data = JSON.parse(this.$el.dataset.data);
  },
  render(h) {
    return h(App, {
      props: {
        section: this.section,
        data: this.data,
      }
    })
  }

});
