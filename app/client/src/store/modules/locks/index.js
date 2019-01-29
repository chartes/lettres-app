import http_with_csrf_token from '../../../modules/http-common';
import {getUser} from "../../../modules/change-helpers";

const state = {
  documentLocks: [],
  userLocks: [],
  fullLocks: []
};

function cmp_dates(d1, d2) {
  if (d1 < d2) {
    return -1;
  }
  if (d1 > d2) {
    return 1;
  }
  return 0;
}

function addUserDataToLocks(changes, included) {
  // sort changes by event-date
  changes.sort((c1, c2) => {return cmp_dates(c2.attributes['event-date'], c1.attributes['event-date'])});

  let changelog = [];
  for(let _chg of changes) {
    changelog.push({
      data: _chg,
      user: getUser(_chg.relationships.user.data.id, included)
    });
  }
  return changelog;
}

const mutations = {
  UPDATE_DOCUMENT_LOCKS (state, {changes, included}) {
    console.log("UPDATE_DOCUMENT_LOCKS", changes);
    // perform the state mutation
    state.documentLocks = addUserDataToLocks(changes, included);
  },

  UPDATE_USER_LOCKS (state, {changes, included}) {
    console.log("UPDATE_USER_LOCKS", changes, included);
    // perform the state mutation
    state.userLocks = addUserDataToLocks(changes, included);
  },

  UPDATE_FULL_LOCKS (state, {changes, included}) {
    console.log("UPDATE_FULL_LOCKS", changes, included);
    // perform the state mutation
    state.fullLocks = addUserDataToLocks(changes, included);
  }
};

const actions = {

  fetchDocumentLocks ({ commit }, {docId}) {
    const http = http_with_csrf_token();
    return http.get(`documents/${docId}/locks?include=user`).then( response => {
      commit('UPDATE_DOCUMENT_LOCKS', {changes: response.data.data, included: response.data.included});
    });
  },
  fetchUserLocks ({ commit }, {user}) {
    const http = http_with_csrf_token();
    return http.get(`users/${user.id}/locks?include=user`).then( response => {
      commit('UPDATE_USER_LOCKS', {changes: response.data.data, included: response.data.included});
    });
  },
  fetchFullLocks ({ commit }) {
    const http = http_with_csrf_token();
    return http.get(`locks?include=user`).then( response => {
      commit('UPDATE_FULL_LOCKS', {changes: response.data.data, included: response.data.included});
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
