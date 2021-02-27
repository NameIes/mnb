<template>
  <div id="note-main">
    <div class="w-100 text-center" v-if="!openedNote">
      <h4 class="mt-5">Please open note</h4>
    </div>

    <div v-else-if="isEditing" class="mx-3 mt-3 h-100">
      <input type="text" class="float-start" v-model="openedNote.name">
      <button class="btn btn-success py-0 px-4 mt-3 float-end" @click="saveDataChanges()">Save</button>
      <textarea class="w-100 mt-2" v-model="noteData"></textarea>
    </div>

    <div v-else class="ms-3 mt-3">
      <h1 @dblclick="changeData()">{{ openedNote.name }}</h1>
      <div v-html="getNoteData()" @dblclick="changeData()"></div>
    </div>
  </div>
</template>

<script>
var markdown = require('markdown').markdown;

export default {
  name: "Note",
  data: function() {
    return {
      openedNote: false,
      isEditing: false,
      noteData: '',
    };
  },
  methods: {
    getNoteData: function() {
      return markdown.toHTML(this.noteData, 'Maruku');
    },
    openNote: function(note) {
      this.openedNote = note;
      this.noteData = 'Some text';
      this.isEditing = false;
      // TODO: AXIOS
    },
    saveDataChanges: function() {
      this.isEditing = false;
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
  max-height: calc(100% - 40px);
  height: 100%;
  border: none;
}

#note-main {
  height: 100%;
  max-height: calc(100% - 20px);
  overflow-y: auto;
}
</style>
