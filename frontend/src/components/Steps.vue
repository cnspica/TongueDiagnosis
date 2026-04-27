<script setup>
import {ref, computed, onMounted} from 'vue';

const totalTime = 40;
const remainingTime = ref(totalTime);
const dashOffset = ref(0);
const totalLength = 520;
let interval;

const barColor = computed(() => {
  const percentage = remainingTime.value / totalTime;
  if (percentage > 0.66) return '#ff6b6b';
  if (percentage > 0.33) return '#f0b429';
  return '#48bb78';
});

const startCountdown = () => {
  interval = setInterval(() => {
    if (remainingTime.value > 0) {
      remainingTime.value--;
      dashOffset.value = (1 - remainingTime.value / totalTime) * totalLength;
    } else {
      clearInterval(interval);
    }
  }, 1000);
};

const resetCountdown = () => {
  clearInterval(interval);
  remainingTime.value = totalTime;
  dashOffset.value = 0;
  startCountdown();
};

defineExpose({startCountdown, resetCountdown})
</script>

<template>
  <div class="countdown-container">
    <svg width="300" height="180" viewBox="0 0 200 100" class="countdown-svg">
      <rect x="10" y="10" width="180" height="80" rx="15" ry="15" stroke="rgba(99,179,237,0.15)" fill="none" stroke-width="5"/>
      <rect
          x="10"
          y="10"
          width="180"
          height="80"
          rx="15"
          ry="15"
          :stroke="barColor"
          fill="none"
          stroke-width="5"
          stroke-dasharray="520"
          :stroke-dashoffset="totalLength - dashOffset"
          stroke-linecap="round"
          style="transition: stroke 1s ease, stroke-dashoffset 1s linear;"
      />
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" class="countdown-text">{{
          remainingTime
        }}s
      </text>
    </svg>
    <p class="countdown-label">AI 正在分析舌象，请稍候...</p>
  </div>
</template>

<style scoped>
.countdown-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  position: relative;
}

.countdown-svg {
  position: relative;
}

.countdown-text {
  font-size: 18px;
  font-weight: bold;
  fill: #e0e6f0;
}

.countdown-label {
  margin-top: 8px;
  font-size: 14px;
  color: rgba(224, 230, 240, 0.5);
}
</style>
