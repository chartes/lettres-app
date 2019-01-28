import Vue from 'vue';
import App from './App.vue';

import store from './store'

const VueInputMask = require('vue-inputmask').default

Vue.use(VueInputMask)

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
