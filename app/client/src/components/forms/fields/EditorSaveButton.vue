<template>
    <button
            class="argument__save button is-small"
            :class="saveButtonClass"
            :disabled="status === 'disabled'"
            @click="clickSave"
    >
        <component :is="saveButtonIcon"/>
    </button>
</template>

<script>

    import IconSave from '../../ui/icons/IconSave';
    import IconError from '../../ui/icons/IconError';
    import IconSuccess from '../../ui/icons/IconSuccess';


  export default {
      name: "editor-save-button",
      props: {
          name: {
              type: String, required: true
          },
          value: {
              type: String, required: true
          },
          docId: {
              type: Number, required: true
          }
      },
      data() {
          return {
              status: 'normal',
              editorEnabled: true,
              form: ''
          }
      },

      methods: {
          clickSave () {
              if (this.status === 'error' || this.status === 'success') return;
              this.status = 'loading';
              const attributes = {}
              attributes[this.name] = this.value;
              const data = { id: this.docId, attributes };
              console.log('saves transcription ', data )
              this.$store.dispatch('document/save', data)
                      .then(response => {
                          this.status = 'success'
                          setTimeout(() => this.status = 'normal', 3000)
                      }).catch(() => {
                  this.status = 'error'
                  setTimeout(() => this.status = 'normal', 3000)
              })
          },
      },

      computed: {
          saveButtonClass () {
              switch (this.status) {
                  case 'normal':
                  case 'disabled':
                      return 'is-success'
                      break
                  case 'success':
                      return 'is-success'
                      break
                  case 'error':
                      return 'is-danger'
                      break
                  case 'loading':
                      return 'is-loading'
              }
          },
          saveButtonIcon () {
              switch (this.status) {
                  case 'normal':
                  case 'loading':
                  case 'disabled':
                      return IconSave;
                      break;
                  case 'success':
                      return IconSuccess;
                      break;
                  case 'error':
                      return IconError;
                      break;
              }
          },
      },
  }
</script>
