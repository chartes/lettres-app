import http_with_csrf_token from '../../../modules/http-common';
import {getUser} from "../../../modules/change-helpers";

const state = {
  //documentChangelog: [],
  //userChangelog: [],
  fullChangelog: []
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

function addUserDataToChanges(changes, included) {
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
  /*
  UPDATE_DOCUMENT_CHANGELOG (state, {changes, included}) {
    console.log("UPDATE_DOCUMENT_CHANGELOG", changes);
    // perform the state mutation
    state.documentChangelog = addUserDataToChanges(changes, included);
  },

  UPDATE_USER_CHANGELOG (state, {changes, included}) {
    console.log("UPDATE_USER_CHANGELOG", changes, included);
    // perform the state mutation
    state.userChangelog = addUserDataToChanges(changes, included);
  },
  */
  UPDATE_FULL_CHANGELOG (state, {changes, included}) {
    console.log("UPDATE_FULL_CHANGELOG", changes, included);
    // perform the state mutation
    state.fullChangelog = addUserDataToChanges(changes, included);
  }
};

const actions = {
  /*
  fetchDocumentChangelog ({ commit }, {docId}) {
    const http = http_with_csrf_token();
    return http.get(`documents/${docId}/changes?include=user`).then( response => {
      commit('UPDATE_DOCUMENT_CHANGELOG', {changes: response.data.data, included: response.data.included});
    });
  },
  fetchUserChangelog ({ commit }, {user, filters}) {
    const http = http_with_csrf_token();
    return http.get(`changes?include=user&filter[user_id]=${user.id}${filters ? '&'+filters : ''}`).then( response => {
      commit('UPDATE_USER_CHANGELOG', {changes: response.data.data, included: response.data.included});
    });
  },
  */
  fetchFullChangelog ({ commit }, filters) {
    const http = http_with_csrf_token();
    return http.get(`changes?include=user${filters ? '&'+filters : ''}`).then( response => {
      commit('UPDATE_FULL_CHANGELOG', {changes: response.data.data, included: response.data.included});
    });
  }
};

const getters = {


};

const changeModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default changeModule;
