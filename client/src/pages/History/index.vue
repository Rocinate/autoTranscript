<template>
  <a-row justify="center">
    <a-modal v-model:open="open" title="Basic Modal" @ok="handleOk">
      <p>Some contents...</p>
      <p>Some contents...</p>
      <p>Some contents...</p>
    </a-modal>
    <a-modal v-model:open="detailOpen" title="Basic Modal">
      <p>Some contents...</p>
      <p>Some contents...</p>
      <p>Some contents...</p>
    </a-modal>
    <a-col :span="20">
      <p class="title">History</p>
      <a-table :dataSource="dataSource" :columns="columns" bordered>
        <template #bodyCell="{ column, text, record }">
          <template v-if="column.dataIndex === 'status'">
            <a-tag v-if="text === 'Running'" color="blue">{{ text }}</a-tag>
            <a-tag v-if="text === 'Finished'" color="green">{{ text }}</a-tag>
            <a-tag v-if="text === 'Failed'" color="red">{{ text }}</a-tag>
          </template>
          <template v-if="column.dataIndex === 'audio_path'">
            <a-button type="link" v-if="text === ''" disabled>{{ "None" }}</a-button>
            <a-button type="link" v-if="text !== ''" :href="text" target="_blank">{{ "Download" }}</a-button> 
          </template>
          <template v-if="column.dataIndex === 'action'">
            <a style="margin-right: 1rem" @click="onShow(record)">Update</a>

            <a-popconfirm
              v-if="dataSource.length"
              title="Sure to delete?"
              @confirm="onDelete(record.id)"
            >
              <a>Delete</a>
            </a-popconfirm>
          </template>
        </template>
      </a-table>
      <!-- <a-row justify="end">
        <a-button type="primary" style="margin-top: 8px" @click="handleAdd"
          >Add</a-button
        >
      </a-row> -->
    </a-col>
  </a-row>
</template>
<script setup>
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import request from "../../utils/request";

const router = useRouter();
const open = ref(false);
const detailOpen = ref(false);

const columns = [
  {
    title: "id",
    dataIndex: "id",
    key: "id",
  },
  {
    title: "task",
    dataIndex: "task",
    key: "task",
  },
  {
    title: "status",
    dataIndex: "status",
    key: "status",
  },
  // {
  //   title: "analysis",
  //   dataIndex: "analysis",
  //   key: "analysis",
  //   ellipsis: true,
  // },
  {
    title: 'created_on',
    dataIndex: 'created_on',
    key: 'created_on',
  },
  {
    title: "audio",
    dataIndex: "audio_path",
    key: "audio_path",
  },
  {
    title: "action",
    dataIndex: "action",
    key: "action",
  },
];

const dataSource = ref([
  {
    key: "0",
    name: "Edward King 0",
    content: "London, Park Lane no. 0",
    task: "summary",
    status: "finished",
    audio: "",
    action: "edit",
  },
]);

const fetchData = () => {
  // fetch data from server
  request.get("/transcript/list").then((res) => {
    dataSource.value = res.data;
  });
};

const onDelete = (id) => {
  request.post("/transcript/delete", { id: id }).then((res) => {
    fetchData();
  });
};

const onShow = (record) => {
    open.value = true;
}

fetchData()

</script>

<style scoped>
.title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 20px;
}
</style>
