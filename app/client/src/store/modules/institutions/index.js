import http_with_csrf_token from '../../../modules/http-common';
import {http} from '../../../modules/http-common';

const state = {

  institutions: [],
  currentInstitution: null,
  institutionsSearchResults: [],
  newInstitution: null,

};

const mutations = {

  UPDATE (state, payload) {
    state.institutions = payload;
  },
  UPDATE_ONE (state, payload) {
    state.currentInstitution = payload;
  },
  ADD_ONE (state, payload) {
    state.currentInstitution = payload;
  },

  SEARCH_RESULTS (state, payload) {
    state.institutionsSearchResults = payload;
  }

};

const actions = {

  fetch ({ commit }) {
    commit('UPDATE', []);
    http.get(`/institutions?include=witnesses&without-relationships`).then( response => {
      const institutions = response.data.data.map(inst => {
        return {
          id: inst.id,
          witnesses: response.data.included.map(w => {return {id: w.id, ...w.attributes}}),
          ...inst.attributes,
        }
      });
      commit('UPDATE', institutions)
    });
  },
  fetchOne ({ commit }, id) {
    console.log('institution fetchOne', id)
    http.get(`/institution/${id}?include=witnesses&without-relationships`).then( response => {
      const institution = {
        id: response.data.data.id,
        witnesses: response.data.included.map(w => {
          return {id: w.id, ...w.attributes}
        }),
        ...response.data.data.attributes
      };
      console.log('institution fetchOne', institution)
      commit('UPDATE_ONE', institution)
    })
  },

  addOne ({commit}, institution) {
    console.log('institution addOne', institution)

    const institutionData = {
      data: {
        type: 'institution',
        attributes: institution
      }
    }

    const http = http_with_csrf_token();
    return http.post(`/institutions`, institutionData).then( response => {
      const institution = { id: response.data.data.id, ...response.data.data.attributes };
      console.log('institution fetchOne', institution)
      commit('ADD_ONE', institution)
    })
  },

  search ({ commit }, what) {
    console.log('institution search', what)
    commit('SEARCH_RESULTS', [])
    http.get(`/search?query=*${what}*&index=lettres__${process.env.NODE_ENV}__institution&without-relationships`).then( response => {
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
