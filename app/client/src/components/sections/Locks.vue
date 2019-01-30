<template>
   <section>
      <header v-if="!compact">
         <h2 class="section__title subtitle">Documents verrouillés</h2>
      </header>

      <table class="table is-narrow" :class="!compact ? 'is-bordered is-striped is-hoverable' : ''">
        <thead :class="compact ? 'is-invisible' : ''">
          <tr>
             <th style="min-width: 180px;">Date de début</th>
             <th style="min-width: 180px;">Date de fin</th>
             <th v-if="!compact">Objet</th>
             <th>Description</th>
             <th>Utilisateur</th>
          </tr>
        </thead>
         <tbody v-for="change in data" :key="change.id">
            <tr>
              <td>{{change.data.attributes["event-date"]}}</td>
              <td>{{change.data.attributes["expiration-date"]}}</td>
              <td v-if="!compact">
                 <a :href="url">
                    <span class="tag">{{change.data.attributes["object-type"]}} {{change.data.attributes["object-id"]}}</span>
                 </a>
              </td>
              <td>{{change.data.attributes["description"]}}</td>
              <td><span class="tag">{{change.user.username}}</span></td>
            </tr>
         </tbody>
      </table>

   </section>
</template>

<script>
  export default {
    name: "locks",
    components : {},
    props: {
      data: {required: true},
      compact: {default: false}
    },
    data () {
      return {

      }
    },
    created() {
    },
    computed: {

    }
  }
</script>

<style scoped>
  .section__title {
    margin-bottom: 20px;
  }
  td {
    color: #962D3E;
  }
  td a:hover span{
    background: #EBEBEB;
    color: #348899 ;
  }
</style>
