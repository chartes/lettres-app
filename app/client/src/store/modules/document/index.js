import http_with_csrf_token from '../../../modules/http-common';
import {getCorrespondents, getLanguages, getWitnesses,
        getNotes, getCollections, getCurrentLock} from '../../../modules/document-helpers';

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

  save ({ commit, rootGetters, rootState, dispatch }, data) {
    const modifiedData = data;
    console.log('document/save', data)
    data.type = 'document'
    const http = http_with_csrf_token();
    return http.patch(`/documents/${data.id}`, { data })
      .then(response => {
        console.log('response', response)
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
        //reject(error)
      })
  },


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
