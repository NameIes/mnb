<template>
  <div id="note-main">
    <div class="w-100 text-center" v-if="!openedNote">
      <h4 class="mt-5">Please open note</h4>
    </div>

    <div v-else-if="isEditing" class="mx-3 mt-3 h-100">
      <button class="btn btn-success py-0 float-end" @click="saveDataChanges()">Save</button>
      <textarea class="w-100 mt-2" v-model="noteData"></textarea>
    </div>

    <div v-else v-html="getNoteData()" class="ms-3 mt-3" @dblclick="changeData()">
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
      note;
      // TODO: AXIOS
    },
    saveDataChanges: function() {
      console.log('test');
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
