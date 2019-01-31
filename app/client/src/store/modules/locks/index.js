import http_with_csrf_token from '../../../modules/http-common';
import {getUser} from "../../../modules/change-helpers";

const state = {
  fullLocks: [],
  links: []
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

function addUserToData(data, included) {
  // sort changes by event-date
  data.sort((c1, c2) => {return cmp_dates(c2.attributes['event-date'], c1.attributes['event-date'])});

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
  }
};

const actions = {
  fetchFullLocks ({ commit }, {pageId, pageSize, filters}) {
    const http = http_with_csrf_token();
    return http.get(`locks?include=user&page[size]=${pageSize}&page[number]=${pageId}${filters ? '&'+filters : ''}`).then( response => {
      commit('UPDATE_FULL_LOCKS', {
        locks: response.data.data,
        included: response.data.included,
        links:response.data.links
      });
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
