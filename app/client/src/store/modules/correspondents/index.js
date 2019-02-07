import {http} from '../../../modules/http-common';


const state = {

  correspondentsSearchResults: [],
  roles: []

};

const mutations = {

  UPDATE_ROLES (state, payload) {
    state.roles = payload;
  },
  SEARCH_RESULTS (state, payload) {
    state.correspondentsSearchResults = payload;
  },

};

const actions = {

  search ({ commit }, what) {
    console.log('correspondents search', what)
    commit('SEARCH_RESULTS', [])

    http.get(`/search?query=*${what}*&index=lettres__${process.env.NODE_ENV}__correspondent&without-relationships`)
      .then( response => {
        const correspondents = response.data.data.map(inst => { return { id: inst.id, ...inst.attributes}});
        commit('SEARCH_RESULTS', correspondents)
      });
  },
  fetchRoles () {
    http.get(`/correspondents-roles?without-relationships`).then( response => {
      const roles = {
        id: response.data.data.id,
        ...response.data.data.attributes,
      };
      commit('UPDATE_ROLES', roles)
    });
  }

};

const getters = {



};

const correspondentsModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}

export default correspondentsModule;
