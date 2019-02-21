import {http} from '../../../modules/http-common';
import http_with_csrf_token from '../../../modules/http-common';
import wikidata from 'wikidata-entity-lookup';

const state = {

    placenamesSearchResults: null,
    placenamesWikidataSearchResults: null,
    roles: [],
    newPlacename: null

};

const mutations = {

    UPDATE_ROLES(state, payload) {
        state.roles = payload;
    },
    SEARCH_RESULTS(state, payload) {
        state.placenamesSearchResults = payload;
    },
    WIKIDATA_SEARCH_RESULTS(state, payload) {
        state.placenamesWikidataSearchResults = payload.map(p => {
            return {
                ...p,
                label: p.description ? `${p.name} — ${p.description}` : p.name
            }
        });
    },
    ADD_ONE(state, payload) {
        state.placenamesSearchResults = payload;
    },

};

const actions = {

    search({commit}, what) {
        commit('SEARCH_RESULTS', [])
        http.get(`/search?query=*${what}*&index=lettres__${process.env.NODE_ENV}__placename&without-relationships`)
            .then(response => {
                const placenames = response.data.data.map(inst => {
                    return {id: inst.id, ...inst.attributes}
                });
                commit('SEARCH_RESULTS', placenames)
            });
    },
    searchOnWikidata({commit}, what) {
        commit('WIKIDATA_SEARCH_RESULTS', []);
        wikidata.findPlace(what).then((result) => {
            console.log(result);
            commit('WIKIDATA_SEARCH_RESULTS', result)
        });
    },
    fetchRoles({commit}) {
        console.log('fetchRoles')
        http.get(`/placename-roles?without-relationships`).then(response => {
            const roles = response.data.data.map(r => {
                return {id: r.id, ...r.attributes,}
            })
            console.log('fetchRoles', response.data.data, roles)
            commit('UPDATE_ROLES', roles)
        });
    },

    addOne({commit}, placename) {
        const http = http_with_csrf_token();
        const data = {type: 'placename', attributes: {...placename}}
        return http.post(`placenames`, {data})
            .then(response => {
                return response.data.data
            })
    },

    linkToDocument({commit, rootState}, {roleId, placenameId}) {
        const data = {
            data: {
                type: 'placename-has-role',
                relationships: {
                    document: {
                        data: {
                            id: rootState.document.document.id,
                            type: 'document'
                        }
                    },
                    'placename-role': {
                        data: {
                            id: roleId,
                            type: 'placename-role'
                        }
                    },
                    placename: {
                        data: {
                            id: placenameId,
                            type: 'placename'
                        }
                    }
                }
            }
        }
        const http = http_with_csrf_token()
        return http.post(`/placenames-having-roles`, data).then(response => {
            return response.data.data
        })
            .catch(error => console.log(error))
    },
    unlinkFromDocument({commit, rootState}, {relationId, placenameId, roleId}) {
        const http = http_with_csrf_token()
        return http.delete(`/placenames-having-roles/${relationId}`)
            .then(() => this.dispatch('document/removePlacename', relationId))
            .catch(error => console.log(error))
    },

};

const getters = {

    getRoleByLabel: state => label => {
        return state.roles.find(role => role.label === label)
    }

};

const placenamesModule = {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
}

export default placenamesModule;
