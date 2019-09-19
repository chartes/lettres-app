<template>
  <section class="document-correspondents">
    <div class="panel">
      <header class="panel-heading">
        <h2 class="document-correspondents__title subtitle">Correspondants</h2>
      </header>
      <div class="panel-block" style="display: inline-block; width: 100%">
        <div class="subtitle mb-2" >
          Expéditeur{{documentSender.length > 1 ? 's' :''}}
          <a v-if="editable" class="tag" href="#" @click="openAddPerson('sender')">
            <icon-add/>
          </a>
        </div>
        <div v-if="documentSender.length" v-for="c in documentSender" :key="c.person.id"
             class="tags has-addons are-medium correspondent-item mb-1">
                <span class="tag">
                    <a :href="c.person.ref" target="_blank">
                      {{ c.person.label }}
                    </a>
                </span>
                <a v-if="editable" class="tag is-delete" @click.prevent="unlinkPersonFromDoc(c)"></a>
        </div>
        <div v-if="documentSender.length === 0">
          <p class="person-item"><em>Aucun expéditeur renseigné</em></p>
        </div>
      </div>
      <div class="panel-block" style="display: inline-block; width: 100%">
        <div class="subtitle mb-2">
            Destinataire{{ documentRecipients.length > 1 ? 's':'' }}
          <a v-if="editable" class="tag" href="#" @click="openAddPerson('recipient')">
            <icon-add/>
          </a>
        </div>
        <div v-if="documentRecipients.length > 0" v-for="c in documentRecipients" :key="c.person.id"
             class="tags has-addons are-medium correspondent-item mb-1">
             <span class="tag">
                 <a :href="c.person.ref" target="_blank">{{ c.person.label }}</a>
             </span>
             <a v-if="editable" class="tag is-delete" @click.prevent="unlinkPersonFromDoc(c)"></a>
        </div>
        <div v-if="documentRecipients.length === 0">
          <p class="person-item"><em>Aucun destinataire renseigné</em></p>
        </div>
      </div>
  
      <person-list-form
          v-if="personsForm && editable"
          title="Sélectionner une personne"
          :submit="linkPersonToDoc"
          :cancel="closePersonChoice"
      />
      </div>
  

  </section>
</template>

<script>

  import { mapState, mapGetters } from 'vuex'
  import IconBin from '../ui/icons/IconBin';
  import PersonListForm from '../forms/PersonListForm';
  import LauchButton from '../forms/LaunchButton';
  import IconAdd from "../ui/icons/IconAdd";
  export default {
    name: 'DocumentPersons',
    components: {LauchButton, PersonListForm, IconBin, IconAdd},
    props: {
      editable: {
        type: Boolean,
        default: false
      },
    },
    data () {
      return {
        personsForm: null
      }
    },
    mounted () {
      this.$store.dispatch('persons/fetchRoles')
    },
    methods: {
      openAddPerson (role) {
        this.personsForm = role;
      },
      closePersonChoice() {
        this.personsForm = null;
      },
      linkPersonToDoc(person) {
        const personId = person.id
        const role = this.getRoleByLabel(this.personsForm)
        const roleId =  role && role.id ? role.id : null;
        this.$store.dispatch('persons/linkToDocument', {
          personId,
          roleId
        })
          .then(personHasRole => {
            const corrData = {
              person,
              personId,
              relationId: personHasRole.id,
              role,
              roleId
            }
            this.$store.dispatch('document/addPerson', corrData);
            this.closePersonChoice()
          })
      },
      unlinkPersonFromDoc(person) {
        const personId = person.personId
        const roleId =  person.roleId
        this.$store.dispatch('persons/unlinkFromDocument', {
            relationId: person.relationId,
            personId,
            roleId
          })
          .then(response => {
            this.closePersonChoice()
          })
      }
    },
    computed: {
      ...mapState('document', ['persons']),
      ...mapState('persons', ['roles']),
      ...mapGetters('document', ['documentSender', 'documentRecipients']),
      ...mapGetters('persons', ['getRoleByLabel']),
    }
  }

</script>

<style>
</style>
