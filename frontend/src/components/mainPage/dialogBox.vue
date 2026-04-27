<template>
  <div class="input-bar" ref="draggableContainer">
    <div v-if="sendPic" class="upload-area">
      <el-icon class="arrow-deco arrow-l"><ArrowRightBold/></el-icon>
      <div v-if="isUploading">
        <Steps ref="stepRef"/>
      </div>
      <div v-else>
        <UploadPicture @success="startQuest" style="margin-top: 5px"/>
      </div>
      <el-icon class="arrow-deco arrow-r"><ArrowLeftBold/></el-icon>
    </div>
    <template v-else>
      <div class="drag-handle" @mousedown="startDrag">
        <el-icon><Rank/></el-icon>
      </div>
      <input @keydown="handleKeyDown" class="msg-input" v-model="inputValue" :placeholder="store.t('inputPlaceholder')"/>
      <el-button type="success" :icon="Promotion" @click="sendToMain" size="large" style="font-size: 18px;" circle/>
      <el-button
          :type="isRecording ? 'warning' : 'primary'"
          :icon="isRecording ? CircleClose : Microphone"
          @click="toggleVoiceRecognition"
          size="large"
          :loading="isLoading"
          style="font-size: 18px;"
          circle
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import {ref, reactive, onBeforeMount, computed, nextTick} from 'vue'
import {Promotion, Rank, Microphone, CircleClose, ArrowLeftBold, ArrowRightBold} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";
import {useStateStore} from '@/stores/stateStore';
import UploadPicture from '@/components/UploadPicture.vue';
import Steps from "@/components/Steps.vue";
import axios from "axios";

const store = useStateStore();
let sendPic = ref(true);
let isUploading = ref(false);
const stepRef = ref(null);
const emit = defineEmits(['send-to-main', 'send-picture']);
let inputValue = ref('');
let ask_tip = 0;
const sendToMain = () => {
  emit('send-to-main', ask_tip, inputValue.value);
  ask_tip += 1;
  inputValue.value = '';
};

const isRecording = ref(false);
const isLoading = ref(false);
const result = ref("");

let baseURL = '';
onBeforeMount(() => {
  if (store.baseUrl == "0") {
    ErrorPop("请先设置服务地址", 5000)
  }
  baseURL = store.baseUrl;
});

let recognition = null;

const tongueDictionary = {
  color: ["舌色：淡白舌,", "舌色：淡红舌,", "舌色：红舌,", "舌色：绛舌,", "舌色：青紫舌,"],
  outcolor: ["舌苔颜色：白苔,", "舌苔颜色：黄苔,", "舌苔颜色：灰黑苔,"],
  rot: ["舌苔腻,", "舌苔腐,"],
  thick: ["舌头薄,", "舌头厚,"]
};

async function getRecordData() {
  try {
    const response = await axios.get('/api/user/record', {
      headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    });
    return response.data
  } catch (error) {
    console.error('获取 /user/record 失败:', error);
    return null;
  }
}

const toggleVoiceRecognition = () => {
  if (isRecording.value) stopRecognition();
  else startRecognition();
};

const resetLoading = () => { stepRef.value.resetCountdown() }

if ('webkitSpeechRecognition' in window) {
  recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'zh-CN';
  recognition.onstart = () => { isRecording.value = true; };
  recognition.onresult = (event) => { inputValue.value += event.results[0][0].transcript; };
  recognition.onerror = () => { ErrorPop(store.t('errorSpeech')); };
  recognition.onend = () => { isRecording.value = false; };
} else {
  console.warn('当前浏览器不支持语音识别');
}

const startRecognition = () => {
  if (recognition) recognition.start();
  else ErrorPop(store.t('errorNoSpeech'));
};

const stopRecognition = () => {
  if (recognition) recognition.stop();
};

let audioType = ref("De");

interface Position { x: number; y: number; }
interface Offset { x: number; y: number; }

const position = reactive<Position>({x: window.innerWidth - 850, y: window.innerHeight - 250})
const offset = reactive<Offset>({x: 0, y: 0})
let isDragging = ref<boolean>(false)
const draggableContainer = ref<HTMLDivElement | null>(null)

const startDrag = (event: MouseEvent): void => {
  if (draggableContainer.value) {
    const rect = draggableContainer.value.getBoundingClientRect()
    isDragging.value = true
    offset.x = event.clientX - rect.left
    offset.y = event.clientY - rect.top
    document.addEventListener('mousemove', onDrag)
    document.addEventListener('mouseup', endDrag)
  }
}

const onDrag = (event: MouseEvent): void => {
  if (isDragging.value) {
    position.x = Math.max(0, Math.min(event.clientX - offset.x, window.innerWidth - (draggableContainer.value?.offsetWidth || 0)));
    position.y = Math.max(0, Math.min(event.clientY - offset.y, window.innerHeight - (draggableContainer.value?.offsetHeight || 0)));
  }
};

const endDrag = (): void => {
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', endDrag)
}

const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter') sendToMain();
};

const ErrorPop = (info: string, time = 3000) => {
  ElMessage({ showClose: true, message: info, type: 'error', duration: time })
}

let pic64 = ref("")

const startQuest = async (info) => {
  if (info.success) pic64.value = info.base64
  emit("send-picture", {base64: pic64.value, fileData: info.fileData})
  startLoading();
}

async function pollGetRecord(interval = 2000, startTime = Date.now()) {
  try {
    const responseData = await getRecordData();
    const data = responseData.data;
    if (data && data[data.length - 1].state === 1) {
      const result = data[data.length - 1].result
      let ans = ''
      ans += tongueDictionary.color[result.tongue_color]
      ans += tongueDictionary.outcolor[result.coating_color]
      ans += tongueDictionary.thick[result.tongue_thickness]
      ans += tongueDictionary.rot[result.rot_greasy]
      emit("send-picture", {base64: pic64.value, ans: ans})
      startChat();
      return data[data.length - 1].result;
    }
    setTimeout(() => pollGetRecord(interval, startTime), interval);
  } catch (error) {
    console.error("❌ 轮询获取数据失败:", error);
    setTimeout(() => pollGetRecord(interval, startTime), interval);
  }
}

const backUploading = () => { sendPic.value = true; isUploading.value = false; }
const startLoading = async () => { isUploading.value = true; await nextTick(); resetLoading(); }
const startChat = () => { sendPic.value = false; isUploading.value = false; }
const getReturn = (data) => { if (data.success) startChat(); else backUploading(); }

defineExpose({startChat, startLoading, backUploading, getReturn})
</script>

<style scoped>
.input-bar {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 800px;
  background: rgba(16, 22, 42, 0.9);
  border: 1px solid rgba(99, 179, 237, 0.15);
  border-radius: 24px;
  padding: 8px 12px;
  margin: 10px auto 16px;
  transition: all 0.3s ease;
}

.input-bar:hover {
  border-color: rgba(99, 179, 237, 0.3);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.upload-area {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
  justify-content: center;
}

.arrow-deco {
  font-size: 20px;
  color: rgba(99, 179, 237, 0.4);
}

.drag-handle {
  margin-right: 8px;
  cursor: grab;
  color: rgba(99, 179, 237, 0.4);
}

.msg-input {
  flex: 1;
  border: none;
  padding: 10px 14px;
  outline: none;
  border-radius: 18px;
  font-size: 15px;
  background: transparent;
  color: #e0e6f0;
  line-height: 1.5;
}

.msg-input::placeholder {
  color: rgba(224, 230, 240, 0.35);
}

@media (max-width: 768px) {
  .input-bar {
    max-width: 100%;
    margin: 8px 12px 12px;
    border-radius: 20px;
  }
}
</style>
