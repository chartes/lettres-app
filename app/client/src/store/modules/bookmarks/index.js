import http_with_csrf_token from '../../../modules/http-common';

const state = {

  userBookmarks: {},
  links: []
};

const mutations = {
  UPDATE_USER_BOOKMARKS (state, {documents, links}) {
    console.log("UPDATE_USER_BOOKMARKS", documents);
    state.links = links;
    state.userBookmarks = documents.map(document => {
      return {
        id: document.id,
        type: document.type,
        attributes: {
          title: document.attributes["title"],
          'iiif-thumbnail-url' : document.attributes['iiif-thumbnail-url'],

        },
        //persons: persons,
        //witnesses: witnesses
      }
    });
  },
  UPDATE_USER_BOOKMARK (state, {docId, witnesses}) {
    console.log("UPDATE_USER_BOOKMARK", docId, witnesses);
    state.userBookmarks = state.userBookmarks.map(bookmark => {
        if (bookmark.id !== docId)
          return bookmark;
        bookmark.witnesses = witnesses;
        return bookmark;
    });
  }
};

const actions = {
  fetchUserBookmarks ({ commit }, {userId, pageId, pageSize, filters}) {
    const http = http_with_csrf_token();
    return http.get(`users/${userId}/bookmarks?without-relationships&page[size]=${pageSize}&page[number]=${pageId}${filters ? '&'+filters : ''}`).then( response => {
      response.data.data.sort((d1, d2) => {return d1.attributes["title"] - d2.attributes["title"]});
      return response.data;
    }).then (docs =>{
      commit('UPDATE_USER_BOOKMARKS', {
          documents: docs.data,
          links: docs.links
      });

      for (let doc of docs.data) {
        http.get(`documents/${doc.id}/witnesses?without-relationships`).then(witnesses => {
          commit('UPDATE_USER_BOOKMARK', {
            docId: doc.id,
            witnesses: witnesses.data.data,
            //persons: getPersons(docs.included)
          });
        });
      }

   });

  },

  deleteUserBookmark({ commit }, {userId, docId}) {
    const http = http_with_csrf_token();
    const dataToRemove = {
      data: [
        {id: docId, type: "document"}
      ]
    };
    return http.delete(`users/${userId}/relationships/bookmarks`, {data: dataToRemove});
  },

  postUserBookmark({ commit }, {userId, docId}) {
    const http = http_with_csrf_token();
    const dataToAdd = {
      data: [
        {id: docId, type: "document"}
      ]
    };
    return http.post(`users/${userId}/relationships/bookmarks`, dataToAdd);
  }
};

const getters = {


};

const bookmarksModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default bookmarksModule;
