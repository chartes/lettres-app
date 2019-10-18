import {render} from '@vue/server-test-utils'
import {shallowMount, createLocalVue} from '@vue/test-utils'
import Vuex from 'vuex'

import DocumentAttributes from  '../../components/document/DocumentAttributes'

const localVue = createLocalVue()

localVue.use(Vuex)

describe('DocumentAttributes component', () => {
	
	let store
	let documentState
	let languagesState
	
	beforeEach(() => {
		
		documentState = {
				document: {
					title: "testTitle",
				},
				languages: [{label: 'French', id:'FR'}, {label: 'Italien', id:'ITA'}]
		}
		languagesState = {
				languages: [{label: 'French', id: 'FR'}, {label: 'Italien', id: 'ITA'}, {label: 'Latin', id: 'LAT'}]
		}
		
		store = new Vuex.Store({
			modules: {
				document: {
					namespaced: true,
					state: documentState
				},
				languages: {
					namespaced: true,
					state: languagesState
				}
			}
		})
	})
	
	it('dispatches "actionInput" when input event value is "input"', async () => {
		const wrapper = await render(DocumentAttributes, {
			store,
			localVue,
			propsData: {
				editable: true
			}
		})
		console.log(wrapper.html())
	})
	
});
