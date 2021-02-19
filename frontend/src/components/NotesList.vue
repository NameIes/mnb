<template>
  <div class="notes-main">
    <ul class="list-group list-group-flush pt-0">
      <li class="list-group-item d-flex note-item">
        <div class="flex-shrink vertical-separator d-flex align-items-center">
          <button class="btn btn-outline-primary rounded-circle complete-btn p-0"></button>
        </div>
        <div class="w-100 ms-2">
          <h5 class="my-0">Axios CSRF</h5>
          <small class="text-muted"><i class="far fa-clock me-1"></i> Due tomorrow</small>
          <hr class="my-1">
          <div class="note-tags">
            <span class="badge rounded-pill bg-primary note-tag me-1">Vue</span>
            <span class="badge rounded-pill bg-primary note-tag me-1">Django</span>
            <span class="badge rounded-pill bg-primary note-tag me-1">Python</span>
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