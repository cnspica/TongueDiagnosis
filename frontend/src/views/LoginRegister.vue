<script setup>
import Register_Login from '@/components/Register_Login.vue';
</script>

<template>
  <div class="login-page">
    <!-- 背景装饰 -->
    <div class="bg-grid"></div>
    <div class="bg-glow glow-1"></div>
    <div class="bg-glow glow-2"></div>
    <div class="bg-particles">
      <span v-for="i in 20" :key="i" class="particle" :style="{
        left: Math.random() * 100 + '%',
        top: Math.random() * 100 + '%',
        animationDelay: Math.random() * 6 + 's',
        animationDuration: (4 + Math.random() * 4) + 's'
      }"></span>
    </div>

    <div class="container_middle">
      <Register_Login />
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #0a0e1a;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
}

.bg-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
}

.glow-1 {
  width: 400px;
  height: 400px;
  background: rgba(0, 212, 255, 0.08);
  top: -100px;
  right: -100px;
}

.glow-2 {
  width: 300px;
  height: 300px;
  background: rgba(139, 92, 246, 0.08);
  bottom: -50px;
  left: -50px;
}

.bg-particles .particle {
  position: absolute;
  width: 2px;
  height: 2px;
  background: rgba(0, 212, 255, 0.4);
  border-radius: 50%;
  animation: particleFloat linear infinite;
  pointer-events: none;
}

@keyframes particleFloat {
  0% { opacity: 0; transform: translateY(0); }
  50% { opacity: 1; }
  100% { opacity: 0; transform: translateY(-100px); }
}

.container_middle {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 20px;
}
</style>
