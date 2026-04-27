<script setup>
import axios from "axios";
import {ref, onMounted, onUnmounted, computed} from 'vue'

const emit = defineEmits(["getRecord"])
const props = defineProps(['isupstate'])

// 图片 URL 基路径
const imgBase = import.meta.env.DEV ? '' : ''
const color = {
  [0]: "舌色：淡白舌",
  [1]: "舌色：淡红舌",
  [2]: "舌色：红舌",
  [3]: "舌色：绛舌",
  [4]: "舌色：青紫舌",
}
const outcolor = {
  [0]: "舌苔颜色：白苔",
  [1]: "舌苔颜色：黄苔",
  [2]: "舌苔颜色：灰黑苔",
}
const rot = {
  [0]: "舌苔腻",
  [1]: "舌苔腐",
}
const thick = {
  [0]: "舌头薄",
  [1]: "舌头厚",
}

function reverseArray1(arr) {
  for (let index = 0; index < Math.floor(arr.length / 2); index++) {
    let temp = arr[index];
    arr[index] = arr[arr.length - 1 - index];
    arr[arr.length - 1 - index] = temp
  }
  return arr;
}

let rec = ref([0]);
let isEmpty = ref(false)
let pollTimer = null

onMounted(function () {
  axios.get("/api/user/record", {
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('token')
    }
  }).then(res => {
    rec.value = res.data.data
    if (rec.value && Object.keys(rec.value).length !== 0) {
      isEmpty.value = true
      reverseArray1(rec.value)
    }
  }).catch(error => {
    console.log(error);
  })
})

// 轮询（替代原来的方式，增加清理逻辑）
onMounted(function () {
  pollTimer = window.setInterval(() => {
    if (props.isupstate === true || (rec.value && rec.value[0] && rec.value[0].state === 0)) {
      axios.get("/api/user/record", {
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
      })
          .then(function (res) {
            rec.value = res.data.data
            if (rec.value && rec.value.length > 0) {
              reverseArray1(rec.value)
              if (Object.keys(rec.value).length !== 0) {
                isEmpty.value = true
              }
              if (rec.value[0].state !== 0) {
                emit("getRecord", false)
              }
            }
          })
          .catch(function (error) {
            console.log(error);
          })
    }
  }, 2000)
})

onUnmounted(() => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
})
</script>

<template>
  <div class="result-container">
    <div class="record-card" v-for="item in rec" :key="item.id" v-if="isEmpty === true">
      <div class="card-header">
        <span class="card-icon">🔬</span>
        <span class="card-title">诊断结果</span>
      </div>
      <div class="card-body">
        <div class="result-row">
          <span class="label">图片</span>
          <a :href="'/' + item.img_src" class="img-link" target="_blank">点击查看舌象图片</a>
        </div>
        <div class="result-row" v-if="item.state === 0">
          <span class="label">检测状态</span>
          <span class="value processing">检测进行中，请稍候...</span>
        </div>
        <div class="result-row" v-if="item.state === 1 && item.result">
          <span class="label">检测结果</span>
          <span class="value success">
            {{ color[item.result.tongue_color] }} · {{ outcolor[item.result.coating_color] }} · {{ rot[item.result.rot_greasy] }} · {{ thick[item.result.tongue_thickness] }}
          </span>
        </div>
        <div class="result-row" v-if="item.state === 201">
          <span class="label">检测状态</span>
          <span class="value error">未检测到舌象图片，请重新上传清晰的舌象照片</span>
        </div>
        <div class="result-row" v-if="item.state === 202">
          <span class="label">检测状态</span>
          <span class="value error">检测到多张舌象图片，请重新拍摄上传</span>
        </div>
        <div class="result-row" v-if="item.state === 203">
          <span class="label">检测状态</span>
          <span class="value error">文件类型不正确，请检查后重新上传</span>
        </div>
      </div>
    </div>
    <div v-if="!isEmpty" class="empty-state">
      <span class="empty-icon">📋</span>
      <p>暂无检测记录</p>
    </div>
  </div>
</template>

<style scoped>
.result-container {
  padding: 16px;
  max-width: 800px;
  margin: 0 auto;
}

.record-card {
  background: rgba(16, 22, 42, 0.8);
  border: 1px solid rgba(99, 179, 237, 0.15);
  border-radius: 12px;
  margin-bottom: 14px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.record-card:hover {
  border-color: rgba(99, 179, 237, 0.3);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 18px;
  background: rgba(99, 179, 237, 0.05);
  border-bottom: 1px solid rgba(99, 179, 237, 0.08);
}

.card-icon {
  font-size: 18px;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: #63b3ed;
  letter-spacing: 1px;
}

.card-body {
  padding: 14px 18px;
}

.result-row {
  display: flex;
  align-items: baseline;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid rgba(99, 179, 237, 0.05);
}

.result-row:last-child {
  border-bottom: none;
}

.label {
  font-size: 13px;
  color: rgba(224, 230, 240, 0.5);
  white-space: nowrap;
  min-width: 70px;
}

.value {
  font-size: 14px;
  color: #e0e6f0;
  line-height: 1.6;
}

.img-link {
  color: #00d4ff;
  text-decoration: underline;
  font-size: 14px;
  transition: color 0.2s;
}

.img-link:hover {
  color: #4fe0ff;
}

.value.processing {
  color: #f0b429;
}

.value.success {
  color: #48bb78;
}

.value.error {
  color: #ff6b6b;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 20px;
  gap: 12px;
}

.empty-icon {
  font-size: 36px;
  opacity: 0.4;
}

.empty-state p {
  font-size: 15px;
  color: rgba(224, 230, 240, 0.4);
}
</style>
