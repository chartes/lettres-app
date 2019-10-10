<template>
  <div class="document-date__attributes" style="width: 100%">

    <header class="document-date__attributes--title mb-3">
      <span class="subtitle">Dates de temps</span>
    </header>

    <div class="columns is-multiline" v-if="editAttributes">
      <div class="column is-one-third">
        <date-field
                :tabulation-index="0"
                label="Date de rédaction"
                name="creation"
                not-set="Inconnue"
                :initial-value="document['creation']"
                :editable="editable"
                v-on:changed="fieldChanged"/>
      </div>
      <div class="column is-one-third">
        <date-field
                :tabulation-index="0"
                label="Date de rédaction (rédigée avant le ...)"
                name="creation-not-after"
                :initial-value="document['creation-not-after']"
                :editable="editable"
                v-on:changed="fieldChanged"/>
      </div>
      <div class="column is-one-third">
        <title-field-in-place
            label="Date de rédaction (étiquette) :"
            name="creation-label"
            :not-set="null"
            :initial-value="document['creation-label']"
            :editable="editable"
            :status="creationLabelStatus"
            specific-class="field-date__input"
            v-on:changed="fieldChanged"
        />
      </div>
    </div>
  </div>
</template>
<script>
  import { mapState } from 'vuex';
  import DateField from '../forms/fields/DateField';
  import DocumentPlacenames from "./DocumentPlacenames";
  import TitleFieldInPlace from "../forms/fields/TitleFieldInPlace";

  export default {
    name: 'DocumentAttributes',
    components: {DateField, TitleFieldInPlace, DocumentPlacenames },
    props: {
      editable: {
        type: Boolean,
        default: false
      },
      editAttributes: {
          type: Boolean, default: true
      }
    },
    data() {
      return {
	      creationLabelStatus: 'normal'
      }
    },
    methods: {
      fieldChanged (fieldProps) {
        const data = { id: this.document.id, attributes: {} };
        data.attributes[fieldProps.name] = fieldProps.value;
        this.$store.dispatch('document/save', data).then(response => {
        	
        	switch (fieldProps.name) {
            case 'creation-label':
	            this.creationLabelStatus = 'success';
	            setTimeout(() => {
		            this.creationLabelStatus = "normal"
	            }, 3000)
		          break;
	        }
       
        }).catch(e => {
	        switch (fieldProps.name) {
		        case 'creation-label':
			        this.creationLabelStatus = 'error';
		          break;
	        }
        });
      },

    },
    computed: {
      ...mapState('document', ['document']),
    }
  }
</script>

<style scoped>
</style>
