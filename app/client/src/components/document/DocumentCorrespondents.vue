<template>
  <section v-if="correspondents.length > 0" class="document-correspondents section">
    <header class="document-correspondents__header">
      <h2 class="document-correspondents__title subtitle">Correspondants</h2>
    </header>

    <div class="columns">

      <div class="document-correspondents__senders column">

        <h3 class="document-correspondents__subtitle document-correspondents__subtitle--sender">Expéditeur</h3>

        <ul class="document-correspondents__senders-list" v-if="documentSender.length">
          <li v-for="c in documentSender" :key="c.correspondent.id" class="correspondent-item">
            <a :href="c.correspondent.ref" target="_blank">
              {{ c.correspondent.firstname + ' ' + c.correspondent.lastname }}
            </a>
            <span class="tag">{{ c.role.label }}</span>
            <a v-if="editable" class="correspondent-item__delete" @click="unlinkCorrespondentFromDoc(c)"><icon-bin/></a>
          </li>
        </ul>

        <div v-else>
          <p class="correspondent-item"><em>Aucun expéditeur n'a été renseigné</em></p>
          <p v-if="editable">
            <lauch-button class="correspondent-item__add" if="userCanEdit" label="Ajouter l'expéditeur" @click="openAddCorrespondent('sender')"/>
          </p>
        </div>

      </div>

      <div class="document-correspondents__recipients column">

        <h3 class="document-correspondents__subtitle document-correspondents__subtitle--recipient">Destinataire{{ documentRecipients.length > 1 ? 's':'' }}</h3>

        <ul class="document-correspondents__recipients-list" v-if="documentRecipients.length">
          <li v-for="c in documentRecipients" :key="c.correspondent.id" class="correspondent-item">
            <a :href="c.correspondent.ref" target="_blank">
              {{ c.correspondent.firstname + ' ' + c.correspondent.lastname }}</a>
            <span class="tag">{{ c.role.label }}</span>
            <a v-if="editable" class="correspondent-item__delete" @click="unlinkCorrespondentFromDoc(c)"><icon-bin/></a>
          </li>
        </ul>

        <div v-else>
          <p class="correspondent-item"><em>Aucun destinataire n'a été renseigné</em></p>
        </div>

        <div v-if="editable">
          <p>
            <lauch-button class="correspondent-item__add" label="Ajouter un destinataire" @click="openAddCorrespondent('recipient')"/>
          </p>
        </div>


      </div>

      <correspondent-list-form
          v-if="correspondentsForm && editable"
          title="Ajouter un correspondant"
          :submit="linkCorrespondentToDoc"
          :cancel="closeCorrespondentChoice"
      />

    </div>
  </section>
</template>

<script>

  import { mapState, mapGetters } from 'vuex'
  import IconBin from '../ui/icons/IconBin';
  import CorrespondentListForm from '../forms/CorrespondentListForm';
  import LauchButton from '../forms/LaunchButton';
  export default {
    name: 'DocumentCorrespondents',
    components: {LauchButton, CorrespondentListForm, IconBin},
    props: {
      editable: {
        type: Boolean,
        default: false
      },
    },
    data () {
      return {
        correspondentsForm: null
      }
    },
    mounted () {
      this.$store.dispatch('correspondents/fetchRoles')
    },
    methods: {
      openAddCorrespondent (role) {
        this.correspondentsForm = role;
      },
      closeCorrespondentChoice() {
        this.correspondentsForm = null;
      },
      linkCorrespondentToDoc(correspondent) {
        const correspondentId = correspondent.id
        const role = this.getRoleByLabel(this.correspondentsForm)
        const roleId =  role && role.id ? role.id : null;
        this.$store.dispatch('correspondents/linkToDocument', {
          correspondentId,
          roleId
        })
          .then(correspondentHasRole => {
            const corrData = {
              correspondent,
              correspondentId,
              relationId: correspondentHasRole.id,
              role,
              roleId
            }
            this.$store.dispatch('document/addCorrespondent', corrData);
            this.closeCorrespondentChoice()
          })
      },
      unlinkCorrespondentFromDoc(correspondent) {
        const correspondentId = correspondent.correspondentId
        const roleId =  correspondent.roleId
        this.$store.dispatch('correspondents/unlinkFromDocument', {
            relationId: correspondent.relationId,
            correspondentId,
            roleId
          })
          .then(response => {
            this.closeCorrespondentChoice()
          })
      }
    },
    computed: {
      ...mapState('document', ['correspondents']),
      ...mapState('correspondents', ['roles']),
      ...mapGetters('document', ['documentSender', 'documentRecipients']),
      ...mapGetters('correspondents', ['getRoleByLabel']),
    }
  }

</script>

<style>
</style>