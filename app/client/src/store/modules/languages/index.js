import {http} from '../../../modules/http-common';

const state = {

  languages: [],

};

const mutations = {

  UPDATE (state, payload) {
    state.languages = payload;
  }

};

const actions = {

  fetch ({ commit }) {
    http.get(`/languages?without-relationships`).then( response => {
      const languages = response.data.data.map(lang => { return { id: lang.id, ...lang.attributes}});
      commit('UPDATE', languages)
    });
  }

};

const getters = {

};

const languagesModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}

export default languagesModule;
