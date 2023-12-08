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
          <template v-if="column.dataIndex === 'audio'">
            <a>{{ text }}</a>
          </template>
          <template v-if="column.dataIndex === 'action'">
            <a style="margin-right: 1rem" @click="onShow(record)">Update</a>

            <a-popconfirm
              v-if="dataSource.length"
              title="Sure to delete?"
              @confirm="onDelete(record.key)"
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
    title: "name",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "content",
    dataIndex: "content",
    key: "content",
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
  {
    title: "audio",
    dataIndex: "audio",
    key: "audio",
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
    // Object.assign(info, res)
    console.log(res)
  });
};

const onDelete = (key) => {
  console.log(key);
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
