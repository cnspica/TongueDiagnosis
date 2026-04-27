<template>
  <div class="back_ground">
    <div class="center-container">
      <div class="container">
        <!-- 左侧品牌区 -->
        <div class="brand-panel" :class="{ 'slide-right': slide_tip }">
          <div class="brand-content">
            <div class="brand-icon">🔬</div>
            <h2 class="brand-title">中医舌诊</h2>
            <p class="brand-subtitle">AI 智能舌诊分析系统</p>
            <div class="brand-divider"></div>
            <p class="brand-desc" v-if="!slide_tip">还没有账号？</p>
            <p class="brand-desc" v-else>已有账号？</p>
            <button class="switch-btn" @click="change_style">
              {{ slide_tip ? '去登录' : '去注册' }}
            </button>
          </div>
        </div>

        <!-- 右侧表单区 -->
        <div class="form-panel">
          <div class="form-box" v-loading="loading_tip" element-loading-background="rgba(10, 14, 26, 0.8)">
            <transition name="fade" mode="out-in">
              <div class="register-box" v-if="show_change" key="register">
                <h1>注 册</h1>
                <registerBlock @change="change_style" />
              </div>
              <div class="login-box" v-else key="login">
                <h1>登 录</h1>
                <loginBlock />
              </div>
            </transition>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import registerBlock from '@/components/Registerblock.vue';
import loginBlock from '@/components/Loginblock.vue';
import { ref } from 'vue'

let slide_tip = ref(false)
let show_change = ref(false)
let loading_tip = ref(false)

const change_style = () => {
  loading_tip.value = true
  slide_tip.value = !slide_tip.value
  show_change.value = !show_change.value
  setTimeout(() => {
    loading_tip.value = false
  }, 300)
}
</script>

<style scoped>
.back_ground {
  overflow: hidden;
  width: 100%;
}

.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.container {
  background: rgba(15, 20, 35, 0.9);
  width: 800px;
  min-height: 460px;
  border-radius: 16px;
  border: 1px solid rgba(0, 212, 255, 0.15);
  box-shadow:
    0 0 40px rgba(0, 212, 255, 0.05),
    0 20px 60px rgba(0, 0, 0, 0.4);
  display: flex;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(20px);
}

/* 左侧品牌面板 */
.brand-panel {
  width: 45%;
  background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(139, 92, 246, 0.1));
  border-right: 1px solid rgba(0, 212, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.5s ease-in-out;
}

.brand-panel::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 212, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 212, 255, 0.04) 1px, transparent 1px);
  background-size: 20px 20px;
}

.brand-content {
  text-align: center;
  position: relative;
  z-index: 1;
  padding: 40px 30px;
}

.brand-icon {
  font-size: 48px;
  margin-bottom: 16px;
  filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.3));
}

.brand-title {
  font-size: 26px;
  font-weight: 700;
  color: #e0e6f0;
  letter-spacing: 4px;
  margin-bottom: 8px;
}

.brand-subtitle {
  font-size: 13px;
  color: rgba(0, 212, 255, 0.7);
  letter-spacing: 2px;
  margin-bottom: 24px;
}

.brand-divider {
  width: 40px;
  height: 2px;
  background: linear-gradient(90deg, #00d4ff, #8b5cf6);
  margin: 0 auto 24px;
  border-radius: 1px;
}

.brand-desc {
  font-size: 13px;
  color: rgba(224, 230, 240, 0.5);
  margin-bottom: 16px;
  letter-spacing: 1px;
}

.switch-btn {
  background: transparent;
  color: #00d4ff;
  border: 1px solid rgba(0, 212, 255, 0.4);
  padding: 8px 28px;
  border-radius: 6px;
  font-size: 13px;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.3s;
}

.switch-btn:hover {
  background: rgba(0, 212, 255, 0.1);
  border-color: #00d4ff;
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
}

/* 右侧表单面板 */
.form-panel {
  width: 55%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.form-box {
  width: 100%;
  max-width: 340px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 30px;
  position: relative;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.register-box,
.login-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #e0e6f0;
  letter-spacing: 8px;
  font-size: 22px;
  font-weight: 600;
  position: relative;
}

h1::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 2px;
  background: linear-gradient(90deg, #00d4ff, #8b5cf6);
  border-radius: 1px;
}

/* 响应式 */
@media (max-width: 768px) {
  .container {
    flex-direction: column;
    width: 95%;
    max-width: 420px;
    min-height: auto;
  }

  .brand-panel {
    width: 100%;
    padding: 30px 20px;
    border-right: none;
    border-bottom: 1px solid rgba(0, 212, 255, 0.1);
  }

  .brand-icon {
    font-size: 36px;
  }

  .brand-title {
    font-size: 20px;
  }

  .form-panel {
    width: 100%;
  }

  .form-box {
    padding: 30px 20px;
  }
}
</style>
