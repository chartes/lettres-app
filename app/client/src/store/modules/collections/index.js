import {http} from '../../../modules/http-common';
import {getIncludedRelation} from "../../../modules/document-helpers";

const state = {

  collectionsSearchResults: [],

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

function searchId(tree, id) {
    if (!tree){
      return null;
    }
    else if (tree.id === id) {
      return tree;
    }
    else {
      if (tree.children) {
        for (let child of tree.children) {
          const found = searchId(child, id);
          if (!!found) {
            return found;
          }
        }
      }
      return null;
    }
}

function countDocuments(collectionId) {
  return http.get(`/collections/${collectionId}/relationships/documents`).then(response => {
    return response.data.meta['total-count'];
  })
}

const mutations = {

  RESET(state) {
    state.collectionsWithParents = {};
  },

  FETCH_ALL(state, {data, included}) {
    let countPromises = [];
    let collections = data.map( c => {
      countPromises.push(countDocuments(c.id));
      return {
        id: c.id,
        title: c.attributes.title,
        description: c.attributes.description,
        //documentCount: count,
        //documents: getIncludedRelation(c, included, "documents"),
        parents: getIncludedRelation(c, included, "parents"),
      }
    });

    Promise.all(countPromises).then(counts =>{
      collections.map( c => {
        c.documentCount = counts.shift();
        c.titleWithCount = c.parents.length === 0 ? c.title : `${c.title} (${c.documentCount})`;
      });
      // build full hierarchy tree
      state.allCollectionsWithParents = collections;
      state.fullHierarchy = [];
      state.fullHierarchy = buildTree(collections, null, 0);
    });

  },
  SEARCH_RESULTS (state, payload) {
    state.collectionsSearchResults = payload;
  }

};

const actions = {

  reset({commit}) {
    commit('RESET');
  },

  fetchAll({commit}) {
    return http.get(`/collections?include=parents`).then(response => {
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
  searchWithinTree: (state) => (id) => {
    return !state.fullHierarchy ? null : searchId(state.fullHierarchy[0], id);
  }
};

const collectionsModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default collectionsModule;
