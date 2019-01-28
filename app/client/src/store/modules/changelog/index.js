import {http, baseApiURL} from '../../../modules/http-common';
import {getChanges} from '../../../modules/document-helpers';
import store from "../../index";

const state = {
  changes: null
};

const mutations = {
  UPDATE_CHANGELOG (state, {changes}) {
    state.changes = changes;
  }
};

const actions = {

  fetchObjectChanges ({ commit }, objectType, objectId, userId) {
    console.log(`fetching changes for ${objectType} '${id}'`);
    return http.get(`user/${userId}/changes?without-relationships`).then( response => {

      let object_changes = response.data.filter(c => {
        return c.attributes["object-type"] === objectType && c.attributes["object-id"] === objectId
      });


      commit('UPDATE_CHANGELOG', object_changes);
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
