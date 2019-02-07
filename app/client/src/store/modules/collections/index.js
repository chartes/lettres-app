import {http} from '../../../modules/http-common';

const state = {

  collectionsSearchResults: [],

};

const mutations = {

  SEARCH_RESULTS (state, payload) {
    state.collectionsSearchResults = payload;
  }

};

const actions = {

  search ({ commit }, what) {
    console.log('collection search', what)
    commit('SEARCH_RESULTS', [])
    http.get(`/search?query=*${what}*&index=lettres__${process.env.NODE_ENV}__collection&without-relationships`).then( response => {
      const collections = response.data.data.map(coll => { return { id: coll.id, ...coll.attributes}});
      commit('SEARCH_RESULTS', collections)
    });
  }

};

const getters = {



};

const collectionsModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}

export default collectionsModule;
