import {http} from '../../../modules/http-common';
import http_with_csrf_token from '../../../modules/http-common';

const state = {

  correspondentsSearchResults: null,
  roles: [],
  newCorrespondent: null

};

const mutations = {

  UPDATE_ROLES (state, payload) {
    state.roles = payload;
  },
  SEARCH_RESULTS (state, payload) {
    state.correspondentsSearchResults = payload;
  },
  ADD_ONE (state, payload) {
    state.correspondentsSearchResults = payload;
  },

};

const actions = {

  search ({ commit }, what) {
    commit('SEARCH_RESULTS', [])
    http.get(`/search?query=*${what}*&index=lettres__${process.env.NODE_ENV}__correspondent&without-relationships`)
      .then( response => {
        const correspondents = response.data.data.map(inst => { return { id: inst.id, ...inst.attributes}});
        commit('SEARCH_RESULTS', correspondents)
      });
  },
  fetchRoles ({ commit }) {
    console.log('fetchRoles')
    http.get(`/correspondent-roles?without-relationships`).then( response => {
      const roles = response.data.data.map( r =>  {
        return { id: r.id, ...r.attributes, }
      })
      console.log('fetchRoles', response.data.data, roles)
      commit('UPDATE_ROLES', roles)
    });
  },

  addOne ({ commit }, correspondent) {
    const http = http_with_csrf_token();
    const data = { type: 'correspondent', attributes: { ...correspondent }}
    return http.post(`correspondents`, {data})
      .then(response => {
        return response.data.data
      })
  },

  linkToDocument ({ commit, rootState }, {roleId, correspondentId}) {
    const data = { data: {
        type: 'correspondent-has-role',
        relationships: {
          document: {
            data: {
              id: rootState.document.document.id,
              type: 'document'
            }
          },
          'correspondent-role': {
            data: {
              id: roleId,
              type: 'correspondent-role'
            }
          },
          correspondent: {
            data: {
              id: correspondentId,
              type: 'correspondent'
            }
          }
        }
      }}
    const http = http_with_csrf_token()
    return http.post(`/correspondents-having-roles`, data).then( response => {
        return response.data.data
      })
      .catch(error => console.log(error))
  },
  unlinkFromDocument ({ commit, rootState }, {relationId, correspondentId, roleId}) {
    const http = http_with_csrf_token()
    return http.delete(`/correspondents-having-roles/${relationId}`)
      .then (() => this.dispatch('document/removeCorrespondent', relationId))
      .catch(error => console.log(error))
  },

};

const getters = {

  getRoleByLabel: state => label => {
    return state.roles.find(role => role.label === label)
  }

};

const correspondentsModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}

export default correspondentsModule;
