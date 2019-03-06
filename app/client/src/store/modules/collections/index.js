import {http} from '../../../modules/http-common';
import Vue from "vue";
import {getIncludedRelation} from "../../../modules/document-helpers";

const state = {

  collectionsSearchResults: [],
  collectionsWithParents: {},

  allCollectionsWithParents: [],
  fullHierarchy: []

};

function buildTree(collections, parent, depth) {
  return collections.filter(c => c.parents.length === depth).map(c => {
    const children = buildTree(collections, c, depth + 1).filter(child => c.id === child.parents[0].id);
    if (children.length === 0)
      return c;
    else
      return {
        ...c,
        children: children
      }
  });
}

const mutations = {

  RESET(state) {
    state.collectionsWithParents = {};
  },
  FETCH_ONE(state, data) {
    Vue.set(state.collectionsWithParents, data.collection.id, {...data.collection, parents: data.parents});
  },
  FETCH_ALL(state, {data, included}) {

    const collections = data.map( c => {
      return {
        id: c.id,
        title: c.attributes.title,
        description: c.attributes.description,
        //documents: getIncludedRelation(c, included, "documents"),
        parents: getIncludedRelation(c, included, "parents")
      }
    });

    // build full hierarchy tree
    state.allCollectionsWithParents = collections;
    state.fullHierarchy = [];
    state.fullHierarchy = buildTree(collections, null, 0);
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

  fetchAll({commit}) {
    http.get(`/collections?include=parents`).then(response => {
      commit('FETCH_ALL', {data: response.data.data, included: response.data.included})
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
