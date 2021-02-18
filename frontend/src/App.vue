<template>
  <div id="app" class="d-flex">
    <div id="items-list" class="vh-100 pt-3 px-2" :class="{ 'opened': leftPanel }" @mouseover="openLeftPanel" @mouseleave="closeLeftPanel">
      <Search @search-focused="changeSearchStatus($event)"></Search>
      <hr class="my-3">
      <ItemsList></ItemsList>
    </div>
    <div id="data-view" class="vh-100 w-100">
      Somebody once told me
    </div>
  </div>
</template>

<script>
import ItemsList from './components/ItemsList.vue'
import Search from './components/Search.vue'

export default {
  name: 'App',
  components: {
    ItemsList,
    Search
  },
  data: function () {
    return {
      leftPanel: false,
      leftPanelMouseOver: false,
      searchFocused: false
    }
  },
  methods: {
    openLeftPanel: function() {
      this.leftPanel = true;
      this.leftPanelMouseOver = true;
    },
    closeLeftPanel: function() {
      if (!this.searchFocused) {
        this.leftPanel = false;
      }
      this.leftPanelMouseOver = false;
    },
    changeSearchStatus: function (data) {
      this.searchFocused = data;
      if (!this.leftPanelMouseOver) {
        this.leftPanel = false;
      }
    }
  }
}
</script>

<style>
#items-list.opened {
  width: 340px;
}
#items-list {
  transition-duration: .2s;
  width: 40px;
  border-right: 1px solid lightgray;
}
#items-list.opened > div > .form-control {
  opacity: 1;
}
#items-list > div > .form-control {
  transition: .3s;
  opacity: 0;
}
#items-list.opened + #data-view {
  max-width: calc(100% - 340px);
}
</style>