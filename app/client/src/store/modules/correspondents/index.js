import {http} from '../../../modules/http-common';


const state = {

  correspondentsSearchResults: [],
  roles: []

};

const mutations = {

  UPDATE_ROLES (state, payload) {
    state.roles = payload;
  },
  SEARCH_RESULTS (state, payload) {
    state.correspondentsSearchResults = payload;
  },

};

const actions = {

  fetch () {


    setTimeout( () => {
      commit('UPDATE_ROLES', [
        { id: "1", label: "sender", description: "Expéditeur de la lettre" },
        { id: "2", label: "recipient", description: "Destinataire" },
        { id: "3", label: "sender", description: "Destinataire (copie)" },
      ])
    }, 2000)
    /*http.get(`/witnesses/${id}?include=institution`).then( response => {
      const roles = {
        id: response.data.data.id,
        ...response.data.data.attributes,
      };
      commit('UPDATE_ROLES', roles)
    });*/
  },
  search ({ commit }, what) {
    console.log('correspondents search', what)
    commit('SEARCH_RESULTS', [])
    setTimeout( () => {
      commit('SEARCH_RESULTS', [
        { id: "1", firstname:	"Catherine", lastname: "de Médicis", key: "Catherine de Médicis (reine de France ; 1519-1589)", ref: "https://data.bnf.fr/ark:/12148/cb123351707" },
        { id: "1", firstname:	"Jean-Luc", lastname: "Lahaye", key: "Lahaye, Jean-Luc", ref: "1" },
        { id: "1", firstname:	"Bernard", lastname: "Lavilliers", key: "Lavilliers, Bernard", ref: "2" },
      ])
    }, 2000)
    /*http.get(`/correspondents?without-relationships`).then( response => {
      const institutions = response.data.data.map(inst => { return { id: inst.id, ...inst.attributes}});
      commit('SEARCH_RESULTS', institutions)
    });*/
  },
  fetchRoles () {


    setTimeout( () => {
      commit('UPDATE_ROLES', [
        { id: "1", label: "sender", description: "Expéditeur de la lettre" },
        { id: "2", label: "recipient", description: "Destinataire" },
        { id: "3", label: "sender", description: "Destinataire (copie)" },
      ])
    }, 2000)
    /*http.get(`/witnesses/${id}?include=institution`).then( response => {
      const roles = {
        id: response.data.data.id,
        ...response.data.data.attributes,
      };
      commit('UPDATE_ROLES', roles)
    });*/
  }

};

const getters = {



};

const correspondentsModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}

export default correspondentsModule;
