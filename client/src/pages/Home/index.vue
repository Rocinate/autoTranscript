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
              :disabled="formState.upload.length > 0"
              v-model:value="formState.content"
              type="text"
              autocomplete="off"
            />
          </a-form-item>
          <a-form-item label="Upload" name="upload">
            <a-upload-dragger
              :maxCount="1"
              accept=".mp3,.mp4"
              v-model:fileList="formState.upload"
              :headers="headers"
              :action="action"
              :beforeUpload="beforeUpload"
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
import { message, Upload } from "ant-design-vue";
import { InboxOutlined } from "@ant-design/icons-vue";
import { useRouter } from "vue-router";
import request from "../../utils/request";

const router = useRouter();
const action = import.meta.env.MODE === 'development' ? 'http://localhost:5000/api/common/upload' : '/api/common/upload'
const headers = {
  Authorization: `Bearer ${sessionStorage.getItem("token")}`
}

const formRef = ref();
const formState = reactive({
  title: "",
  content: "",
  type: "",
  upload: [],
});

const validateContent = async (_rule, value) => {
  if (value === "" && formState.upload.length === 0) {
    return Promise.reject("Please input content or upload a file");
  } else {
    return Promise.resolve();
  }
};

// limit file type to mp3 and mp4
const beforeUpload = (file) => {
  const isValid = file.type === "audio/mp3" || file.type === "video/mp4";
  if (!isValid) {
    message.error("You can only upload mp3 or mp4 files!");
    return Upload.LIST_IGNORE;
  } else {
    return true;
  }
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
  const data = toRaw(formState);

  if (data.upload.length > 0) {
    data['content'] = '';
    data['audio_name'] = data.upload[0].name.split('.')[0] + ".mp3";
  }

  request.post("/transcript/create", data).then((res) => {
    message.success("Task created successfully", 3);
    resetForm();
  })
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
  // get status of the uploading file
  const status = info.file.status;

  if (status === "done") {
    message.success(`File uploaded successfully.`);
  } else if (status === "error") {
    const response = info.file.response;

    // if 401, redirect to login page
    if (response.msg === "Token has expired") {
      message.error(`Login expired, redirecting in 3s`, 3);
      setTimeout(() => {
        router.push("/login");
      }, 3000);
    } else {
      message.error(`${response.msg}`, 3);
    }
  }
};

function handleDrop(e) {
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
