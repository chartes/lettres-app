<template>
    <section class="search-container">
       <h1 class="title is-size-5">Rechercher</h1>
       <div class="field has-addons">
         <div class="control">
           <input id="search-box" class="input search-container__search-box" type="text"
                  placeholder="Catherine de Medicis"
                  @keyup.enter="action()">
         </div>
         <div class="control" v-on:click="action()">
           <button :class="myClasses">Search</button>
         </div>
       </div>
    </section>
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
      width: 420px;
  }
  .search-container__search-box__submit-btn {
    color: #962D3E;
    background: whitesmoke ;
  }
  .search-container__search-box__submit-btn:hover {
    color: #348899 ;
  }
  .search-container {
      margin-top: 10px;
      padding-bottom: 60px;
  }
</style>
