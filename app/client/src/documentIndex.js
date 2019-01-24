import Vue from 'vue';
import App from './IndexApp.vue';

import store from './store';

new Vue({
  el: '#app',
  store,
  data: {
    pageId: undefined,
    pageSize: undefined,
    userId: undefined,
  },
  beforeMount: function () {
    this.pageId = this.$el.dataset.pageId;
    this.pageSize = this.$el.dataset.pageSize;
    this.userId = this.$el.dataset.userId;
  },
  render (h) {
    return h(App, { props: {
        page_id: this.pageId,
        page_size: this.pageSize,
        user_id: this.userId
      }
    })
  }

});
