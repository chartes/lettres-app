<template>
  <section class="document-persons ">
    <header class="document-persons__header">
      <h2 class="document-persons__title subtitle">Correspondants</h2>
    </header>

    <div class="columns">

      <div class="document-persons__senders column">

        <h3 class="document-persons__subtitle">
          Expéditeur
          <a v-if="editable" class="tag" href="#" @click="openAddPerson('sender')">
            <icon-add/>
          </a>
        </h3>

        <ul class="document-persons__senders-list" v-if="documentSender.length">
          <li v-for="c in documentSender" :key="c.person.id" class="person-item">
            <a :href="c.person.ref" target="_blank">
              {{ c.person.label }}
            </a>
            <a v-if="editable" class="witness-item__delete" @click="unlinkPersonFromDoc(c)"><icon-bin/></a>
          </li>
        </ul>

        <div v-else>
          <p class="person-item"><em>Aucun expéditeur n'a été renseigné</em></p>
        </div>

      </div>

      <div class="document-persons__recipients column">

        <h3 class="document-persons__subtitle">
          Destinataire{{ documentRecipients.length > 1 ? 's':'' }}
          <a v-if="editable" class="tag" href="#" @click="openAddPerson('recipient')">
            <icon-add/>
          </a>
        </h3>

        <ul class="document-persons__recipients-list" v-if="documentRecipients.length">
          <li v-for="c in documentRecipients" :key="c.person.id" class="person-item">
            <a :href="c.person.ref" target="_blank">
              {{ c.person.label }}</a>
            <a v-if="editable" class="person-item__delete" @click="unlinkPersonFromDoc(c)"><icon-bin/></a>
          </li>
        </ul>

        <div v-else>
          <p class="person-item"><em>Aucun destinataire n'a été renseigné</em></p>
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