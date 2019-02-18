import http_with_csrf_token from '../../../modules/http-common';
import {getCorrespondents, getLanguages, getWitnesses,
        getNotes, getCollections, getCurrentLock} from '../../../modules/document-helpers';
import Vue from "vue";

const state = {

  documentLoading: true,
  document: null,
  correspondents: [],
  witnesses: [],
  languages: [],
  collections: [],
  notes: [],

  documents: [],
  documentsPreview: {},
  links: [],
  totalCount: 0,
};

const mutations = {

  UPDATE_DOCUMENT (state, {data, included}) {
    console.log('UPDATE_DOCUMENT', data, included);
    state.document = { ...data.attributes, id: data.id};
    state.correspondents = getCorrespondents(included);
    state.collections = getCollections(included);
    state.languages = getLanguages(included);
    state.witnesses = getWitnesses(included);
    state.notes = getNotes(included);
    state.currentLock = getCurrentLock(included);
  },
  UPDATE_DOCUMENT_DATA (state, data) {
    console.log('UPDATE_DOCUMENT_DATA', data);
    state.document = { ...data.attributes, id: data.id};
  },
  UPDATE_DOCUMENT_PREVIEW (state, {data, included}) {
    console.log('UPDATE_DOCUMENT_PREVIEW');
    const newPreviewCard = {
      id: data.id,
      attributes: data.attributes,
      correspondents: getCorrespondents(included),
      languages: getLanguages(included),
      collections: getCollections(included),
      currentLock: getCurrentLock(included)
    };
    Vue.set(state.documentsPreview, data.id, newPreviewCard);
  },
  UPDATE_ALL (state, payload) {
    console.log('UPDATE_ALL');
    state.documents = payload.data;
    state.links = payload.links;
    state.totalCount = payload.meta["total-count"];
  },

  LOADING_STATUS (state, payload) {
    state.documentLoading = payload;
  },

  ADD_COLLECTION (state, payload) {
    const exists = state.collections.find(coll => coll.id === payload.id)
    if (exists) return;
    state.collections = [ ...state.collections, payload ]
  },

  ADD_WITNESS (state, payload) {
    state.witnesses = [ ...state.witnesses, payload ]
  },
  UPDATE_WITNESS (state, payload) {
    let wit = state.witnesses.find(w => w.id === payload.id)
    const index = state.witnesses.indexOf(wit)
    wit = { ...payload }
    state.witnesses.splice(index, 1, wit)
  },
  REMOVE_WITNESS (state, payload) {
    let wit = state.witnesses.find(w => w.id === payload.id)
    const index = state.witnesses.indexOf(wit)
    state.witnesses.splice(index, 1)
  },
  REMOVE_COLLECTION (state, payload) {
    state.collections = state.collections.filter(coll => coll.id !== payload.id)
  },
  REMOVE_CORRESPONDENT (state, payload) {
    state.correspondents = state.correspondents.filter(corr => corr.relationId !== payload)
  },
  ADD_CORRESPONDENT (state, payload) {
    state.correspondents = [ ...state.correspondents, payload ]
  },

};

const actions = {

  fetch ({ commit, rootState }, id) {
    commit('LOADING_STATUS', true);

    let incs = [
      'collections', 'correspondents', 'roles',
      'correspondents-having-roles', 'notes',
      'witnesses', 'languages', 'current-lock'
    ];

    this.dispatch('languages/fetch');

    const http = http_with_csrf_token();
    return http.get(`documents/${id}?include=${incs.join(',')}`).then( response => {
      commit('UPDATE_DOCUMENT', response.data);
      commit('LOADING_STATUS', false)
    })
  },
  fetchPreview ({ commit }, id) {
    commit('LOADING_STATUS', true);
    const incs = [
      'collections', 'correspondents', 'correspondents-having-roles',
      'roles', 'witnesses', 'languages', 'current-lock'
    ];

    const http = http_with_csrf_token();
    return http.get(`documents/${id}?include=${incs.join(',')}&without-relationships`).then( response => {
      commit('UPDATE_DOCUMENT_PREVIEW', response.data);
      commit('LOADING_STATUS', false)
    })
  },
  fetchAll ({ commit }, {pageId, pageSize}) {
    commit('LOADING_STATUS', true);
    const http = http_with_csrf_token();
    return http.get(`/documents?page[size]=${pageSize}&page[number]=${pageId}&without-relationships`)
      .then( (response) => {
      commit('UPDATE_ALL', response.data);
      commit('LOADING_STATUS', false);
    })
  },
  fetchSearch ({ commit }, {pageId, pageSize, query}) {
    commit('LOADING_STATUS', true);

    const index = `lettres__${process.env.NODE_ENV}__document`;
    const incs = ['collections', 'correspondents', 'correspondents-having-roles', 'roles', 'witnesses', 'languages'];
    const http = http_with_csrf_token();
    return http.get(`/search?query=${query}&index=${index}&include=${incs.join(',')}&without-relationships&page[size]=${pageSize}&page[number]=${pageId}`)
      .then( (response) => {
      commit('UPDATE_ALL', response.data);
      commit('LOADING_STATUS', false);
    })
  },

  save ({ commit, rootGetters, rootState, dispatch }, data) {
    const modifiedData = data;
    console.log('document/save', data)
    data.type = 'document'
    const http = http_with_csrf_token();
    return http.patch(`/documents/${data.id}`, { data })
      .then(response => {
        commit('UPDATE_DOCUMENT_DATA', response.data.data);
        //resolve(response.data)
        return response.data.data
      })
      .then( doc => {
        let desc = 'Modifications';
        if (doc.attributes) {
          desc = `Modification de ${Object.keys(modifiedData.attributes).join(', ')}`;
        }
        const data = {
          type: 'change',
          attributes: {
            'object-type': 'document',
            'object-id': doc.id,
            'description': desc,
          },
          relationships: {
            document: {
              data: {id: doc.id, type: 'document'}
            },
            user: {
              data: {id: rootState.user.current_user.id, type: 'user'}
            }
          }
        };
        return http.post(`changes`, { data }).then(response => {
          dispatch('changelog/fetchFullChangelog', {
            filters: `filter[object-id]=${doc.id}&filter[object-type]=document`
          }, { root: true });
        })
      })
      .catch(error => {
        console.error("error", error);
      })
  },

  addWitness ({commit, state}, witness) {
    const witnessData = { ...witness }
    const institutionId = witness.institution ? witness.institution.id : null;
    delete(witnessData.id)
    delete(witnessData.institution)
    const relationships = {
      document: {
        data: {
          id: state.document.id,
          type: "document"
        }
      }
    }
    if (!!institutionId) {
      relationships.institution = {
        data: {
          id: institutionId,
          type: "institution"
        }
      }
    }
    const data = {
        type: "witness",
        attributes: witnessData,
        relationships
    }

    const http = http_with_csrf_token();
    return http.post(`/witnesses?without-relationships`, {data})
      .then(response => {
        console.log('response', response)
        witness.id = response.data.data.id;
        commit('ADD_WITNESS', witness);
      })
  },
  updateWitness ({commit, state}, witness) {

    const attributes = {...witness}
    const institutionId = witness.institution ? witness.institution.id : null;
    delete (attributes.id)
    delete (attributes.institution)
    delete (attributes['manifest-url'])
    const relationships = {
      document: {
        data: {
          id: state.document.id,
          type: "document"
        }
      }
    }
    if (!!institutionId) {
      relationships.institution = {
        data: {
          id: institutionId,
          type: "institution"
        }
      }
    }
    const data = {
        id : witness.id,
        type: "witness",
        attributes: attributes,
        relationships
    }
    const http = http_with_csrf_token();
    return http.patch(`witnesses/${witness.id}?without-relationships`, {data})
      .then(response => {
        console.log('response', response)
        commit('UPDATE_WITNESS', witness);
      })
  },
  removeWitness ({commit, state}, witness) {

    const data = { data: { id : witness.id, type: "witness" } }
    console.log('document store removeWitness', data, state.document.id)

    const http = http_with_csrf_token();
    return http.delete(`/witnesses/${witness.id}`, {data})
      .then(response => {
        console.log('response', response)
        commit('REMOVE_WITNESS', witness);
      })
  },

  addCorrespondent ({commit}, correspondent) {
    commit('ADD_CORRESPONDENT', correspondent)
  },
  removeCorrespondent ({commit}, relationId) {
    commit('REMOVE_CORRESPONDENT', relationId)
  },

  addCollection ({commit, state}, collection) {

    const data = { data: [ { id : collection.id, type: "collection" }, ] }

    const http = http_with_csrf_token();
    return http.post(`/documents/${state.document.id}/relationships/collections?without-relationships`, data)
      .then(response => {
        commit('ADD_COLLECTION', collection);
        return true
      })
  },
  removeCollection ({commit, state}, collection) {
    const data = { data: { id : collection.id, type: "collection" } }
    const http = http_with_csrf_token();
    return http.delete(`/documents/${state.document.id}/relationships/collections?without-relationships`, {data})
      .then(response => {
        commit('REMOVE_COLLECTION', collection);
        return true
      })
  }


};

const getters = {

  documentSender (state) {
    return state.correspondents.filter( corr => {
      if (!corr.role) return false;
      return corr.role.label === 'sender'
    })
  },
  documentRecipients (state) {
    return state.correspondents.filter( corr => {
      if (!corr.role) return false;
      return corr.role.label !== 'sender'
    })
  },

};

const documentModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default documentModule;
