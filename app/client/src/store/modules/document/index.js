import http from '../../../modules/http-common';
import {getCorrespondents, getInstitution, getLanguages, getTradition} from '../../../modules/document-helpers';

const state = {

  documentLoading: true,
  document: false,
  correspondents: [],
  documents: [],
  institution: false,
  tradition: false,
  languages: false,
  notes: false,
  images: false,

};

const mutations = {

  UPDATE_DOCUMENT (state, {data, included}) {
    console.log('UPDATE_DOCUMENT', data, included)
    state.document = { ...data.attributes, id: data.id};
    state.correspondents = getCorrespondents(included);
    state.institution = getInstitution(included);
    state.tradition = getTradition(included);
    state.languages = getLanguages(included);
  },
  UPDATE_ALL (state, payload) {
    state.documents = payload;
  },
  LOADING_STATUS (state, payload) {
    state.documentLoading = payload;
  },

};

const actions = {

  fetch ({ commit }, id) {

    commit('LOADING_STATUS', true)

    let incs = ['correspondents', 'roles', 'correspondents-having-roles', 'notes', 'institution', 'tradition', 'languages']

    return http.get(`documents/${id}?include=${incs.join(',')}`).then( response => {

      console.log('doc', response.data)
      commit('UPDATE_DOCUMENT', response.data)
      commit('LOADING_STATUS', false)

    })
  },
  save ({ commit, rootGetters }, data) {

    //const auth = rootGetters['user/authHeader'];

    //return http.put(`/documents`, { data: data }, auth)
    return http.put(`/documents`, { data: data })
      .then(response => {
        commit('UPDATE_DOCUMENT', response.data.data)
        resolve(response.data)
      })
      .catch(error => {
        console.error("error", error)
        reject(error)
      })
  },
  fetchAll ({ commit }, id) {
    return http.get(`/documents`)
      .then( (response) => {
      commit('UPDATE_DOCUMENT', response.data.data)
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
