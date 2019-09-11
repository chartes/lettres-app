<template>
  <section class="document-persons  ">
    <header>
      Dates de lieu
    </header>
    <div class="columns">
      
      <div class="document-placenames__senders column">
        
        <h3 class="document-persons__subtitle">
          Expédition
          <a v-if="editable" class="tag" href="#" @click="openAddPlacename('location-date-from')">
            <icon-add/>
          </a>
        </h3>

        <ul class="document-placenames__senders-list" v-if="locationDateFrom.length">
          <li v-for="c in locationDateFrom" :key="c.placename.id" class="placename-item">
            <a :href="c.placename.ref" target="_blank">
              {{ c.placename.label }}
            </a>
            <a v-if="editable" class="witness-item__delete" @click="unlinkPlacenameFromDoc(c)">
              <icon-bin/>
            </a>
          </li>
        </ul>
        
        <div v-else>
          <p class="placename-item"><em>Aucune date de lieu n'a été renseignée</em></p>
        </div>
      
      </div>
      
      <div class="document-placenames__recipients column">
        
        <h3 class="document-persons__subtitle">
          Destination{{ locationDateTo.length > 1 ? 's':'' }}
          <a v-if="editable && locationDateTo.length === 0" class="tag" href="#"
             @click="openAddPlacename('location-date-to')">
            <icon-add/>
          </a>
        </h3>

        <ul class="document-placenames__recipients-list" v-if="locationDateTo.length">
          <li v-for="c in locationDateTo" :key="c.placename.id" class="placename-item">
            <a :href="c.placename.ref" target="_blank">
              {{ c.placename.label }}</a>
            <a v-if="editable" class="placename-item__delete" @click="unlinkPlacenameFromDoc(c)">
              <icon-bin/>
            </a>
          </li>
        </ul>
        
        <div v-else>
          <p class="placename-item"><em>Aucune date de lieu n'a été renseignée</em></p>
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
                    roleId
                })
                    .then(placenameHasRole => {
                        if (!!placenameHasRole) {
                            const corrData = {
                                placename,
                                placenameId,
                                relationId: placenameHasRole.id,
                                role,
                                roleId
                            };
                            this.$store.dispatch('document/addPlacename', corrData);
                        }
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
