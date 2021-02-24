<template>
  <div class="notes-main">
    <ul class="list-group list-group-flush pt-0">
      <li class="list-group-item d-flex note-item" v-for="note in filteredNotes()" :key="note.id" @click="openNote($event, note)">
        <div class="flex-shrink vertical-separator d-flex align-items-center">
          <button class="btn rounded-circle complete-btn p-0" :class="noteStatus(note)" :disabled="note.isNote" @click="changeNoteStatus(note)" name="statusBtn"></button>
        </div>
        <div class="w-100 ms-2">
          <h5 class="my-0">{{ note.name }}</h5>
          <small class="text-muted" v-show="!note.isNote"><i class="far fa-clock me-1"></i> {{ note.date }}</small>
          <hr class="my-1">
          <div class="note-tags">
            <span
              class="badge rounded-pill bg-primary note-tag me-1"
              v-for="tag in note.tags"
              :key="tag.id"
            >
              {{ tag.name }}
            </span>
          </div>
        </div>
      </li>
    </ul>
    <div class="fade-effect"></div>
  </div>
</template>

<script>
export default {
  name: "NotesList",
  data: function () {
    return {
      notes: [
        {
          id: 1,
          name: "Axios CSRF",
          date: "2021-02-24T10:00:00",
          completed: false,
          isNote: true,
          tags: [
            {
              id: 1,
              name: 'Vue'
            },
            {
              id: 2,
              name: 'Django'
            },
            {
              id: 3,
              name: 'Python'
            },
          ]
        },
        {
          id: 2,
          name: "Complete notes search",
          date: "2021-02-24T10:00:00",
          completed: false,
          isNote: false,
          tags: [
            {
              id: 1,
              name: 'Vue'
            },
            {
              id: 3,
              name: 'Python'
            },
          ]
        },
      ],
      query: '',
      tags: [],
    }
  },
  methods: {
    noteStatus: function(note) {
      if (note.isNote) {
        return "btn-secondary";
      }
      if (note.completed) {
        return "btn-success";
      }
      if (new Date(note.date) < Date.now()) {
        return "btn-danger";
      }
      return "btn-outline-primary";
    },
    openNote: function(event, note) {
      if (event.target.name === "statusBtn") {
        event.preventDefault();
        event.stopPropagation();
      } else {
        console.log('Note open');
      }
      note;
      console.log(this);
    },
    changeNoteStatus: function(note) {
      note;
      console.log('Note status');
    },
    filteredNotes: function() {
      if (!this.tags && !this.query) {
        return this.notes;
      }

      let filteredByTags = [];
      for (let i=0; i<this.notes.length; i++) {
        let flag = true;
        for (let j=0; j<this.tags.length; j++) {
          if (!this.notes[i].tags.find(item => item.id == this.tags[j].id)) {
            flag = false;
          }
        }
        if (flag) {
          filteredByTags.push(this.notes[i]);
        }
      }

      return filteredByTags.filter(item => {
        return !item.name.search(new RegExp(this.query, "i"));
      });
    }
  },
  watch: {
    '$parent.$refs.mySearch.searchValue': function (value) {
      this.query = value;
    },
    '$parent.$refs.mySearch.filterTags': function (value) {
      this.tags = value;
    }
  }
};
</script>

<style scoped>
.notes-main {
  position: relative;
  width: 339px;
  height: 100%;
  overflow-y: auto;
}

.list-group-item {
  padding-left: 0px;
}

.complete-btn {
  width: 20px;
  height: 20px;
  margin: 0 7px;
  vertical-align: middle;
}

.note-item {
  transition-duration: .2s;
  background-color: white;
}

.note-item:hover {
  background-color: #f0f0f0;
  cursor: pointer;
}

.note-item:active {
  background-color: #ebebeb;
}
</style>