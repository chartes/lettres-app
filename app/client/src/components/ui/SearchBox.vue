<template>
    <div class="search-container">
       <div class="field has-addons">
         <div class="control">
           <input id="search-box" class="input search-container__search-box" type="text"
                  placeholder="Catherine de Medicis"
                  @keyup.enter="action()">
         </div>
         <div class="control" v-on:click="action()">
           <button :class="myClasses"><i class="fas fa-search"></i></button>
         </div>
       </div>
    </div>
</template>

<script>
  export default {
    name: "search-box",
    props: {
      action: { required: true } ,
      loading: {
        type: Boolean,
        default: false
      },
    },
    data() {
      return {
      }
    },
    created() {
    },
    computed: {
      myClasses () {
        let classes = ['button search-container__search-box__submit-btn'];
        if (this.loading) classes.push('is-loading');
        return classes.join(' ')
      }
    }
  }
</script>

<style scoped>
  .search-container__search-box {
    padding-left: 1em !important;

    margin-bottom: 50px;
  }
  .search-container__search-box__submit-btn {
    color: #962D3E;
    background: whitesmoke ;
  }
  .search-container__search-box__submit-btn:hover {
    color: #348899 ;
  }
  .search-container .control {
     width: 400px;
  }
</style>
