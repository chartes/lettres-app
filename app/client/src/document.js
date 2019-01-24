import Vue from 'vue';
import App from './App.vue';

import store from './store'

new Vue({
  el: '#app',
  store,
  data: {
    documentId: undefined,
    userId: undefined,
  },
  beforeMount: function () {
    this.documentId = this.$el.dataset.documentId;
    this.userId = this.$el.dataset.userId;
  },
  render (h) {
    return h(App, { props: {
        doc_id: this.documentId,
        user_id: this.userId,
      }
    })
  }

});
