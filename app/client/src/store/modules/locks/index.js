import http_with_csrf_token from '../../../modules/http-common';
import {getUser} from "../../../modules/change-helpers";
import Vue from "vue";

const state = {
  fullLocks: [],
  links: [],

  currentLock: null,
  lockOwner: {}
};


function addUserToData(data, included) {
  let dataWithUsers = [];
  for(let _d of data) {
    dataWithUsers.push({
      data: _d,
      user: getUser(_d.relationships.user.data.id, included)
    });
  }
  return dataWithUsers;
}

const mutations = {
  UPDATE_FULL_LOCKS (state, {locks, included, links}) {
    console.log("UPDATE_FULL_LOCKS", locks, included);
    state.fullLocks = addUserToData(locks, included);
    state.links = links;
  },

  SAVE_LOCK(state, lock) {
    state.currentLock = lock;
  },

  REMOVE_LOCK (state) {
    state.currentLock = null;
  },

  FETCH_LOCK_OWNER(state, {docId, user}) {
    console.log("FETCH_LOCK_OWNER", docId, user);
    Vue.set(state.lockOwner, docId, user);
  },

  RESET_LOCK_OWNER(state, {docId}) {
    console.log("RESET_LOCK_OWNER", docId);
    Vue.set(state.lockOwner, docId, null);
  }
};

const actions = {
  fetchFullLocks ({ commit }, {pageId, pageSize, filters}) {
    const http = http_with_csrf_token();
    return http.get(`locks?include=user&sort=-expiration-date&page[size]=${pageSize}&page[number]=${pageId}${filters ? '&'+filters : ''}`).then( response => {
      commit('UPDATE_FULL_LOCKS', {
        locks: response.data.data,
        included: response.data.included,
        links:response.data.links
      });
    });
  },

  fetchLockOwner({commit}, {docId, lockId}) {
    const http = http_with_csrf_token();
    return http.get(`/locks/${lockId}/user`).then(response => {
      commit('FETCH_LOCK_OWNER', {docId: docId, user: response.data.data});
    });
  },

  saveLock({commit}, lock) {
    const http = http_with_csrf_token();
    return http.post(`/locks`, {data: lock}).then(response => {
      commit('SAVE_LOCK', response.data.data);
    });
  },

  removeLock({commit}, lock) {
    const http = http_with_csrf_token();
    return http.delete(`locks/${lock.id}`, {data : {data: [{id: lock.id, type: 'lock'}]}}).then(response => {
      commit('REMOVE_LOCK');
      commit('RESET_LOCK_OWNER', {docId: lock['object-id']});
    });
  }
};

const getters = {


};

const locksModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default locksModule;
