<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Transcripts</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" @click="toggleAddTranscriptModal">Add Transcript</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Content</th>
              <th scope="col">Analysis</th>
              <th scope="col">Task</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(transcript, index) in transcripts" :key="index">
              <td>{{ transcript.title }}</td>
              <td>{{ transcript.content }}</td>
              <td>{{ transcript.analysis }}</td>
              <td>{{ transcript.task }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- add new transcript modal -->
    <div
      ref="addTranscriptModal"
      class="modal fade"
      :class="{ show: activeAddTranscriptModal, 'd-block': activeAddTranscriptModal }"
      tabindex="-1"
      role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add a new transcript</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleAddTranscriptModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="addTranscriptTitle" class="form-label">Title:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addTranscriptTitle"
                  v-model="addTranscriptForm.title"
                  placeholder="Enter title">
              </div>
              <div class="mb-3">
                <label for="addTranscriptContent" class="form-label">Content:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addTranscriptContent"
                  v-model="addTranscriptForm.content"
                  placeholder="Enter content">
              </div>
              <div class="mb-3">
                <label for="addTask" class="form-label">Task Type:</label>
                <select
                  id="addTask"
                  class="form-select"
                  v-model="addTranscriptForm.task"
                >
                  <option value="">Select a task</option>
                  <option value="Key points identification">Key points identification</option>
                  <option value="Summary extraction">Abstract extraction</option>
                  <option value="Action item extraction">Action item extraction</option>
                  <option value="Sentiment analysis">Sentiment analysis</option>
                  <!-- Add more options as needed -->
                </select>
              </div>

              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-primary btn-sm"
                  @click="handleAddSubmit">
                  Submit
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="handleAddReset">
                  Reset
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeAddTranscriptModal" class="modal-backdrop fade show"></div>

  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      activeAddTranscriptModal: false,
      addTranscriptForm: {
        title: '',
        content: '',
        task: '',
      },
      transcripts: [],
    };
  },
  methods: {
    addTranscript(payload) {
      const path = 'http://localhost:5001/transcripts';
      axios.post(path, payload)
        .then(() => {
          this.getTranscripts();
        })
        .catch((error) => {
          console.log(error);
          this.getTranscripts();
        });
    },
    getTranscripts() {
      const path = 'http://localhost:5001/transcripts';
      axios.get(path)
        .then((res) => {
          this.transcripts = res.data.transcripts;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    handleAddReset() {
      this.initForm();
    },
    handleAddSubmit() {
      this.toggleAddTranscriptModal();
      const payload = {
        title: this.addTranscriptForm.title,
        content: this.addTranscriptForm.content,
        task: this.addTranscriptForm.task,
      };
      this.addTranscript(payload);
      this.initForm();
    },
    initForm() {
      this.addTranscriptForm.title = '';
      this.addTranscriptForm.content = '';
      this.addTranscriptForm.task = '';
    },
    toggleAddTranscriptModal() {
      const body = document.querySelector('body');
      this.activeAddTranscriptModal = !this.activeAddTranscriptModal;
      if (this.activeAddTranscriptModal) {
        body.classList.add('modal-open');
      } else {
        body.classList.remove('modal-open');
      }
    },
  },
  created() {
    this.getTranscripts();
  },
};
</script>