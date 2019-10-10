<template>
  <div class="modal is-active">
    <div class="modal-background" @click="cancel"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title" v-html="title"></p>
        <button class="delete" aria-label="close" @click="cancel"></button>
      </header>
      <section class="modal-card-body">
        <slot></slot>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-success" v-if="submit" :disabled="!valid || submitting" @click="submit">{{submitText}}</button>
        <button class="button" v-if="cancel" :disabled="submitting" @click="cancel">Annuler</button>
        <div style="float: right;width: 100%;text-align: right;" v-if="remove">
          <button class="button is-danger" :disabled="submitting" @click="remove">{{removeText}}</button>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>

  export default {
    name: "modal-form",
    props: {
      title: { type: String, default: ''},
      cancel: { type: Function},
      submit: { type: Function},
      remove: { type: Function},
      valid: { type: Boolean, required: true},
      submitText: { type: String, default: 'Enregistrer'},
      removeText: {type: String, default: 'Supprimer'},
      submitting: { type: Boolean, default: false},
    },
    mounted () {
      document.addEventListener('keyup', this.onKeyUp)
    },
    methods: {
      onKeyUp (e) {
        if (!(e.target === document.body)) return;
        if (e.code === 'Enter') this.submit()
        else if (e.code === 'Escape') this.cancel()

      }
    },
    beforeDestroy () {
      document.removeEventListener('keyup', this.onKeyUp)
    }
  }
</script>
