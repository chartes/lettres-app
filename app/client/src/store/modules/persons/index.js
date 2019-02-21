import {http} from '../../../modules/http-common';
import http_with_csrf_token from '../../../modules/http-common';
import wikidata from '../../../modules/ref-providers/wikidata';

const state = {

  personsSearchResults: null,
  personsWikidataSearchResults: null,
  roles: [],
  newPerson: null

};

const mutations = {

  UPDATE_ROLES (state, payload) {
    state.roles = payload;
  },
  SEARCH_RESULTS (state, payload) {
    state.personsSearchResults = payload;
  },
  WIKIDATA_SEARCH_RESULTS(state, payload) {
    state.personsWikidataSearchResults = payload.map(p => {
      return {
        ...p,
        label: p.description ? `${p.name} — ${p.description}` : p.name
      }
    });
  },
  ADD_ONE (state, payload) {
    state.personsSearchResults = payload;
  },

};

const actions = {

  search ({ commit }, what) {
    commit('SEARCH_RESULTS', [])
    http.get(`/search?query=*${what}*&index=lettres__${process.env.NODE_ENV}__person&without-relationships`)
      .then( response => {
        const persons = response.data.data.map(inst => { return { id: inst.id, ...inst.attributes}});
        commit('SEARCH_RESULTS', persons)
      });
  },
  searchOnWikidata({commit}, what) {
    commit('WIKIDATA_SEARCH_RESULTS', []);
    wikidata.findPlace(what).then((result) => {
      console.log(result);
      commit('WIKIDATA_SEARCH_RESULTS', result)
    });
  },
  fetchRoles ({ commit }) {
    console.log('fetchRoles')
    http.get(`/person-roles?without-relationships`).then( response => {
      const roles = response.data.data.map( r =>  {
        return { id: r.id, ...r.attributes, }
      })
      console.log('fetchRoles', response.data.data, roles)
      commit('UPDATE_ROLES', roles)
    });
  },

  addOne ({ commit }, person) {
    const http = http_with_csrf_token();
    const data = { type: 'person', attributes: { ...person }}
    return http.post(`persons`, {data})
      .then(response => {
        return response.data.data
      })
  },

  linkToDocument ({ commit, rootState }, {roleId, personId}) {
    const data = { data: {
        type: 'person-has-role',
        relationships: {
          document: {
            data: {
              id: rootState.document.document.id,
              type: 'document'
            }
          },
          'person-role': {
            data: {
              id: roleId,
              type: 'person-role'
            }
          },
          person: {
            data: {
              id: personId,
              type: 'person'
            }
          }
        }
      }}
    const http = http_with_csrf_token()
    return http.post(`/persons-having-roles`, data).then( response => {
        return response.data.data
      })
      .catch(error => console.log(error))
  },
  unlinkFromDocument ({ commit, rootState }, {relationId, personId, roleId}) {
    const http = http_with_csrf_token()
    return http.delete(`/persons-having-roles/${relationId}`)
      .then (() => this.dispatch('document/removePerson', relationId))
      .catch(error => console.log(error))
  },

};

const getters = {

  getRoleByLabel: state => label => {
    return state.roles.find(role => role.label === label)
  }

};

const personsModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
}

export default personsModule;
