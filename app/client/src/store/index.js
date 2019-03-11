import Vue from 'vue';
import Vuex from 'vuex';

import collections from './modules/collections';
import persons from './modules/persons';
import placenames from './modules/placenames';
import document from './modules/document';
import institutions from './modules/institutions';
import languages from './modules/languages';
import user from './modules/user';
import changelog from './modules/changelog';
import locks from './modules/locks';
import witnesses from './modules/witnesses';
import bookmarks from './modules/bookmarks';
import notes from './modules/notes';

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
      collections,
      persons,
      placenames,
      document,
      institutions,
      languages,
      user,
      changelog,
      locks,
      witnesses,
      bookmarks,
      notes,
    }
});
