<template>
  <div id="app" class="d-flex">
    <div id="items-list" class="vh-100 pt-3 px-0" :class="{ 'opened': leftPanel }" @mousemove="openLeftPanel" @mouseleave="closeLeftPanel">
      <Search @search-focused="changeSearchStatus($event)" ref="mySearch"></Search>
      <hr class="mb-1 mt-2 mx-2">
      <NotesList ref="myNotes"></NotesList>
    </div>
    <div id="data-view" class="vh-100 w-100">
      <Note ref="myNote"></Note>
    </div>
  </div>
</template>

<script>
import NotesList from './components/NotesList.vue'
import Search from './components/Search.vue'
import Note from './components/Note.vue'

export default {
  name: 'App',
  components: {
    NotesList,
    Search,
    Note
  },
  data: function () {
    return {
      leftPanel: false,
      leftPanelMouseOver: false,
      searchFocused: false
    }
  },
  methods: {
    openLeftPanel: function(e) {
      if (e.pageX <= 50) {
        this.leftPanel = true;
        this.leftPanelMouseOver = true;
      }
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
    },
  }
}
</script>

<style>
body {
  overflow: hidden;
}

#items-list.opened {
  width: 340px;
}

#items-list {
  transition-duration: .2s;
  width: 40px;
  border-right: 1px solid lightgray;
}

#items-list.opened > div {
  opacity: 1;
}

#items-list > div {
  transition: .3s;
  opacity: 0;
}

#items-list.opened .fade-effect {
  left: 100%;
}

#items-list .fade-effect {
  transition-duration: .2s;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0px;
  background: white;
}

#items-list.opened .notes-main {
  margin-left: 0px;
}

#items-list .notes-main {
  transition-duration: .2s;
  margin-left: -300px;
}

#items-list.opened + #data-view {
  max-width: calc(100% - 340px);
}

.vertical-separator {
  border-right: 1px solid lightgray;
}
</style>