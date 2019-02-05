import Vue from 'vue';
import App from './IndexApp.vue';

import store from './store';

import { library } from '@fortawesome/fontawesome-svg-core';
import { faBookmark as fasBookmark } from '@fortawesome/free-solid-svg-icons';
import { faBookmark as farBookmark } from '@fortawesome/free-regular-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';


library.add(fasBookmark, farBookmark);
Vue.component('font-awesome-icon', FontAwesomeIcon);

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
