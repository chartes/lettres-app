import {http} from '../../../modules/http-common';
import Vue from "vue";

const state = {

  collectionsSearchResults: [],
  collectionsWithParents: {}

};

const mutations = {

  RESET(state) {
    state.collectionsWithParents = {};
  },
  FETCH_ONE(state, data) {
    Vue.set(state.collectionsWithParents, data.collection.id, {...data.collection, parents: data.parents});
  },

  SEARCH_RESULTS (state, payload) {
    state.collectionsSearchResults = payload;
  }

};

const actions = {

  reset({commit}) {
    commit('RESET');
  },

  fetchOne({ commit}, collectionId) {
    commit('SEARCH_RESULTS', [])
    http.get(`/collections/${collectionId}?include=parents&without-relationships`).then(response => {
      const parents = response.data.included.map(p => {
        return {id: p.id, ...p.attributes}
      });
      commit('FETCH_ONE', {collection: response.data.data, parents: parents})
    });
  },

  search ({ commit }, what) {
    console.log('collection search', what)
    commit('SEARCH_RESULTS', [])
    http.get(`/search?query=*${what}*&index=lettres__${process.env.NODE_ENV}__collections&include=parents&without-relationships`).then( response => {
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
