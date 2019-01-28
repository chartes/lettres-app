import Vue from 'vue';
import App from './IndexApp.vue';

import store from './store';

new Vue({
  el: '#app',
  store,
  data: {
  },
  beforeMount: function () {
  },
  render (h) {
    return h(App, {})
  }

});
