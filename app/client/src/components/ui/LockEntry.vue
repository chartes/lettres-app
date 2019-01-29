<template>
   <tr>
      <td>{{entry.attributes["event-date"]}}</td>
      <td>{{entry.attributes["expiration-date"]}}</td>
      <td v-if="!compact">
         <a :href="url">
            <span class="tag">{{entry.attributes["object-type"]}} {{entry.attributes["object-id"]}}</span>
         </a>
      </td>
      <td>{{entry.attributes["description"]}}</td>
      <td><span class="tag">{{user.username}}</span></td>
   </tr>
</template>

<script>
  export default {
    name: "lock-entry",
    props: {
       entry: {required: true},
       user: {}              ,
       compact: {default: false}
    },
    data () {
      return {
             url: `documents/${this.entry.attributes["object-id"]}`
      }
    },
    created() {
    },
    computed: {
    }
  }
</script>

<style scoped>
td {
   color: #962D3E;
}
 td a:hover span{
  background: #EBEBEB;
  color: #348899 ;
 }
</style>
