import http_with_csrf_token from '../../../modules/http-common';

const state = {
  changes: null
};

const mutations = {
  UPDATE_CHANGELOG (state, changes) {
    console.log("UPDATE_CHANGELOG", changes);
    state.changes = changes;
  }
};

const actions = {

  fetchObjectChanges ({ commit }, {objectType, objectId, userId}) {
    console.log(`fetching changes for ${objectType} '${objectId}'`);
    const http = http_with_csrf_token();
    return http.get(`${objectType}/${objectId}/changes?include=user`).then( response => {
      let object_changes = response.data.data.filter(c => {
        console.warn(c.attributes["object-type"], c.attributes["object-id"]);
        return true;//c.attributes["object-type"] === objectType && c.attributes["object-id"] === objectId
      });
      console.log(object_changes);
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
