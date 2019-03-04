import http_with_csrf_token, {http} from '../../../modules/http-common';
import {baseApiURL} from '../../../modules/http-common';

import {getRoles, getUserRoles} from '../../../modules/user-helpers';

const state = {
  current_user: null,
  isUserLoaded: false,

  usersSearchResults: [],
};

const mutations = {
  UPDATE_USER (state, {data, included}) {
    console.log('UPDATE_USER', data);
    if (!data) {
      state.current_user = null;
    } else {
      const roles = getRoles(included);
      state.current_user = {
        id: data.id,
        ...data.attributes,
        roles: roles,
        isAdmin: roles.filter(r => r.name === "admin").length === 1
      };
    }
    state.isUserLoaded = true;
  },

  RESET_USER(state) {
    state.isUserLoaded = false;
  },

  SEARCH_RESULTS(state, {users, included}) {
    state.usersSearchResults = users.map( u => {
      const roles = getUserRoles(users, included, u);
      return  {
        id: u.id,
        ...u.attributes,
        roles: roles,
        isAdmin: roles.filter(r => r.name === "admin").length === 1
      }
    });
  }
};

const actions = {

  fetchCurrent ({ commit }) {
    commit('RESET_USER');
    const http = http_with_csrf_token();
    return http.get("token/refresh")
      .then(response => {
        if (response.data && response.data.user) {
          const user_api_url = response.data.user.replace(baseApiURL, '');
          return http.get(`${user_api_url}?include=roles&without-relationships`).then( response => {
            commit('UPDATE_USER', response.data);
          })
        } else {
          commit('UPDATE_USER', {data: null});
        }
      }).catch(error => {
        console.warn(error);
        commit('UPDATE_USER', {data: null});
      });
  },

  search({commit}, what) {
    console.log('user search', what);
    commit('SEARCH_RESULTS', {users: [], included: []});
    http.get(`/search?query=*${what}*&index=lettres__${process.env.NODE_ENV}__users&include=roles`).then(response => {
      commit('SEARCH_RESULTS', {users: response.data.data, included: response.data.included});
    });
  }
  /*
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
  */
};

const getters = {


};

const userModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default userModule;
