import http_with_csrf_token from '../../../modules/http-common';
import {getUser} from "../../../modules/change-helpers";

const state = {
  changelog: {}
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

const mutations = {
  UPDATE_CHANGELOG (state, {objectType, changes, included}) {
    console.log("UPDATE_CHANGELOG", objectType, changes);

    // sort changes by event-date
    let changelog = [];
    changes.sort((c1, c2) => cmp_dates(c2.attributes['event-date'], c1.attributes['event-date']));

    // TODO: passer en fonctionnel avec map
    for(let _chg of changes) {
      changelog.push({
        data: _chg,
        user: getUser(_chg.relationships.user.data.id, included)
      });
    }

    // perform the state mutation
    state.changelog[objectType] = changelog;
  }
};

const actions = {

  fetchObjectChanges ({ commit }, {objectType, objectId}) {
    const http = http_with_csrf_token();
    return http.get(`${objectType}/${objectId}/changes?include=user`).then( response => {
      commit('UPDATE_CHANGELOG', {objectType: objectType, changes: response.data.data, included: response.data.included});
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
