import Vue from 'vue';
import Vuex from 'vuex';

import document from './modules/document';
import user from './modules/user';
import changelog from './modules/changelog';

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
      document,
      user,
      changelog
    }
});
