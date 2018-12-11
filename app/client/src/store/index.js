import Vue from 'vue';
import Vuex from 'vuex';

import document from './modules/document'
import editors from './modules/editors'
import institutions from './modules/institutions'
import languages from './modules/languages'
import notes from './modules/notes'
import noteTypes from './modules/noteTypes'
import traditions from './modules/traditions'
import transcription from './modules/transcription'
import user from './modules/user'

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
      document,
      /*editors,
      institutions,
      languages,
      notes,
      noteTypes,
      traditions,
      transcription,
      user*/
    }
});
