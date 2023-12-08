<template>
  <div class="content-wrapper">
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
      <a-button id="jump" type="primary" size="large" @click="handleJump">
        Try it out !
      </a-button>
    </div>
  </div>
  <a-divider />
  <a-row id="upload-wrapper" justify="center" align="middle">
    <a-col :span="6">
      <a-typography-title :strong="true" :level="2"
        >Create your task</a-typography-title
      >
    </a-col>
    <a-col :span="8">
      <a-card>
        <a-form
          ref="formRef"
          layout="vertical"
          :rules="rules"
          name="custom-validation"
          :model="formState"
          @finish="handleFinish"
          @finishFailed="handleFinishFailed"
        >
          <a-form-item has-feedback label="Title" name="title">
            <a-input
              v-model:value="formState.title"
              type="text"
              autocomplete="off"
            />
          </a-form-item>
          <a-form-item has-feedback label="Task" name="type">
            <a-select
              v-model:value="formState.type"
              placeholder="Please select a task type"
            >
              <a-select-option value="summary"
                >Summary extraction</a-select-option
              >
              <a-select-option value="sentiment"
                >Sentiment analysis</a-select-option
              >
            </a-select>
          </a-form-item>
          <a-form-item has-feedback label="Content" name="content">
            <a-input
              v-model:value="formState.content"
              type="text"
              autocomplete="off"
            />
          </a-form-item>
          <a-form-item label="Upload" name="upload">
            <a-upload-dragger
              v-model:fileList="formState.upload"
              :headers="headers"
              :action="action"
              @change="handleChange"
              @drop="handleDrop"
            >
              <p class="ant-upload-drag-icon">
                <inbox-outlined></inbox-outlined>
              </p>
              <p class="ant-upload-text">
                Click or drag file to this area to upload
              </p>
              <p class="ant-upload-hint">Only support .mp4 or .mp3 files.</p>
            </a-upload-dragger>
          </a-form-item>
          <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
            <a-button type="primary" html-type="submit">Submit</a-button>
            <a-button style="margin-left: 10px" @click="resetForm"
              >Reset</a-button
            >
          </a-form-item>
        </a-form>
      </a-card>
    </a-col>
  </a-row>
  <a-divider />
</template>

<script setup>
import { ref, reactive, toRaw } from "vue";
import { message } from "ant-design-vue";
import { InboxOutlined } from "@ant-design/icons-vue";

const action = import.meta.env.MODE === 'development' ? 'http://localhost:5000/api/common/upload' : '/api/common/upload'
const headers = {
  Authorization: `Bearer ${sessionStorage.getItem("token")}`
}

const formRef = ref();
const formState = reactive({
  title: "",
  content: "",
  type: "",
  resource: "",
  upload: [],
});

const validateContent = async (_rule, value) => {
  
};

const rules = {
  title: [
    {
      required: true,
      trigger: "blur",
      message: "Please input title",
    },
  ],
  content: [
    {
      validator: validateContent,
    },
  ],
  type: [
    {
      required: true,
      trigger: "blur",
      message: "Please choose a task type",
    },
  ],
};

const handleFinish = () => {
  // console.log(toRaw(formState));
  console.log(handleFinishFailed);
};

const handleFinishFailed = (errors) => {
  console.log(errors);
};

const resetForm = () => {
  formRef.value.resetFields();
};

// jump to the upload-wrapper element
const handleJump = () => {
  const uploadWrapper = document.getElementById("upload-wrapper");
  uploadWrapper.scrollIntoView({ behavior: "smooth" });
};

// process file upload
const handleChange = (info) => {
  // limit file number to 1
  let resFileList = [...info.fileList];
  resFileList = resFileList.slice(-1);
  formState.upload.value = resFileList;

  // get status of the uploading file
  const status = info.file.status;

  if (status !== "uploading") {
    console.log(info.file, info.fileList);
  }
  if (status === "done") {
    message.success(`${info.file.name} file uploaded successfully.`);
  } else if (status === "error") {
    message.error(`${info.file.name} file upload failed.`, 5);
  }
};

function handleDrop(e) {
  //   console.log(e);
  console.log("drop");
}
</script>

<style scoped>
.content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
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

#jump {
  margin-top: 1rem;
}
</style>
