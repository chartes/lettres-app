<template>
    <div class="container pagination buttons are-normal" v-if="end > 1">
        <span v-if="curr > 1" class="pagination__button button" @click="action(1)">1</span>
        <span v-if="curr > 2"  class="pagination__dot-dot">...</span>
        <span v-if="prev > 1" class="pagination__button button" @click="action(prev)">{{prev}}</span>
        <span v-if="curr <= end" class="pagination__button button pagination__button--current" @click="action(curr)">{{curr}}</span>
        <span v-if="next > 1 && next < end" class="pagination__button button" @click="action(next)">{{next}}</span>
        <span v-if="end > 1 && next+1 < end" class="pagination__dot-dot">...</span>
        <span v-if="end > 1 && curr < end" class="pagination__button button" @click="action(end)">{{end}}</span>
    </div>
</template>

<script>
  export default {
    name: "pagination",
    props: {
        start: {default: 1, type: Number},
        current: { required: true, default: 1, type: Number},
        end: { required: true, type: Number },
        action: { required: true, type: Function}
    },
    data () {
      return {

      }
    },
    created() {
    },
    computed: {
        prev: function() { return (this.current > 1 ) ? this.current - 1 : 1},
        curr: function() { return this.current },
        next: function() { return (this.current < this.end) ? this.current + 1 : this.end },
    }
  }
</script>

<style scoped>
    .pagination + span {
        color: #962D3E;
        background: white;
    }
    .pagination {
       justify-content: center;
    }
    .pagination__button {
        min-width: 40px;
    }
    .pagination__button:hover {
        background: #962D3E;
        color: white;
    }
    .pagination__dot-dot {
        margin-left: 6px;
        margin-right: 12px;
        color: #962D3E;
    }
    .pagination__button--current {
        background: #962D3E;
        color: white;
    }
</style>
