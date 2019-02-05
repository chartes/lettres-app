import Vue from 'vue';
import App from './App.vue';

import store from './store'

import { library } from '@fortawesome/fontawesome-svg-core';
import { faBookmark as fasBookmark } from '@fortawesome/free-solid-svg-icons';
import { faBookmark as farBookmark } from '@fortawesome/free-regular-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';


const VueInputMask = require('vue-inputmask').default;

Vue.use(VueInputMask);

library.add(fasBookmark, farBookmark);
Vue.component('font-awesome-icon', FontAwesomeIcon);


new Vue({
  el: '#app',
  store,
  data: {
    documentId: undefined
  },
  beforeMount: function () {
    this.documentId = this.$el.dataset.documentId;
  },
  render (h) {
    return h(App, { props: {
        doc_id: this.documentId
      }
    })
  }

});
