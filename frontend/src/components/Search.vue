<template>
  <div class="mx-2">
    <input
      type="text"
      class="form-control"
      placeholder="Just start typing"
      @focus="srchFocused"
      @blur="srchBlured"
      @input="srchChanged"
      @keydown="controlFocus"
      v-model="searchValue"
    />
    <transition name="fade">
      <div class="dropdown-list" v-show="isListVisible" id="dropdown-list">
        <div class="dropdown-list-item" :class="{ 'focus': 0 === focus }" @mouseover="setFocus(0)" @click="createNewTag()">Create tag</div>
        <div class="dropdown-list-item" :class="{ 'focus': 1 === focus }" @mouseover="setFocus(1)" @click="createNewNote()">Create note</div>
        <div
          v-for="(item, index) in findedTags()"
          :key="item.id"
          :class="{ 'focus': index+2 === focus }"
          class="dropdown-list-item text-truncate"
          @mouseover="setFocus(index+2)"
          @click="addTagToFilters(item)"
        >
          {{ item.name }}
        </div>
      </div>
    </transition>
    <div class="mt-2" id="pinned-tags">
      <span
        class="badge rounded-pill bg-primary pinned-tag"
        v-for="tag in filterTags"
        :key="tag.id"
      >
        <p class="text-truncate float-start pinned-tag-text">
          {{ tag.name }}
        </p>
        <button class="text-white btn btn-sm p-0 ms-1 lh-1 fw-bold" @click="deleteFilterTag(tag.id)">X</button>
      </span>
      <div class="fade-effect"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Search",
  data: function() {
    return {
      tagsList: [
        { name: "test", id: 1 },
        { name: "qwe", id: 2 },
        { name: "ewq", id: 3 },
        { name: "adhgsasfasgfasdgsdfhdfjfgjfghkghklgltudfghsrgaedgsdfhsfdjhdf", id: 4 },
        { name: "gfhklgh", id: 5 },
        { name: "syhwr", id: 6 },
        { name: "jfkqf", id: 7 },
        { name: "jfwkf", id: 8 },
        { name: "jfkef", id: 9 },
        { name: "jfkrf", id: 10 },
        { name: "jfktf", id: 11 },
        { name: "jfkyf", id: 12 },
        { name: "jfkuf", id: 13 },
        { name: "jfkif", id: 14 },
        { name: "jfkof", id: 15 },
        { name: "jfkpf", id: 16 },
      ],
      isListVisible: false,
      searchValue: '',
      focus: 0,
      filterTags: []
    };
  },
  methods: {
    srchFocused: function() {
      this.$emit("search-focused", true);
      if (this.searchValue.length > 1) {
        this.isListVisible = true;
      }
    },
    srchBlured: function() {
      setTimeout(() => {
        this.$emit("search-focused", false);
        this.isListVisible = false;
      }, 200);
    },
    srchChanged: function() {
      if (this.searchValue.length > 1) {
        this.isListVisible = true;
      } else {
        this.isListVisible = false;
      }
      // TODO: Filter notes
    },
    controlFocus: function(event) {
      let elem = document.getElementById('dropdown-list');
      switch (event.keyCode) {
        case 38:
          if (this.focus > 0) this.focus--;
          if (this.focus > 5) elem.scrollTop -= 36;
          break;
        case 27:
          if (document.activeElement instanceof HTMLElement)
            document.activeElement.blur();
          break;
        case 40:
          if (this.focus < this.findedTags().length + 1) this.focus++;
          if (this.focus > 7) elem.scrollTop += 36;
          break;
        case 13:
          if (this.focus == 0) {
            this.createNewTag();
            break;
          }
          if (this.focus == 1) {
            this.createNewNote();
            break;
          }
          if (this.findedTags().length <= this.focus-2) break;
          this.addTagToFilters(
            this.findedTags()[this.focus-2]
          );
          break;
      }
    },
    setFocus: function(index) {
      this.focus = index;
    },
    createNewTag: function() {
      this.isListVisible = false;
      this.searchValue = '';
      console.log('TAG CREATE');
      // TODO: AXIOS
    },
    createNewNote: function() {
      this.isListVisible = false;
      this.searchValue = '';
      console.log('NOTE CREATE');
      // TODO: AXIOS
    },
    addTagToFilters: function(item) {
      console.log('TAG ADDED');

      this.isListVisible = false;
      this.searchValue = '';
      this.filterTags.push(item);
    },
    findedTags: function() {
      let filteredByQuery = this.tagsList.filter((item) => {
        return !item.name.search(this.searchValue);
      });
      return filteredByQuery.filter(item => !this.filterTags.includes(item));
    },
    findedNotes: function() {
      // TODO: AXIOS
    },
    deleteFilterTag: function(id) {
      this.filterTags = this.filterTags.filter((item) => item.id != id);
    }
  },
};
</script>

<style scoped>
.dropdown-list {
  position: absolute;
  width: 325px;
  max-height: 300px;
  overflow-y: auto;
  overflow-x: none;
  background: rgb(253, 253, 253);
  z-index: 999;
  border: 1px solid rgb(240, 240, 240);
  border-radius: 5px;
}

.dropdown-list-item {
  padding: 6px 8px;
  cursor: pointer;
}

.dropdown-list-item.focus {
  background: #0D6EFD;
  color: white;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .1s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

.pinned-tag {
  margin: 0px 2px;
  max-width: 310px;
}

.pinned-tag-text {
  max-width: 280px;
  margin: 0;
  margin-top: 3px;
  padding-right: 5px;
}

#pinned-tags {
  position: relative;
  width: 320px;
}
</style>
