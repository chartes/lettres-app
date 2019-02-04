import {http} from '../../../modules/http-common';

const state = {

  institutions: [],
  currentInstitution: null,
  institutionsSearchResults: []

};

const mutations = {

  UPDATE (state, payload) {
    state.languages = payload;
  },
  UPDATE_ONE (state, payload) {
    state.currentInstitution = payload;
  },

  SEARCH_RESULTS (state, payload) {
    state.institutionsSearchResults = payload;
  }

};

const actions = {

  fetch ({ commit }) {
    http.get(`/institutions?without-relationships`).then( response => {
      const institutions = response.data.data.map(inst => { return { id: inst.id, ...inst.attributes}});
      commit('UPDATE', institutions)
    });
  },
  fetchOne ({ commit }, id) {
    console.log('institution fetchOne', id)
    http.get(`/institution/${id}?without-relationships`).then( response => {
      const institution = { id: response.data.data.id, ...response.data.data.attributes };
      console.log('institution fetchOne', institution)
      commit('UPDATE_ONE', institution)
    });
  },

  search ({ commit }, what) {
    console.log('institution search', what)
    commit('SEARCH_RESULTS', [])
    http.get(`/institutions?without-relationships`).then( response => {
      const institutions = response.data.data.map(inst => { return { id: inst.id, ...inst.attributes}});
      commit('SEARCH_RESULTS', institutions)
    });
  }

};

const getters = {



};

const institutionsModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}

export default institutionsModule;
