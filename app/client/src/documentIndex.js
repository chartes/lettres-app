import Vue from 'vue';
import App from './IndexApp.vue';

import store from './store'

new Vue({
  el: '#app',
  store,
  data: {
    pageId: undefined,
    authToken: undefined
  },
  beforeMount: function () {
    this.authToken = this.$el.dataset.pageId;
    this.authToken = this.$el.dataset.authToken;
  },
  render (h) {
    return h(App, { props: {
        auth_token: this.authToken,
        page_id: this.pageId,
      }
    })
  }

});
