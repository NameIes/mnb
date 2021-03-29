<template>
  <div id="note-main">
    <div class="w-100 text-center" v-if="!openedNote">
      <h4 class="mt-5">Please open note</h4>
    </div>

    <div v-else-if="isEditing" class="ms-1 mt-3 h-100 edit-div row">
      <div class="col-xl-10 col-lg-8 col-md-6 order-md-0 order-1">
        <input type="text" class="form-control from-control-lg float-start w-100" v-model="openedNote.name">
        <textarea class="w-100 mt-2" v-model="noteData"></textarea>
      </div>
      <div class="col-xl-2 col-lg-4 col-md-6 order-md-1 order-0 px-2">
        <button class="btn btn-danger py-0 px-3 mt-1 float-start" @click="cancelDataChanges()">Cancel</button>
        <button class="btn btn-success py-0 px-4 mt-1 float-end" @click="saveDataChanges()">Save</button>
        <br style="clear: both">
        <hr class="my-2">
        <button
          class="btn w-50 float-start note-btn py-0"
          :class="openedNote.is_note ? 'btn-primary' : 'btn-outline-primary'"
          @click="openedNote.is_note = true"
        >
          Note
        </button>
        <button
          class="btn w-50 float-end todo-btn py-0"
          :class="!openedNote.is_note ? 'btn-primary' : 'btn-outline-primary'"
          @click="openedNote.is_note = false"
        >
          ToDo
        </button>
        <div v-show="!openedNote.is_note">
          <small class="text-muted">Due date</small>
          <Datetime input-class="w-100" v-model="openedNote.date" type="datetime"></Datetime>
        </div>
        <hr class="my-2">
        <div>
          <small class="text-muted">Select tags</small>
          <input type="text" class="form-control" @focus="showSearchF" @blur="showSearch = false" v-model="searchQuery" @input="searchChanged" @keydown="controlFocus">
          <div class="w-100 tags-search-div">
            <transition name="fade">
              <ul class="tags-search-list list-group" v-show="showSearch" id="note-tags-search">
                <li class="list-group-item px-2 py-1" :class="{ 'focus': 0 === searchFocus }" @mouseover="setFocus(0)" @click="createTag">Create tag</li>
                <li
                  class="list-group-item px-2 py-1 text-truncate"
                  v-for="(tag, index) in filterTags()"
                  :key="tag.id"
                  :class="{'focus': index+1 === searchFocus}"
                  @mouseover="setFocus(index+1)"
                  @click="addTagToNote(tag)"
                >
                  {{ tag.name }}
                </li>
              </ul>
            </transition>
          </div>
          <div class="mt-1">
            <span
              class="badge rounded-pill bg-primary me-1"
              v-for="tag in openedNote.tags"
              :key="tag.id"
            >
              <p class="text-truncate float-start mb-0 tag-text" style="margin-top: 3px">
                {{ tag.name }}
              </p>
              <button class="text-white btn btn-sm p-0 ms-1 lh-1 fw-bold" @click="removeTagFromNote(tag)">X</button>
            </span>
          </div>
        </div>
        <button class="btn btn-danger w-100 py-0 my-3" @click="deleteNote">Delete note</button>
      </div>
    </div>

    <div v-else class="ms-3 mt-3">
      <span
        class="badge rounded-pill bg-secondary float-start mt-3 me-2 text-white ttip"
        tt-title="Double click on name or description to start editing"
      >
        ?
      </span>
      <h1 @dblclick="changeData()" class="float-start">{{ openedNote.name }}</h1>
      <br style="clear: both">
      <div v-html="getNoteData()" @dblclick="changeData()"></div>
    </div>
  </div>
</template>

<script>
import { Datetime } from 'vue-datetime';
var markdown = require('marked');
const axios = require('axios').default;

export default {
  name: "Note",
  components: {
    Datetime
  },
  data: function() {
    return {
      openedNote: false,
      isEditing: false,
      noteData: '',
      showSearch: false,
      searchQuery: '',
      tagsList: [],
      searchFocus: 0,
    };
  },
  methods: {
    deleteNote: function () {
      if (!confirm('Are you sure you want to delete?'))
        return;

      axios({
        method: 'DELETE',
        url: 'http://127.0.0.1:5000/delete/note/' + this.openedNote.id + '/',
      }).then(() => {
        this.$parent.$refs.myNotes.removeNote(this.openedNote);
        this.openedNote = false;
      });
    },
    removeTagFromNote: function(tag) {
      this.openedNote.tags = this.openedNote.tags.filter(item => item.id != tag.id);
    },
    addTagToNote: function(tag) {
      this.showSearch = false;
      this.searchQuery = '';
      this.openedNote.tags.push(tag);
    },
    createTag: function() {
      if (this.searchQuery.trim().length < 3)
        return;

      let fd = new FormData();
      fd.append('name', this.searchQuery);

      axios({
        method: 'POST',
        url: 'http://127.0.0.1:5000/create/tag/',
        data: fd,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        this.tagsList.push(response.data);
        this.$parent.$refs.mySearch.tagsList.push(response.data);
        this.addTagToNote(response.data);
      });

      this.searchQuery = '';
      this.showSearch = false;
    },
    controlFocus: function(event) {
      let elem = document.getElementById('note-tags-search');
      switch (event.keyCode) {
        case 38:
          // Up arrow
          if (this.searchFocus > 0) this.searchFocus--;
          if (this.searchFocus > 5) elem.scrollTop -= 34;
          break;
        case 27:
          // Escape
          if (document.activeElement instanceof HTMLElement)
            document.activeElement.blur();
          break;
        case 40:
          // Down arrow
          if (this.searchFocus < this.filterTags().length) this.searchFocus++;
          if (this.searchFocus > 7) elem.scrollTop += 34;
          break;
        case 13:
          // Enter
          if (this.searchFocus == 0) {
            this.createTag();
            break;
          }
          if (this.filterTags().length <= this.searchFocus-1) break;
          this.addTagToNote(
            this.filterTags()[this.searchFocus-1]
          );
          break;
      }
    },
    setFocus: function (index) {
      this.searchFocus = index;
    },
    filterTags: function () {
      let filteredByQuery = this.tagsList.filter((item) => {
        return item.name.search(new RegExp(this.searchQuery, "i")) >= 0;
      });
      let result = [];
      for (let i = 0; i < filteredByQuery.length; i++) {
        let flag = true;
        for (let j = 0; j < this.openedNote.tags.length; j++) {
          if (filteredByQuery[i].id == this.openedNote.tags[j].id) {
            flag = false;
            break;
          }
        }
        if (flag)
          result.push(filteredByQuery[i]);
      }
      return result;
    },
    searchChanged: function() {
      this.showSearchF();
      this.searchFocus = 0;
    },
    showSearchF: function() {
      if (this.searchQuery.trim().length > 1) {
        this.showSearch = true;
      } else {
        this.showSearch = false;
      }
    },
    getNoteData: function() {
      return markdown(this.noteData);
    },
    openNote: function(note) {
      if (this.isEditing && this.openedNote) {
        this.cancelDataChanges();
      }
      this.openedNote = note;
      this.isEditing = false;

      axios({
        method: 'GET',
        url: 'http://127.0.0.1:5000/get/note/' + note.id + '/',
      }).then(response => {
        if (response.data.description)
          this.noteData = response.data.description;
        else
          this.noteData = '';
      });

      axios({
        method: 'GET',
        url: 'http://127.0.0.1:5000/get/tags/',
      }).then(response => {
        this.tagsList = response.data;
      });
    },
    saveDataChanges: function() {
      if (this.openedNote.name.trim().length < 3) {
        alert('Name length must be at least 3');
        return;
      }

      let fd = new FormData();
      fd.append('name', this.openedNote.name);
      fd.append('is_note', this.openedNote.is_note);
      fd.append('date', this.openedNote.date.slice(0, -1));
      fd.append('description', this.noteData);

      let tags = '';
      for (let i=0; i<this.openedNote.tags.length; i++)
        tags += this.openedNote.tags[i].id + ' ';

      fd.append('tags', tags);

      axios({
        method: 'POST',
        url: 'http://127.0.0.1:5000/edit/note/' + this.openedNote.id + '/',
        data: fd,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(() => {
        this.isEditing = false;
        this.$parent.$refs.mySearch.tagsList.updateTags();
      });
    },
    cancelDataChanges: function () {
      axios({
        method: 'GET',
        url: 'http://127.0.0.1:5000/get/note/' + this.openedNote.id + '/',
      }).then(response => {
        if (response.data.description)
          this.noteData = response.data.description;
        else
          this.noteData = '';
        this.openedNote.name = response.data.name;
        this.openedNote.date = response.data.date;
        this.openedNote.is_note = response.data.is_note;
        this.openedNote.tags = response.data.tags;
        this.isEditing = false;
      });
    },
    changeData: function() {
      this.isEditing = true;
    }
  },
};
</script>

<style scoped>
textarea {
  resize: none;
  max-height: calc(100% - 65px);
  height: 100%;
  border: 1px solid lightgray;
  border-radius: 4px;
}

#note-main {
  height: 100%;
  max-height: 100vh;
  overflow-y: auto;
}

.ttip {
  cursor: help;
}

.ttip::after {
  background: rgba(0, 0, 0, 0.8);
	border-radius: 8px 8px 8px 0px;
	box-shadow: 1px 1px 10px rgba(0, 0, 0, 0.5);
	color: #FFF;
	content: attr(tt-title);
	margin-top: -24px;
	opacity: 0;
	padding: 3px 7px;
	position: absolute;
	visibility: hidden;
	transition: all 0.4s ease-in-out;
}

.ttip:hover::after {
  opacity: 1;
  visibility: visible;
}

.edit-div {
  max-height: calc(100% - 16px);
  max-width: calc(100% - 16px);
}

.todo-btn {
  border-radius: 0px 5px 5px 0px;
}

.note-btn {
  border-radius: 5px 0px 0px 5px;
}

.badge {
  max-width: 100%;
}

.tag-text {
  max-width: calc(100% - 15px);
}

.tags-search-div {
  position: relative;
}

.tags-search-list {
  position: absolute;
  background: white;
  width: 100%;
  max-height: 200px;
  border: 1px solid lightgray;
  overflow-y: auto;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .1s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

.list-group-item.focus {
  cursor: pointer;
  background: #0D6EFD;
  color: white;
}
</style>
