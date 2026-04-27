<script setup>
import {nextTick, onBeforeMount, onMounted, ref, watch, computed} from 'vue';
import MarkdownIt from 'markdown-it';
import DOMPurify from 'dompurify';
import hljs from 'highlight.js';
import 'github-markdown-css';
import {useStateStore} from "@/stores/stateStore";
import 'highlight.js/styles/github-dark.css';
import axios from 'axios';
import emojiRegex from 'emoji-regex';
import {ElMessage} from "element-plus";

const store = useStateStore();
const sessionId = ref()

const getWelcomeText = () => {
  const t = store.t;
  return `# ${t('welcomeTitle')}\n\n` +
    `${t('welcomeUpload')}\n\n` +
    `${t('welcomeHowTitle')}\n` +
    `${t('welcomeHow1')}\n` +
    `${t('welcomeHow2')}\n` +
    `${t('welcomeHow3')}\n\n` +
    `${t('welcomeDisclaimer')}  \n` +
    `${t('welcomeDisclaimerText')}\n\n` +
    `${t('welcomeStart')}\n`;
}

const initPage = (basePic, sessionName) => {
  messages.value.push({
    text: basePic.base64,
    isUser: true,
    time: new Date().toLocaleString('default', {
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit'
    }),
    loading: false,
    isPicture: true
  });
  getPictureAnswer(basePic.fileData, sessionName);
}

const inputData = (data, id) => {
  sessionId.value = id;
  messages.value = data;
  setTimeout(() => { scrollToBottom() }, 500)
}

async function getRecordData() {
  try {
    const response = await axios.get('/api/user/record', {
      headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    });
    console.log(response.data.data[response.data.data.length - 1].state);
  } catch (error) {
    console.error('获取 /user/record 失败:', error);
    return null;
  }
}

const resetPage = () => {
  messages.value = [{
    text: getWelcomeText(),
    isUser: false,
    time: new Date().toLocaleString('default', {
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit'
    }),
    loading: false,
    isPicture: false
  }];
}

defineExpose({initPage, inputData, resetPage})

const userAvatar = ref("./static/userDefault.jpg");
const aiAvatar = ref("./static");
const messages = ref([{
  text: getWelcomeText(),
  isUser: false,
  time: new Date().toLocaleString('default', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit'
  }),
  loading: false,
  isPicture: false
}]);

let newMessage = ref('');
const chatContainer = ref(null);

const md = new MarkdownIt({
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, {language: lang}).value}</code></pre>`;
      } catch (__) {}
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
  },
});

function org(input) {
  const noMarkdown = input
    .replace(/!\[.*?\]\(.*?\)/g, '')
    .replace(/\[(.*?)\]\(.*?\)/g, '$1')
    .replace(/[`_*~#>]/g, '')
    .replace(/\n+/g, ' ');
  const regex = emojiRegex();
  return noMarkdown.replace(regex, '')
}

const sendMessage = async () => {
  if (newMessage.value.trim() !== '') {
    messages.value.push({
      text: newMessage.value,
      isUser: true,
      time: new Date().toLocaleString('default', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit'
      }),
      loading: false,
      isPicture: false
    });
    saveHistory();
    await nextTick();
    scrollToBottom();
    await sendAIMessage();
  }
};

const sendAIMessage = async () => {
  setTimeout(async () => {
    messages.value.push({
      text: '',
      isUser: false,
      time: new Date().toLocaleString('default', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit'
      }),
      loading: true,
      isPicture: false,
      receivedContent: false
    });
    await scrollToBottom();
    await getAnswer();
    await nextTick();
  }, 500);
};

const getAnswer = async () => {
  const timeout = 120000;
  let token = localStorage.getItem('token');
  const timeoutPromise = new Promise((_, reject) =>
    setTimeout(() => reject(new Error("请求超时")), timeout)
  );

  try {
    scrollToBottom();
    const response = await Promise.race([
      fetch(baseURL + "/" + sessionId.value, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          input: personalPrompt + newMessage.value,
        }),
      }),
      timeoutPromise,
    ]);

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    if (!response.body) throw new Error("流式返回没有body");

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;

    while (!done) {
      const {value, done: readerDone} = await reader.read();
      done = readerDone;
      if (value) {
        const chunk = decoder.decode(value, {stream: true});
        const lines = chunk.split("\n");
        lines.forEach((line) => {
          if (line.trim()) {
            try {
              const parsedChunk = JSON.parse(line);
              if (!parsedChunk.is_complete && parsedChunk.token) {
                const currentMessage = messages.value[messages.value.length - 1];
                if (!currentMessage.receivedContent) {
                  currentMessage.receivedContent = true;
                  currentMessage.loading = false;
                }
                currentMessage.text += parsedChunk.token;
              }
              scrollToBottom();
            } catch (parseError) {
              console.warn("JSON解析失败，跳过该行: ", line);
            }
          }
        });
      }
    }
    scrollToBottom();
  } catch (error) {
    console.error("错误: ", error);
    if (messages.value.length > 0 && messages.value[messages.value.length - 1].loading) {
      const currentMessage = messages.value[messages.value.length - 1];
      currentMessage.loading = false;
      if (!currentMessage.receivedContent) currentMessage.receivedContent = true;
    }
    messages.value.pop();
    if (error.message === "请求超时") {
      ErrorPop(store.t('errorTimeout'));
    } else {
      ErrorPop(store.t('errorGeneral'));
    }
  }
  saveHistory();
};

const getPictureAnswer = async (fileData, sessionName) => {
  emit("get-return", {success: false});
  setTimeout(async () => {
    messages.value.push({
      text: '',
      isUser: false,
      time: new Date().toLocaleString('default', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit'
      }),
      loading: true,
      isPicture: false,
      receivedContent: false
    });
    await nextTick();
  }, 0);

  const timeout = 120000;
  let token = localStorage.getItem('token');
  const timeoutPromise = new Promise((_, reject) =>
    setTimeout(() => reject(new Error("请求超时")), timeout)
  );

  try {
    const response = await Promise.race([
      (async () => {
        const formData = new FormData();
        formData.append('file_data', fileData);
        formData.append('user_input', "请描述一下");
        formData.append('name', sessionName);
        return await fetch(baseURL, {
          method: "POST",
          headers: { "Authorization": `Bearer ${token}` },
          body: formData,
        });
      })(),
      timeoutPromise,
    ]);

    if (!response.ok) {
      emit("get-return", {success: false});
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 检查是否为流式响应
    const contentType = response.headers.get('content-type') || '';
    if (!contentType.includes('x-ndjson') && !contentType.includes('stream')) {
      // 非流式响应 - 可能是错误信息
      const jsonResp = await response.json();
      if (jsonResp.code && jsonResp.code !== 0) {
        emit("get-return", {success: false});
        const currentMessage = messages.value[messages.value.length - 1];
        if (currentMessage) {
          currentMessage.loading = false;
          currentMessage.receivedContent = true;
          currentMessage.text = jsonResp.message || "诊断失败，请重试";
        }
        return;
      }
    }

    if (!response.body) throw new Error("流式返回没有body");
    emit("get-return", {success: true});

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;

    while (!done) {
      const {value, done: readerDone} = await reader.read();
      done = readerDone;
      if (value) {
        const chunk = decoder.decode(value, {stream: true});
        const lines = chunk.split("\n");
        lines.forEach((line) => {
          if (line.trim()) {
            try {
              const parsedChunk = JSON.parse(line);
              // 处理裁剪图片路径
              if (parsedChunk.cropped_img_src) {
                const currentMessage = messages.value[messages.value.length - 1];
                if (currentMessage) {
                  currentMessage.croppedImgSrc = '/' + parsedChunk.cropped_img_src;
                }
              }
              if (!parsedChunk.is_complete && parsedChunk.token) {
                const currentMessage = messages.value[messages.value.length - 1];
                if (!currentMessage.receivedContent) {
                  currentMessage.receivedContent = true;
                  currentMessage.loading = false;
                }
                currentMessage.text += parsedChunk.token;
              }
              sessionId.value = parsedChunk.session_id;
              emit("back-id", sessionId.value);
              scrollToBottom();
            } catch (parseError) {
              console.warn("JSON解析失败，跳过该行: ", line);
            }
          }
        });
      }
    }

    if (messages.value.length > 0 && messages.value[messages.value.length - 1].loading) {
      const currentMessage = messages.value[messages.value.length - 1];
      currentMessage.loading = false;
      if (!currentMessage.receivedContent) currentMessage.receivedContent = true;
    }
    scrollToBottom();
  } catch (error) {
    emit("get-return", {success: false});
    console.error("错误: ", error);
    if (messages.value.length > 0 && messages.value[messages.value.length - 1].loading) {
      const currentMessage = messages.value[messages.value.length - 1];
      currentMessage.loading = false;
      if (!currentMessage.receivedContent) currentMessage.receivedContent = true;
    }
    messages.value.pop();
    if (error.message === "请求超时") {
      ErrorPop(store.t('errorTimeout'));
    } else {
      ErrorPop(store.t('errorGeneral'));
    }
  }
};

const renderedText = (text) => DOMPurify.sanitize(md.render(text));

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

let audioType = "De";
watch(() => store.audioType, (newValue) => { audioType = newValue; });

const isPlaying = ref(false);
const fetchAndPlayAudio = async (text) => {
  text = org(text);
  if (audioType === "De") {
    if (isPlaying.value) stopAudio();
    else playAudio(text);
  }
};

const voices = ref([]);
const loadVoices = () => {
  voices.value = window.speechSynthesis.getVoices().filter(voice => voice.lang.startsWith("zh"));
};

onMounted(() => {
  loadVoices();
  window.speechSynthesis.onvoiceschanged = loadVoices;
});

const stopAudio = () => { window.speechSynthesis.cancel(); isPlaying.value = false; };
const playAudio = (text) => {
  if (!text) return;
  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "zh-CN";
  if (voices.value.length > 6) utterance.voice = voices.value[6];
  utterance.onstart = () => { isPlaying.value = true; };
  utterance.onend = () => { isPlaying.value = false; };
  utterance.onerror = () => { isPlaying.value = false; };
  synth.speak(utterance);
};

let baseURL = ""
let personalPrompt = ""

onBeforeMount(() => {
  aiAvatar.value = store.aiImagePath;
  userAvatar.value = store.userImagePath;
  store.setaudioType("De");
  baseURL = store.baseUrl;
  // 关键：注入语言指令，使 AI 用中文/英文回答
  personalPrompt = store.personalPrompt + (store.aiLangDirective || '');
});

const saveHistory = () => { store.setChatHistory(messages.value); }

const props = defineProps({ receivedInput: String });

watch(() => props.receivedInput[0], (newValue) => {
  if (newValue !== undefined) {
    const firstValue = props.receivedInput.slice(2);
    handleReceivedInput(firstValue);
  }
});

const handleReceivedInput = (inputValue) => {
  newMessage.value = inputValue;
  sendMessage();
};

const ErrorPop = (info, time = 3000) => {
  ElMessage({ showClose: true, message: info, type: 'error', duration: time })
}

const deleteMessage = (index) => {
  messages.value.splice(index, 1);
  saveHistory();
};
const emit = defineEmits(['get-return', 'back-id']);
</script>

<template>
  <div class="chat-page" ref="chatContainer">
    <div
        v-for="(message, index) in messages"
        :key="index"
        class="message-item"
        :class="message.isUser ? 'user-msg' : 'ai-msg'"
    >
      <div class="avatar" @dblclick="deleteMessage(index)">
        <img v-if="message.isUser" :src="userAvatar" alt="User"/>
        <img v-else :src="aiAvatar" alt="AI"/>
      </div>
      <div class="msg-bubble" :class="{ 'user-bubble': message.isUser }">
        <div v-if="message.loading" class="thinking">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
        <div v-else>
          <div v-if="!message.isUser" class="msg-text">
            <!-- 裁剪后的舌头图片 -->
            <div v-if="message.croppedImgSrc" class="cropped-tongue-section">
              <div class="cropped-label">🔍 舌部抠图</div>
              <img :src="message.croppedImgSrc" alt="舌头抠图" class="cropped-tongue-img"/>
            </div>
            <div class="markdown-body" v-html="renderedText(message.text)"></div>
          </div>
          <div v-else class="msg-text">
            <div v-if="message.isPicture">
              <img :src="message.text" alt="舌头图片" class="tongue-img"/>
            </div>
            <div v-else>{{ message.text }}</div>
          </div>
        </div>
        <div class="msg-meta">
          <span class="msg-time">{{ message.time }}</span>
          <button v-if="!message.isUser && !message.loading" class="voice-btn" @click="fetchAndPlayAudio(message.text)">
            🔊 {{ store.t('voicePlay') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  padding: 16px;
  flex: 1;
  overflow-y: auto;
  scroll-behavior: smooth;
}

.chat-page::-webkit-scrollbar {
  width: 5px;
}

.chat-page::-webkit-scrollbar-thumb {
  background: rgba(99, 179, 237, 0.15);
  border-radius: 4px;
}

.message-item {
  display: flex;
  align-items: flex-end;
  margin-bottom: 14px;
  gap: 10px;
}

.user-msg {
  flex-direction: row-reverse;
}

.ai-msg {
  flex-direction: row;
}

.avatar {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
}

.avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid rgba(99, 179, 237, 0.2);
}

.msg-bubble {
  max-width: 70%;
  background: rgba(16, 22, 42, 0.8);
  border: 1px solid rgba(99, 179, 237, 0.1);
  border-radius: 14px;
  padding: 12px 16px;
  color: #e0e6f0;
  font-size: 15px;
  line-height: 1.7;
  word-break: break-word;
}

.user-bubble {
  background: rgba(79, 142, 247, 0.12);
  border-color: rgba(79, 142, 247, 0.2);
}

.msg-text {
  font-size: 15px;
}

.tongue-img {
  width: 180px;
  border-radius: 10px;
  border: 1px solid rgba(99, 179, 237, 0.15);
}

.cropped-tongue-section {
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
}

.cropped-label {
  font-size: 12px;
  color: rgba(99, 179, 237, 0.8);
  font-weight: 600;
  letter-spacing: 0.5px;
}

.cropped-tongue-img {
  max-width: 220px;
  max-height: 180px;
  border-radius: 12px;
  border: 2px solid rgba(99, 179, 237, 0.25);
  box-shadow: 0 0 20px rgba(99, 179, 237, 0.1);
  background: rgba(10, 14, 26, 0.6);
  object-fit: contain;
}

.msg-meta {
  display: flex;
  align-items: center;
  margin-top: 8px;
  gap: 10px;
}

.msg-time {
  font-size: 11px;
  color: rgba(224, 230, 240, 0.35);
}

.voice-btn {
  font-size: 11px;
  color: rgba(99, 179, 237, 0.6);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s;
}

.voice-btn:hover {
  color: #63b3ed;
}

/* Thinking animation */
.thinking {
  display: flex;
  gap: 6px;
  padding: 4px 0;
}

.dot {
  width: 8px;
  height: 8px;
  background: #63b3ed;
  border-radius: 50%;
  animation: bounce 1.4s ease-in-out infinite;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

/* Markdown deep-dark overrides */
.markdown-body {
  background: transparent !important;
  color: #e0e6f0 !important;
  font-size: 15px;
}

.markdown-body h1, .markdown-body h2, .markdown-body h3 {
  color: #f0f4ff !important;
  border-bottom-color: rgba(99, 179, 237, 0.15) !important;
}

.markdown-body code {
  background: rgba(99, 179, 237, 0.08) !important;
  color: #63b3ed !important;
  border-radius: 4px;
  padding: 2px 6px;
}

.markdown-body pre {
  background: rgba(13, 17, 23, 0.6) !important;
  border: 1px solid rgba(99, 179, 237, 0.1) !important;
  border-radius: 10px;
}

.markdown-body blockquote {
  border-left-color: #4f8ef7 !important;
  color: rgba(224, 230, 240, 0.7) !important;
}

.markdown-body strong {
  color: #f0f4ff !important;
}

.markdown-body a {
  color: #63b3ed !important;
}

.markdown-body table th, .markdown-body table td {
  border-color: rgba(99, 179, 237, 0.15) !important;
}

.markdown-body table tr {
  background: transparent !important;
}

.markdown-body table tr:nth-child(2n) {
  background: rgba(99, 179, 237, 0.03) !important;
}

@media (max-width: 768px) {
  .msg-bubble {
    max-width: 85%;
    font-size: 14px;
  }
}
</style>
