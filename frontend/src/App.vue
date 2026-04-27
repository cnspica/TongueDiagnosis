<script setup>
import { RouterView } from 'vue-router'
import Header from '@/components/Header.vue'
</script>

<template>
  <div class="app-root">
    <Header></Header>
    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #e0e6f0;
  background-color: #0a0e1a;
  -webkit-font-smoothing: antialiased;
}

#app {
  padding: 0;
  margin: 0;
  width: 100%;
  overflow-x: hidden;
}

.app-root {
  min-height: 100vh;
}

.main-content {
  padding-top: 64px;
  min-height: 100vh;
  position: relative;
  z-index: 1;
}

.main-content > * {
  min-height: calc(100vh - 64px);
}

/* ========== Element Plus 全局深色覆盖 ========== */

/* 输入框 */
.el-input__wrapper {
  background-color: rgba(15, 20, 35, 0.8) !important;
  box-shadow: 0 0 0 1px rgba(99, 179, 237, 0.2) inset !important;
  border-radius: 8px;
}

.el-input__wrapper:hover {
  box-shadow: 0 0 0 1px rgba(99, 179, 237, 0.35) inset !important;
}

.el-input__wrapper.is-focus {
  box-shadow: 0 0 0 1px #00d4ff inset !important;
}

.el-input__inner {
  color: #e0e6f0 !important;
}

.el-input__inner::placeholder {
  color: rgba(224, 230, 240, 0.3) !important;
}

/* 输入框后缀图标 */
.el-input__suffix .el-icon {
  color: rgba(224, 230, 240, 0.4) !important;
}

.el-input__suffix .el-icon:hover {
  color: #63b3ed !important;
}

/* Input Group (append) — 侧边栏新增按钮用的 */
.el-input-group__append {
  background-color: rgba(0, 212, 255, 0.1) !important;
  border: 1px solid rgba(99, 179, 237, 0.2) !important;
  border-left: none !important;
  color: #00d4ff !important;
  box-shadow: none !important;
}

.el-input-group__append .el-button {
  background: transparent !important;
  border: none !important;
  color: #00d4ff !important;
  font-weight: 600;
  letter-spacing: 1px;
}

.el-input-group__append .el-button:hover {
  color: #4fe0ff !important;
}

/* 按钮 */
.el-button--primary {
  background: linear-gradient(135deg, #00d4ff, #0099cc) !important;
  border-color: transparent !important;
  box-shadow: 0 2px 10px rgba(0, 212, 255, 0.2);
}

.el-button--primary:hover {
  background: linear-gradient(135deg, #00e5ff, #00b3e6) !important;
  box-shadow: 0 4px 16px rgba(0, 212, 255, 0.35);
}

.el-button--success {
  background: linear-gradient(135deg, #00d4ff, #4f8ef7) !important;
  border-color: transparent !important;
}

.el-button--success:hover {
  background: linear-gradient(135deg, #00e5ff, #6ca0f7) !important;
}

/* 消息提示 */
.el-message {
  background: rgba(13, 17, 23, 0.95) !important;
  border: 1px solid rgba(99, 179, 237, 0.15) !important;
}

.el-message .el-message__content {
  color: #e0e6f0 !important;
}

/* Descriptions（诊断记录用） */
.el-descriptions {
  --el-descriptions-table-border: 1px solid rgba(99, 179, 237, 0.12) !important;
}

.el-descriptions__body {
  background: rgba(15, 20, 35, 0.6) !important;
  color: #e0e6f0 !important;
}

.el-descriptions__label {
  color: rgba(224, 230, 240, 0.6) !important;
  background: rgba(99, 179, 237, 0.05) !important;
}

.el-descriptions__content {
  color: #e0e6f0 !important;
  background: transparent !important;
}

.el-descriptions__header {
  color: #e0e6f0 !important;
}

.el-descriptions__title {
  color: #63b3ed !important;
}

/* Tag */
.el-tag {
  background: rgba(99, 179, 237, 0.1) !important;
  border-color: rgba(99, 179, 237, 0.2) !important;
  color: #63b3ed !important;
}

.el-tag a {
  color: #00d4ff !important;
  text-decoration: underline;
}

/* Card（登录/注册用） */
.el-card {
  background: rgba(15, 20, 35, 0.8) !important;
  border-color: rgba(99, 179, 237, 0.15) !important;
  color: #e0e6f0 !important;
}

/* Form 验证 */
.el-form-item__error {
  color: #ff6b6b !important;
}

/* Loading */
.el-loading-mask {
  background-color: rgba(10, 14, 26, 0.8) !important;
}

.el-loading-spinner .path {
  stroke: #00d4ff !important;
}

.el-loading-text {
  color: rgba(224, 230, 240, 0.6) !important;
}
</style>
