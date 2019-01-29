import http_with_csrf_token from '../../../modules/http-common';
import {getCorrespondents, getLanguages, getWitnesses,
        getNotes, getCollections, getLocks, getChanges,} from '../../../modules/document-helpers';

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

  fetch ({ commit, rootState }, id) {
    commit('LOADING_STATUS', true);
    console.log(`fetching doc '${id}'`);
    let incs = ['collections', 'correspondents', 'roles',
                'correspondents-having-roles', 'notes',
                'witnesses', 'languages'];

    this.dispatch('languages/fetch')

    const http = http_with_csrf_token();
    return http.get(`documents/${id}?include=${incs.join(',')}`).then( response => {
      commit('UPDATE_DOCUMENT', response.data);
      commit('LOADING_STATUS', false)
    })
  },
  fetchPreview ({ commit }, id) {
    commit('LOADING_STATUS', true);
    //console.log(`fetching doc preview '${id}'`);
    const incs = ['collections', 'correspondents', 'correspondents-having-roles', 'roles', 'witnesses', 'languages', 'locks'];

    const http = http_with_csrf_token();
    return http.get(`documents/${id}?include=${incs.join(',')}&without-relationships`).then( response => {
      commit('UPDATE_DOCUMENT_PREVIEW', response.data);
      commit('LOADING_STATUS', false)
    })
  },
  fetchAll ({ commit }, {pageId, pageSize}) {
    commit('LOADING_STATUS', true);
    const http = http_with_csrf_token();
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
    const http = http_with_csrf_token();
    return http.get(`/search?query=${query}&index=${index}&include=${incs.join(',')}&without-relationships&page[size]=${pageSize}&page[number]=${pageId}`)
      .then( (response) => {
      commit('UPDATE_ALL', response.data);
      commit('LOADING_STATUS', false);
    })
  },

  save ({ commit, rootGetters }, data) {

    console.log('document/save', data)
    //const auth = rootGetters['user/authHeader'];
    //return http.put(`/documents`, { data: data }, auth)
    data.type = 'document'
    const http = http_with_csrf_token();
    return http.patch(`/documents/${data.id}`, { data })
      .then(response => {
        console.log('response', response)
        commit('UPDATE_DOCUMENT_DATA', response.data.data);
        //resolve(response.data)
      })
      .catch(error => {
        console.error("error", error);
        //reject(error)
      })
  },


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
