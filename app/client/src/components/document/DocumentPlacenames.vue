<template>
  <section class="document-placenames mb-3" style="width: 100%">

    <div class="columns">
      
      <div class="document-placenames__senders column is-one-third">
        
        <h3 class="document-placenames__subtitle subtitle">
          Dates de lieu d'expédition
          <a v-if="editable" class="tag" href="#" @click="openAddPlacename('location-date-from')">
            <icon-add/>
          </a>
        </h3>
  
        <div v-if="locationDateFrom.length" v-for="c in locationDateFrom" :key="c.placename.id"
             class="tags has-addons are-medium document-placenames__senders-list mb-1">
                <span class="tag">
                     <a :href="c.placename.ref" target="_blank">
                      {{ !!c.placename.function ? `${c.placename.label}, ${c.placename.function}` : c.placename.label }}
                    </a>
                </span>
          <a v-if="editable" class="tag is-delete" @click.prevent="unlinkPlacenameFromDoc(c)"></a>
        </div>
        <div v-if="locationDateFrom.length === 0">
          <p class="placename-item"><em>Aucune date de lieu d'expédition renseignée</em></p>
        </div>
      
      </div>
      
      <div class="document-placenames__recipients column  is-one-third">
        <h3 class="document-placenames__subtitle subtitle">
          Dates de lieu de destination
          <a v-if="editable" class="tag" href="#" @click="openAddPlacename('location-date-to')">
            <icon-add/>
          </a>
        </h3>
  
        <div v-if="locationDateTo.length" v-for="c in locationDateTo" :key="c.placename.id"
             class="tags has-addons are-medium document-placenames__senders-list mb-1">
                <span class="tag">
                     <a :href="c.placename.ref" target="_blank">
                      {{ !!c.placename.function ? `${c.placename.label}, ${c.placename.function}` : c.placename.label }}
                    </a>
                </span>
          <a v-if="editable" class="tag is-delete" @click.prevent="unlinkPlacenameFromDoc(c)"></a>
        </div>
        <div v-if="locationDateTo.length === 0">
          <p class="placename-item"><em>Aucune date de lieu de destination renseignée</em></p>
        </div>
      </div>
      
      <placename-list-form
          v-if="placenamesForm && editable"
          title="Sélectionner un lieu"
          :submit="linkPlacenameToDoc"
          :cancel="closePlacenameChoice"
      />
    
    </div>
  </section>
</template>

<script>

    import {mapState, mapGetters} from 'vuex'
    import IconBin from '../ui/icons/IconBin';
    import PlacenameListForm from '../forms/PlacenameListForm';
    import LauchButton from '../forms/LaunchButton';
    import IconAdd from "../ui/icons/IconAdd";

    export default {
        name: 'DocumentPlacenames',
        components: {LauchButton, PlacenameListForm, IconBin, IconAdd},
        props: {
            editable: {
                type: Boolean,
                default: false
            },
        },
        data() {
            return {
                placenamesForm: null
            }
        },
        mounted() {
            this.$store.dispatch('placenames/fetchRoles')
        },
        methods: {
            openAddPlacename(role) {
                this.placenamesForm = role;
            },
            closePlacenameChoice() {
	            this.placenamesForm = null;
            },
            linkPlacenameToDoc(placename) {
	            const placenameId = placename.id
                const role = this.getRoleByLabel(this.placenamesForm)
                const roleId = role && role.id ? role.id : null;
                this.$store.dispatch('placenames/linkToDocument', {
                    placenameId,
                    roleId,
		                func: placename.function
                })
                    .then(placenameHasRole => {
                        
                            const corrData = {
                                placename,
                                placenameId,
                                relationId: placenameHasRole.id,
                                role,
                                roleId
                            };
                            this.$store.dispatch('document/addPlacename', corrData);
	                    this.closePlacenameChoice()
                    })
            },
            unlinkPlacenameFromDoc(placename) {
                const placenameId = placename.placenameId;
                const roleId = placename.roleId;
                this.$store.dispatch('placenames/unlinkFromDocument', {
                    relationId: placename.relationId,
                    placenameId,
                    roleId
                })
                    .then(response => {
                        this.closePlacenameChoice()
                    })
            }
        },
        computed: {
            ...mapState('document', ['placenames']),
            ...mapState('placenames', ['roles']),
            ...mapGetters('document', ['locationDateFrom', 'locationDateTo']),
            ...mapGetters('placenames', ['getRoleByLabel']),
        }
    }

</script>

<style>
</style>
