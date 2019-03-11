<template>
  <div class="document-correspondents document__subsection">
    <header class="document-correspondents__header">
      <h2 class="document-correspondents__title subtitle">Correspondants</h2>
    </header>

    <div class="columns">

      <div class="document-correspondents__senders column">

        <h3 class="document-correspondents__subtitle document-correspondents__subtitle--sender">Expéditeur</h3>

        <ul class="document-correspondents__senders-list" v-if="documentSender.length">
          <li v-for="c in documentSender" :key="c.person.id" class="correspondent-item">
            <a :href="c.person.ref" target="_blank">
              {{ c.person.label }}
            </a>
            <span class="tag">{{ c.role.label }}</span>
            <a v-if="editable" class="correspondent-item__delete" @click="unlinkPersonFromDoc(c)"><icon-bin/></a>
          </li>
        </ul>

        <div v-else>
          <p class="correspondent-item"><em>Aucun expéditeur n'a été renseigné</em></p>
          <p v-if="editable">
            <lauch-button label="Sélectionner un expéditeur" @click="openAddPerson('sender')"/>
          </p>
        </div>

      </div>

      <div class="document-correspondents__recipients column">

        <h3 class="document-correspondents__subtitle document-correspondents__subtitle--recipient">Destinataire{{ documentRecipients.length > 1 ? 's':'' }}</h3>

        <ul class="document-correspondents__recipients-list" v-if="documentRecipients.length">
          <li v-for="c in documentRecipients" :key="c.person.id" class="correspondent-item">
            <a :href="c.person.ref" target="_blank">
              {{ c.person.label }}</a>
            <span class="tag">{{ c.role.label }}</span>
            <a v-if="editable" class="correspondent-item__delete" @click="unlinkPersonFromDoc(c)"><icon-bin/></a>
          </li>
        </ul>

        <div v-else>
          <p class="correspondent-item"><em>Aucun destinataire n'a été renseigné</em></p>
        </div>

        <div v-if="editable">
          <p>
            <lauch-button label="Ajouter un destinataire" @click="openAddPerson('recipient')"/>
          </p>
        </div>


      </div>

      <person-list-form
          v-if="personsForm && editable"
          title="Sélectionner une personne"
          :submit="linkPersonToDoc"
          :cancel="closePersonChoice"
      />

    </div>
  </div>
</template>

<script>

  import { mapState, mapGetters } from 'vuex'
  import IconBin from '../ui/icons/IconBin';
  import PersonListForm from '../forms/PersonListForm';
  import LauchButton from '../forms/LaunchButton';
  export default {
    name: 'DocumentPersons',
    components: {LauchButton, PersonListForm, IconBin},
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