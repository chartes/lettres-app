<template>
  <section v-if="correspondents.length > 0" class="document-correspondents section">
    <header class="document-correspondents__header">
      <h2 class="document-correspondents__title subtitle">Correspondants</h2>
    </header>

    <div class="columns">

      <div class="document-correspondents__senders column">

        <h3 class="document-correspondents__subtitle">Expéditeur</h3>

        <ul class="document-correspondents__senders-list" v-if="documentSender.length">
          <li v-for="c in documentSender" :key="c.correspondent.id" class="correspondent-item">
            <a :href="c.correspondent.ref" target="_blank">
              {{ c.correspondent.firstname + ' ' + c.correspondent.lastname }}
            </a>
            <span class="tag">{{ c.role.label }}</span>
            <a if="userCanEdit" class="witness-item__delete"><icon-bin/></a>
          </li>
        </ul>

        <div v-else>
          <p class="correspondent-item"><em>Aucun expéditeur n'a été renseigné</em></p>
          <p>
            <a if="userCanEdit"
               href="#"
               class="button"
               @click.prevent="addCorrespondent('sender')"
            >Ajouter l'expéditeur</a>
          </p>
        </div>

      </div>

      <div class="document-correspondents__recipients column">

        <h3 class="document-correspondents__subtitle">Destinataire{{ documentRecipients.length > 1 ? 's':'' }}</h3>

        <ul class="document-correspondents__recipients-list"  v-if="documentRecipients.length">
          <li v-for="c in documentRecipients" :key="c.correspondent.id" class="correspondent-item">
            <a :href="c.correspondent.ref" target="_blank">
              {{ c.correspondent.firstname + ' ' + c.correspondent.lastname }}</a>
            <span class="tag">{{ c.role.label }}</span>
            <a if="userCanEdit" class="correspondent-item__delete"><icon-bin/></a>
          </li>
        </ul>

        <div v-else>
          <p class="correspondent-item"><em>Aucun destinataire n'a été renseigné</em></p>
          <p>
            <a if="userCanEdit"
                href="#"
                class="button"
                @click.prevent="addCorrespondent('recipient')"
            >Ajouter un destinataire</a>
          </p>
        </div>


      </div>

      <correspondent-list-form
          v-if="correspondentsForm"
          title="Ajouter un correspondant"
          :cancel="closeCorrespondentChoice"
      />

    </div>
  </section>
</template>

<script>

  import { mapState, mapGetters } from 'vuex'
  import IconBin from '../forms/icons/IconBin';
  import CorrespondentListForm from '../forms/CorrespondentListForm';
  export default {
    name: 'DocumentCorrespondents',
    components: {CorrespondentListForm, IconBin},
    data () {
      return {
        correspondentsForm: ''
      }
    },
    methods: {
      addCorrespondent (role) {
        this.correspondentsForm = role;
      },
      closeCorrespondentChoice() {
        this.correspondentsForm = '';
      }
    },
    computed: {
      ...mapState('document', ['correspondents']),
      ...mapGetters('document', ['documentSender', 'documentRecipients']),
      ...mapState('document', ['correspondents']),
    }
  }

</script>

<style>
</style>