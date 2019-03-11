import http_with_csrf_token from '../../../modules/http-common';
import {
  getPersons, getLanguages, getWitnesses,
  getNotes, getCollections, getCurrentLock,  getPlacenames
} from '../../../modules/document-helpers';
import Vue from "vue";

const TRANSLATION_MAPPING = {
  'creation' : 'Date de création',
  'creation-not-after' : 'Date de création (borne supérieure)',
  'creation-label' : 'Date de création (étiquette)',
  'is-published': 'Statut de publication',
  'argument': 'Argument',
  'transcription': 'Transcription',
  'title': 'Titre'
};

const state = {

  documentLoading: true,
  document: null,
  persons: [],
  placenames: [],
  witnesses: [],
  languages: [],
  collections: [],
  notes: [],

  documents: [],
  documentsPreview: {},
  links: [],
  totalCount: 0,
};

const mutations = {

  UPDATE_DOCUMENT (state, {data, included}) {
    console.log('UPDATE_DOCUMENT', data, included);
    state.document = { ...data.attributes, id: data.id};
    state.persons = getPersons(included);
    state.placenames = getPlacenames(included);
    state.collections = getCollections(included);
    state.languages = getLanguages(included);
    state.witnesses = getWitnesses(included);
    state.notes = getNotes(included);
    state.currentLock = getCurrentLock(included);
  },
  UPDATE_DOCUMENT_DATA (state, data) {
    console.log('UPDATE_DOCUMENT_DATA', data);
    state.document = { ...data.attributes, id: data.id};
  },
  UPDATE_DOCUMENT_PREVIEW (state, {data, included}) {
    console.log('UPDATE_DOCUMENT_PREVIEW');
    const newPreviewCard = {
      id: data.id,
      attributes: data.attributes,
      //persons: getPersons(included),
      //languages: getLanguages(included),
      collections: getCollections(included),
      currentLock: getCurrentLock(included)
    };
    Vue.set(state.documentsPreview, data.id, newPreviewCard);
  },
  UPDATE_ALL (state, payload) {
    console.log('UPDATE_ALL', payload.data);
    state.documents = payload.data;
    state.links = payload.links;
    state.totalCount = payload.meta["total-count"];
  },

  LOADING_STATUS (state, payload) {
    state.documentLoading = payload;
  },

  ADD_COLLECTION (state, payload) {
    const exists = state.collections.find(coll => coll.id === payload.id)
    if (exists) return;
    state.collections = [ ...state.collections, payload ]
  },

  UPDATE_NOTE (state, payload) {
    let no = state.notes.find(n => n.id === payload.id)
    const index = state.notes.indexOf(no)
    no = { ...payload }
    state.notes.splice(index, 1, no)
  },
  ADD_NOTE (state, payload) {
    const exists = state.notes.find(coll => coll.id === payload.id)
    if (exists) return;
    state.notes = [ ...state.notes, payload ]
  },

  ADD_WITNESS (state, payload) {
    state.witnesses = [ ...state.witnesses, payload ]
  },
  UPDATE_WITNESS (state, payload) {
    let wit = state.witnesses.find(w => w.id === payload.id)
    const index = state.witnesses.indexOf(wit)
    wit = { ...payload }
    state.witnesses.splice(index, 1, wit)
  },
  REMOVE_WITNESS (state, payload) {
    let wit = state.witnesses.find(w => w.id === payload.id)
    const index = state.witnesses.indexOf(wit)
    state.witnesses.splice(index, 1)
  },
  REORDER_WITNESSES (state, payload) {
    state.witnesses = [ ...payload ]
  },
  REMOVE_COLLECTION (state, payload) {
    state.collections = state.collections.filter(coll => coll.id !== payload.id)
  },
  REMOVE_PERSON (state, payload) {
    state.persons = state.persons.filter(corr => corr.relationId !== payload)
  },
  ADD_PERSON (state, payload) {
    state.persons = [ ...state.persons, payload ]
  },
  REMOVE_PLACENAME(state, payload) {
    state.placenames = state.placenames.filter(corr => corr.relationId !== payload)
  },
  ADD_PLACENAME(state, payload) {
    state.placenames = [...state.placenames, payload]
  },
};

const actions = {

  fetch ({ commit, rootState }, id) {
    commit('LOADING_STATUS', true);

    let incs = [
      'collections', 'notes',
      'persons-having-roles', 'persons', 'person-roles',
      'placenames-having-roles', 'placenames', 'placename-roles',
      'witnesses', 'languages', 'current-lock'
    ];

    this.dispatch('languages/fetch');

    const http = http_with_csrf_token();
    return http.get(`documents/${id}?include=${incs.join(',')}`).then( response => {
      commit('UPDATE_DOCUMENT', {
        data: response.data.data,
        included: response.data.included
      });
      commit('LOADING_STATUS', false)
    })
  },
  fetchPreview ({ commit }, id) {
    commit('LOADING_STATUS', true);
    const incs = [
      'collections', 'witnesses', 'current-lock'
    ];

    const http = http_with_csrf_token();
    return http.get(`documents/${id}?include=${incs.join(',')}&without-relationships`).then( response => {
      commit('UPDATE_DOCUMENT_PREVIEW', response.data);
      commit('LOADING_STATUS', false)
    })
  },
  fetchAll ({ commit }, {pageId, pageSize, filters}) {
    commit('LOADING_STATUS', true);
    const http = http_with_csrf_token();
    return http.get(`/documents?${filters}&page[size]=${pageSize}&page[number]=${pageId}&without-relationships`)
      .then( (response) => {
      commit('UPDATE_ALL', response.data);
      commit('LOADING_STATUS', false);
    })
  },
  fetchSearch ({ commit }, {pageId, pageSize, query}) {
    commit('LOADING_STATUS', true);

    const index = `lettres__${process.env.NODE_ENV}__documents`;
    const incs = ['collections', 'persons', 'persons-having-roles', 'roles', 'witnesses', 'languages'];
    const http = http_with_csrf_token();
    return http.get(`/search?query=${query}&index=${index}&include=${incs.join(',')}&without-relationships&page[size]=${pageSize}&page[number]=${pageId}`)
      .then( (response) => {
      commit('UPDATE_ALL', response.data);
      commit('LOADING_STATUS', false);
    })
  },

  save ({ commit, rootGetters, rootState, dispatch }, data) {
    const modifiedData = data.attributes || data.relationships;
    console.log('document/save', data)
    data.type = 'document'
    const http = http_with_csrf_token();
    return http.patch(`/documents/${data.id}`, { data })
      .then(response => {
        commit('UPDATE_DOCUMENT_DATA', response.data.data);
        return response.data.data
      })
      .then( doc => {
        let msg = null;
        if (doc.attributes) {

          msg = `Modification de ${Object.keys(modifiedData).map( 
              d => `'${TRANSLATION_MAPPING[d] ? TRANSLATION_MAPPING[d] : d}'`
          ).join(', ')}`;
        }
        return this.dispatch('changelog/trackChanges', {
          objId : doc.id,
          objType: 'document',
          userId: rootState.user.current_user.id,
          msg: msg
        });
      })
  },

  publish({commit, state}, docId) {
    return this.dispatch('document/save', {
        type: 'document',
        id: docId,
        attributes: {
          'is-published' : true
        }
    });
  },

  unpublish({commit, state}, docId) {
    return this.dispatch('document/save', {
        type: 'document',
        id: docId,
        attributes: {
          'is-published': false
        }
    });
  },

  addWitness ({commit, state}, witness) {
    witness.num = Math.max.apply(null, state.witnesses.map(w => w.num)) + 1;

    const witnessData = { ...witness };
    const institutionId = witness.institution ? witness.institution.id : null;
    delete(witnessData.id);
    delete(witnessData.institution);

    const relationships = {
      document: {
        data: {
          id: state.document.id,
          type: "document"
        }
      }
    }
    if (!!institutionId) {
      relationships.institution = {
        data: {
          id: institutionId,
          type: "institution"
        }
      }
    }
    const data = {
        type: "witness",
        attributes: witnessData,
        relationships
    };

    const http = http_with_csrf_token();
    return http.post(`/witnesses?without-relationships`, {data})
      .then(response => {
        console.log('response', response)
        witness.id = response.data.data.id;
        commit('ADD_WITNESS', witness);
      })
  },
  updateWitness ({commit, state}, witness) {

    const attributes = {...witness}
    const institutionId = witness.institution ? witness.institution.id : null;
    delete (attributes.id)
    delete (attributes.institution)
    delete (attributes['manifest-url'])
    const relationships = {
      document: {
        data: {
          id: state.document.id,
          type: "document"
        }
      }
    }
    if (!!institutionId) {
      relationships.institution = {
        data: {
          id: institutionId,
          type: "institution"
        }
      }
    }
    const data = {
        id : witness.id,
        type: "witness",
        attributes: attributes,
        relationships
    }
    const http = http_with_csrf_token();
    return http.patch(`witnesses/${witness.id}?without-relationships`, {data})
      .then(response => {
        console.log('response', response)
        commit('UPDATE_WITNESS', witness);
      })
  },
  removeWitness ({commit, state}, witness) {

    const data = { data: { id : witness.id, type: "witness" } }
    console.log('document store removeWitness', data, state.document.id)

    const http = http_with_csrf_token();
    return http.delete(`/witnesses/${witness.id}`, {data})
      .then(response => {
        console.log('response', response)
        commit('REMOVE_WITNESS', witness);
      })
  },
  reorderWitnesses ({commit, state}, { witness, dir }) {
    let witnesses = state.witnesses.map(w => {return {...w}})
    let found = witnesses.find(w => w.id === witness.id)
    let foundIndex = witnesses.indexOf(found)
    if ((foundIndex === 0 && dir === -1) || (foundIndex === (witnesses.length-1) && dir === 1)) return;
    witnesses.splice(foundIndex, 1)
    witnesses.splice(foundIndex + dir, 0, found)
    witnesses = witnesses.map((w, index) => { w.num = index+1; return w})
    const changed = witnesses.filter((w, index) => {
      console.log(state.witnesses[index].id, w.id, 'add', state.witnesses[index].id !== w.id)
      return state.witnesses[index].id !== w.id
    })

    const http = http_with_csrf_token();
    Promise.all(changed.map(w => {
      return http.patch(`/witnesses/${w.id}`, { data: {
        type: "witness",
        id: w.id,
        attributes: { num: w.num }
      }})
    })).then(() => {
      commit('REORDER_WITNESSES', witnesses)
    })

  },

  addPerson ({commit}, person) {
    commit('ADD_PERSON', person)
  },
  removePerson ({commit}, relationId) {
    commit('REMOVE_PERSON', relationId)
  },

  addPlacename({commit}, placename) {
    commit('ADD_PLACENAME', placename)
  },
  removePlacename({commit}, relationId) {
    commit('REMOVE_PLACENAME', relationId)
  },

  addCollection ({commit, state}, collection) {

    const data = { data: [ { id : collection.id, type: "collection" }, ] }

    const http = http_with_csrf_token();
    return http.post(`/documents/${state.document.id}/relationships/collections?without-relationships`, data)
      .then(response => {
        commit('ADD_COLLECTION', collection);
        return true
      })
  },
  removeCollection ({commit, state}, collection) {
    const data = { data: { id : collection.id, type: "collection" } }
    const http = http_with_csrf_token();
    return http.delete(`/documents/${state.document.id}/relationships/collections?without-relationships`, {data})
      .then(response => {
        commit('REMOVE_COLLECTION', collection);
        return true
      })
  },

  addNote ({commit, state}, note) {
    console.log('store updateNote', note)
    const data = {
      type: 'note',
      attributes: { content: note.content },
      relationships: {
        document: {
          data : [{ type: "document", id: state.document.id }]
        }
      }
    }
    const http = http_with_csrf_token();
    return http.post(`notes?without-relationships`, {data})
      .then(response => {
        console.log('response', note.content)
        note.id = response.data.data.id
        commit('ADD_NOTE', note);
        return note;
      })
  },
  updateNote ({commit, state}, note) {
    console.log('store updateNote', note)
    const data = {
      id: note.id,
      type: 'note',
      attributes: { content: note.content }
    }
    const http = http_with_csrf_token();
    return http.patch(`notes/${note.id}?without-relationships`, {data})
      .then(response => {
        console.log('response', note.content)
        commit('UPDATE_NOTE', note);
      })
  },
  removeNote ({commit, state}, noteId) {
    return noteId
  },


};

const getters = {

  documentSender (state) {
    return state.persons.filter( corr => {
      if (!corr.role) return false;
      return corr.role.label === 'sender'
    })
  },
  documentRecipients (state) {
    return state.persons.filter( corr => {
      if (!corr.role) return false;
      return corr.role.label === 'recipient'
    })
  },

  locationDateFrom(state) {
    console.warn(state.placenames);
    return state.placenames.filter(corr => {
      if (!corr.role) return false;
      console.warn(corr.role.label);
      return corr.role.label === 'location-date-from'
    })
  },
  locationDateTo(state) {
    return state.placenames.filter(corr => {
      if (!corr.role) return false;
      return corr.role.label === 'location-date-to'
    })
  },

};

const documentModule = {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};

export default documentModule;
