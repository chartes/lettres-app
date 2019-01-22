import http from '../../../modules/http-common';
import {getCorrespondents, getLanguages, getWitnesses, getNotes, getCollections} from '../../../modules/document-helpers';

const state = {

  documentLoading: true,
  document: false,
  correspondents: [],
  witnesses: false,
  languages: false,
  collections: [],
  notes: false,

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
  },
  UPDATE_DOCUMENT_PREVIEW (state, {data, included}) {
    console.log('UPDATE_DOCUMENT_PREVIEW');
    const newPreviewCard = {
      id: data.id,
      attributes: data.attributes,
      correspondents: getCorrespondents(included),
      languages: getLanguages(included),
      collections: getCollections(included),
    };

    state.documentsPreview[data.id] = {
      ...state.documentsPreview[data.id],
      ...newPreviewCard
    };
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

};

const actions = {

  fetch ({ commit }, id) {
    commit('LOADING_STATUS', true);
    console.log(`fetching doc '${id}'`);
    const incs = ['collections', 'correspondents', 'roles', 'correspondents-having-roles', 'notes', 'witnesses', 'languages'];
    return http.get(`documents/${id}?include=${incs.join(',')}`).then( response => {
      commit('UPDATE_DOCUMENT', response.data);
      commit('LOADING_STATUS', false)
    })
  },
  save ({ commit, rootGetters }, data) {
    return http.put(`/documents`, { data: data })
      .then(response => {
        commit('UPDATE_DOCUMENT', response.data.data);
        resolve(response.data)
      })
      .catch(error => {
        console.error("error", error);
        reject(error)
      })
  },
  fetchPreview ({ commit }, id) {
    commit('LOADING_STATUS', true);
    console.log(`fetching doc preview '${id}'`);
    const incs = ['collections', 'correspondents', 'correspondents-having-roles', 'roles', 'witnesses', 'languages'];

    return http.get(`documents/${id}?include=${incs.join(',')}&without-relationships`).then( response => {
      commit('UPDATE_DOCUMENT_PREVIEW', response.data);
      commit('LOADING_STATUS', false)
    })
  },
  fetchAll ({ commit }, {pageId, pageSize}) {
    commit('LOADING_STATUS', true);
    return http.get(`/documents?page[size]=${pageSize}&page[number]=${pageId}`)
      .then( (response) => {
      commit('UPDATE_ALL', response.data);
      commit('LOADING_STATUS', false);
    })
  },
  fetchSearch ({ commit }, {pageId, pageSize, query}) {
    commit('LOADING_STATUS', true);

    console.warn("performing searches using the DEV index");
    const index = 'lettres__development__document';
    const incs = ['collections', 'correspondents', 'correspondents-having-roles', 'roles', 'witnesses', 'languages'];

    return http.get(`/search?query=${query}&index=${index}&include=${incs.join(',')}&without-relationships&page[size]=${pageSize}&page[number]=${pageId}`)
      .then( (response) => {
      commit('UPDATE_ALL', response.data);
      commit('LOADING_STATUS', false);
    })
  }

};

const getters = {


};

const documentModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default documentModule;
