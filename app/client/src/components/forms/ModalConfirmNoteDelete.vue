<template>

    <modal-confirm
            :title="'Supprimer la note ?'"
            :submitText="'Oui je veux la supprimer'"
            :cancel="cancelAction"
            :submit="submitAction"
            class="has-text-danger"
    >
                <p><b>Danger</b></p>
                <p>Vous êtes sur le point de supprimer une note.</p>
                <p>La note sera également perdue pour la transcription de ce document, sa traduction et ses commentaires.</p>
                <p><b>Cette action ne peut pas être annulée.</b></p>

    </modal-confirm>



</template>

<script>

    import ModalConfirm from './ModalConfirm';

  export default {
    name: "MmodalConfirmNoteDelete",
    props: ['cancel', 'submit', 'noteId'],
    components: {
      ModalConfirm
    },
    methods: {
      submitAction () {
        console.log("MmodalConfirmNoteDelete submit", this.noteId)
        this.$props.submit(this.noteId);
      },
      cancelAction () {
        this.$props.cancel();
      }
    }
  }
</script>
