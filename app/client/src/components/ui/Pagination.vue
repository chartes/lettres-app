<template>
    <div class="buttons are-normal">
        <span v-if="curr > 1" class="button" @click="action(1)">1</span>
        <span v-if="curr > 1"  class="dotdot">...</span>
        <span v-if="prev > 1" class="button" @click="action(prev)">{{prev}}</span>
        <span v-if="curr <= end" class="button current-page" @click="action(curr)">{{curr}}</span>
        <span v-if="next > 1 && next < end" class="button" @click="action(next)">{{next}}</span>
        <span v-if="end > 1 && next < end" class="dotdot">...</span>

        <span v-if="end > 1 && curr < end" class="button" @click="action(end)">{{end}}</span>
    </div>
</template>

<script>
  export default {
    name: "pagination",
    props: {
        start: {default: 1},
        current: { required: true, default: 1},
        end: { required: true },
        action: { required: true}
    },
    data () {
      return {

      }
    },
    created() {
        console.warn(this.current);
    },
    computed: {
        prev: function() { return (this.current > 1 ) ? this.current - 1 : 1},
        curr: function() { return this.current },
        next: function() { return (this.current < this.end) ? this.current + 1 : this.end },
    }
  }
</script>

<style scoped>
    span {
        color: #962D3E;
        background: white;
    }
    .button:hover {
        background: #962D3E;
        color: white;
    }
    .dotdot {
        margin-left: 6px;
        margin-right: 12px;
    }
    .current-page {
        background: #962D3E;
        color: white;
    }
</style>
