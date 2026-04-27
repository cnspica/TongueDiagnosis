<script setup>
import {ref} from 'vue'
import { useStateStore } from '@/stores/stateStore'

const store = useStateStore()
const showWelcome = ref(true)
const guideText = ref('')

const handleChatStart = () => {
  showWelcome.value = false
}

const changeGuideText = (text) => {
  guideText.value = text
}

defineExpose({handleChatStart, changeGuideText})
</script>

<template>
  <div class="guide-container">
    <div v-if="showWelcome" class="welcome-screen">
      <div class="glow-ring"></div>
      <div class="content-area">
        <div class="icon-wrap">
          <img src="@/assets/Chat_Tongue.webp" alt="AI" class="ai-icon"/>
        </div>
        <h1 class="title">{{ store.t('guideWelcome') }}</h1>
        <p class="subtitle">{{ store.t('guideSubtitle').replace('{action}', guideText || store.t('guideActionNew')) }}</p>
      </div>
      <div class="prompt-hint" v-if="guideText">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
          <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <span>{{ store.t('guidePrompt') }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.guide-container {
  position: relative;
  flex: 1;
  height: 100%;
  overflow: hidden;
}

.welcome-screen {
  position: absolute;
  inset: 0;
  background: #0d1117;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.glow-ring {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(79, 142, 247, 0.08) 0%, transparent 70%);
  animation: pulse-glow 4s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 1; }
}

.content-area {
  text-align: center;
  position: relative;
  z-index: 2;
}

.icon-wrap {
  margin-bottom: 2rem;
  position: relative;
}

.ai-icon {
  height: 18vh;
  border-radius: 50%;
  border: 3px solid rgba(99, 179, 237, 0.2);
  box-shadow: 0 0 40px rgba(79, 142, 247, 0.15);
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-16px); }
}

.title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #f0f4ff;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.1rem;
  color: rgba(224, 230, 240, 0.6);
  line-height: 1.8;
  white-space: pre-line;
}

.prompt-hint {
  position: absolute;
  left: 2rem;
  top: 15%;
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(16, 22, 42, 0.9);
  border: 1px solid rgba(99, 179, 237, 0.15);
  padding: 10px 16px;
  border-radius: 10px;
  color: #63b3ed;
  font-size: 0.85rem;
  animation: slide-hint 4s ease-out, shake-hint 2s ease-in-out 4s infinite;
  z-index: 101;
}

@keyframes slide-hint {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

@keyframes shake-hint {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(4px); }
  75% { transform: translateX(-4px); }
}

@media (max-width: 768px) {
  .ai-icon { height: 14vh; }
  .title { font-size: 1.6rem; }
  .subtitle { font-size: 0.95rem; }
  .prompt-hint { display: none; }
}

@media (max-width: 480px) {
  .title { font-size: 1.4rem; }
  .ai-icon { height: 12vh; }
}
</style>
