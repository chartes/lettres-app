import Vue from 'vue';
import App from './App.vue';

import store from './store'

import {library} from '@fortawesome/fontawesome-svg-core';
import {
  faBookmark as fasBookmark,
  faLock,
  faUnlock,
  faCheckCircle as fasCheckCricle
} from '@fortawesome/free-solid-svg-icons';
import {faBookmark as farBookmark, faCheckCircle as farCheckCricle} from '@fortawesome/free-regular-svg-icons';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';


library.add(fasBookmark, farBookmark, faLock, faUnlock);
library.add(fasCheckCricle, farCheckCricle);

Vue.component('font-awesome-icon', FontAwesomeIcon);

const VueInputMask = require('vue-inputmask').default;

Vue.use(VueInputMask);



new Vue({
  el: '#app',
  store,
  data: {
    documentId: undefined
  },
  beforeMount: function () {
    this.documentId = parseInt(this.$el.dataset.documentId);
  },
  render (h) {
    return h(App, { props: {
        doc_id: this.documentId
      }
    })
  }

});
