import http from '../../../modules/http-common';
import {getCorrespondents, getInstitution, getLanguages, getNotes, getTradition, getCollections} from '../../../modules/document-helpers';

const state = {

  documentLoading: true,
  document: false,
  correspondents: [],
  institution: false,
  tradition: false,
  languages: false,
  collections: [],
  notes: false,
  images: false,

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
    state.institution = getInstitution(included);
    state.tradition = getTradition(included);
    state.languages = getLanguages(included);
    state.notes = getNotes(included);
  },
  UPDATE_DOCUMENT_PREVIEW (state, {data, included}) {
    console.log('UPDATE_DOCUMENT_PREVIEW');
    const newPreviewCard = {
      id: data.id,
      attributes: data.attributes,
      correspondents: getCorrespondents(included),
      institution: getInstitution(included),
      tradition: getTradition(included),
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
    let incs = ['collections', 'correspondents', 'roles', 'correspondents-having-roles', 'notes', 'institution', 'tradition', 'languages'];
    return http.get(`documents/${id}?include=${incs.join(',')}`).then( response => {
      commit('UPDATE_DOCUMENT', response.data);
      commit('LOADING_STATUS', false)
    })
  },
  save ({ commit, rootGetters }, data) {
    //const auth = rootGetters['user/authHeader'];
    //return http.put(`/documents`, { data: data }, auth)
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
    let incs = ['collections', 'correspondents', 'roles', 'correspondents-having-roles', 'institution', 'tradition', 'languages'];

    return http.get(`documents/${id}?include=${incs.join(',')}`).then( response => {
      commit('UPDATE_DOCUMENT_PREVIEW', response.data);
      commit('LOADING_STATUS', false)
    })
  },
  fetchAll ({ commit }, {pageId, pageSize}) {
    return http.get(`/documents?page[size]=${pageSize}&page[number]=${pageId}`)
      .then( (response) => {
      commit('UPDATE_ALL', response.data);
    })
  }

};

const getters = {

  manifestURL: state => {
    const manifest_url = `/lettres/api/1.0/documents/${state.document.id}/manifest`;
    return state.document && state.document.images &&  state.document.images.length > 0 ? manifest_url : null
  }

};

const documentModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}

export default documentModule;
