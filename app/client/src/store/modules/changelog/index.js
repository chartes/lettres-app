import http_with_csrf_token from '../../../modules/http-common';
import {getUser} from "../../../modules/change-helpers";

const state = {
  fullChangelog: [],
  links: [],
  pageId: null,
  pageSize: null
};

function addUserToData(data, included) {
  // sort changes by event-date
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
  UPDATE_FULL_CHANGELOG (state, {changes, included, links, pageId, pageSize}) {
    console.log("UPDATE_FULL_CHANGELOG", changes, included, pageId, pageSize);
    state.fullChangelog = addUserToData(changes, included);
    state.links = links;
    state.pageId = pageId;
    state.pageSize = pageSize;
  }
};

const actions = {
  fetchFullChangelog ({ commit }, {pageId, pageSize, filters}) {
    const http = http_with_csrf_token();
    if (pageId === undefined) {
      pageId = this.state.changelog.pageId;
    }
    if (pageSize === undefined) {
      pageSize = this.state.changelog.pageSize;
    }
    return http.get(`changes?include=user&sort=-event-date&page[size]=${pageSize}&page[number]=${pageId}${filters ? '&'+filters : ''}`)
      .then( response => {
        commit('UPDATE_FULL_CHANGELOG', {
          changes: response.data.data,
          included: response.data.included,
          links:response.data.links,
          pageId: pageId,
          pageSize: pageSize
        });
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
