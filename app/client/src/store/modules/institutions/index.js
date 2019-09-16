import http_with_csrf_token from '../../../modules/http-common';
import {http} from '../../../modules/http-common';
import wikidata from "../../../modules/ref-providers/wikidata";
import  Vue from "vue";

const state = {

  institutions: [],
  currentInstitution: null,
  institutionsSearchResults: [],
  newInstitution: null,
  
  institutionsWikidataSearchResults: null,

};

const mutations = {

  UPDATE (state, payload) {
    state.institutions = payload;
  },
  UPDATE_ONE (state, payload) {
    Vue.set(state, 'currentInstitution', payload)//state.currentInstitution = payload;
  },
  ADD_ONE (state, payload) {
    state.currentInstitution = payload;
  },

  SEARCH_RESULTS (state, payload) {
    payload = [{id: null, name: 'Non renseignée', ref: null}, ...payload];
    state.institutionsSearchResults = payload;
  },
  
  WIKIDATA_SEARCH_RESULTS(state, payload) {
    state.institutionsWikidataSearchResults = payload.map(p => {
      return {
        ...p,
        name: p.description ? `${p.name} — ${p.description}` : p.name
      }
    });
  },

};

const actions = {

  fetch ({ commit }) {
    commit('UPDATE', []);
    http.get(`/institutions?include=witnesses&without-relationships`).then( response => {
      const institutions = response.data.data.map(inst => {
        return {
          id: inst.id,
          witnesses: response.data.included.map(w => {return {id: w.id, ...w.attributes}}),
          ...inst.attributes,
        }
      });
      commit('UPDATE', institutions)
    });
  },
  fetchOne ({ commit }, id) {
    http.get(`/institution/${id}?include=witnesses&without-relationships`).then( response => {
      const institution = {
        id: response.data.data.id,
        witnesses: response.data.included.map(w => {
          return {id: w.id, ...w.attributes}
        }),
        ...response.data.data.attributes
      };
      console.log('institution fetchOne', institution)
      commit('UPDATE_ONE', institution)
    })
  },

  addOne ({commit}, institution) {
    const institutionData = {
      data: {
        type: 'institution',
        attributes: institution
      }
    };

    const http = http_with_csrf_token();
    return http.post(`/institutions`, institutionData).then( response => {
      const institution = { id: response.data.data.id, ...response.data.data.attributes };
      commit('ADD_ONE', institution)
      return institution
    })
  },
  search ({ commit }, what) {
    console.log('institution search', what)
    commit('SEARCH_RESULTS', [])
    http.get(`/search?query=*${what}*&index=lettres__${process.env.NODE_ENV}__institutions&without-relationships`).then( response => {
      const institutions = response.data.data.map(inst => { return { id: inst.id, ...inst.attributes}});
      commit('SEARCH_RESULTS', institutions)
    });
  },
  
  searchOnWikidata({commit}, what) {
    commit('WIKIDATA_SEARCH_RESULTS', []);
    wikidata.findOrganization(what).then((result) => {
      console.log(result);
      commit('WIKIDATA_SEARCH_RESULTS', result)
    });
  },

};

const getters = {


};

const institutionsModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}

export default institutionsModule;
