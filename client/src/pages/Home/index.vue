<template>
  <div id="title-wrapper">
    <div id="title">
      <div id="highlight">
        <h1>Ready to use</h1>
        <h1 class="title-highlight">Smart Transcript</h1>
        <h1>Application</h1>
      </div>
      <a-typography-title :level="4" type="secondary">
        Explore Smart Transcript for sentiment analysis and content
        summarization. Upload text and audio files to gain insightful analysis
        and creative responses using OpenAI api and advanced technologies.
      </a-typography-title>
      <a-button type="primary" size="large"> Try it out ! </a-button>
    </div>
  </div>
  <a-divider />
  <a-row class="upload-wrapper">
    <a-col :span="24">
      <a-upload-dragger
        v-model:fileList="fileList"
        name="file"
        action="/api/upload"
        @change="handleChange"
        @drop="handleDrop"
      >
        <p class="ant-upload-drag-icon">
          <inbox-outlined></inbox-outlined>
        </p>
        <p class="ant-upload-text">Click or drag file to this area to upload</p>
        <p class="ant-upload-hint">Only support .mp4 or .mp3 files.</p>
      </a-upload-dragger>
    </a-col>
  </a-row>
</template>

<script setup>
import { ref } from "vue";
import { message } from "ant-design-vue";
const fileList = ref([]);

const titleStyle = {
  lineHeight: "120px",
};

// process file upload
const handleChange = (info) => {
  // limit file number to 1
  let resFileList = [...info.fileList];
  resFileList = resFileList.slice(-1);
  fileList.value = resFileList;

  // get status of the uploading file
  const status = info.file.status;

  if (status !== "uploading") {
    console.log(info.file, info.fileList);
  }
  if (status === "done") {
    message.success(`${info.file.name} file uploaded successfully.`);
  } else if (status === "error") {
    message.error(`${info.file.name} file upload failed.`);
  }
};

function handleDrop(e) {
  //   console.log(e);
  console.log("drop");
}
</script>

<style scoped>
#title-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

#title {
  width: 60%;
}

#highlight {
  padding-bottom: 1rem;
}

h1 {
  margin-bottom: 0.4rem;
  font-size: 50px;
  font-weight: 700;
}

.title-highlight {
  color: #1677ff;
}
</style>
